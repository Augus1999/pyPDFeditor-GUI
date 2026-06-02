# -*- coding: utf-8 -*-
"""Conversion engines: native PyMuPDF, pdfplumber, Ollama, OpenAI, Anthropic.

Shared features handled here (engine-agnostic):
  • page range selection            (opts.page_range)
  • OCR fallback for scanned pages  (opts.ocr_enabled)
  • post-processing pipeline        (opts.pp_*)
  • pdfplumber table tuning         (opts.plumber_table_settings)
  • concurrent page processing      (opts.llm_concurrency, LLM engines only)
  • cooperative cancellation        (opts.cancel_check)
"""
from __future__ import annotations

import base64
import json
import re
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pymupdf


ProgressCb = Callable[[int, int, str], None]  # (current_page, total_pages, message)


class CancelledError(Exception):
    """Raised cooperatively when the user cancels a running conversion."""


@dataclass
class ConvertOptions:
    include_images: bool = True
    page_separator: bool = True
    image_dir: Path | None = None
    # folder name (not full path) used for relative markdown image refs
    image_dir_name: str | None = None
    # 1-based inclusive page range; None = all pages
    page_range: tuple[int, int] | None = None
    # OCR fallback for pages with no extractable text (needs Tesseract)
    ocr_enabled: bool = False
    ocr_language: str = "eng"
    # post-processing pipeline
    pp_merge_hyphens: bool = False
    pp_collapse_blanks: bool = False
    pp_strip_headers_footers: bool = False
    # pdfplumber table extraction
    plumber_tables_enabled: bool = True
    # pdfplumber table-extraction tuning (passed straight to extract_tables)
    plumber_table_settings: dict | None = None
    # number of pages processed in parallel for LLM engines (1 = sequential)
    llm_concurrency: int = 1
    # cooperative cancellation: a callable that returns True to abort
    cancel_check: Callable[[], bool] | None = None
    # custom prompt for LLM engines (empty/None = default PROMPT)
    custom_prompt: str | None = None
    # math-mode prompt augmentation (LLM engines only)
    math_mode: bool = False
    # streaming callback: stream_cb(page_index_0based, partial_text)
    stream_cb: Callable[[int, str], None] | None = None


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _check_cancel(opts: ConvertOptions) -> None:
    if opts.cancel_check and opts.cancel_check():
        raise CancelledError("Conversion cancelled by user.")


def _page_indices(total: int, page_range: tuple[int, int] | None) -> list[int]:
    """Return 0-based page indices to process for a 1-based inclusive range."""
    if not page_range:
        return list(range(total))
    start, end = page_range
    start = max(1, start or 1)
    end = min(total, end or total)
    return [i for i in range(total) if start <= i + 1 <= end]


def _ocr_page(page: pymupdf.Page, language: str = "eng", dpi: int = 200) -> str:
    """OCR a page via PyMuPDF's Tesseract integration. Raises if unavailable."""
    tp = page.get_textpage_ocr(flags=3, language=language, dpi=dpi, full=True)
    return page.get_text(textpage=tp).strip()


# ---- post-processing ----

def _strip_headers_footers(pages: list[str]) -> list[str]:
    """Drop the first/last line of each page when it repeats across most pages
    (running headers / footers / page numbers)."""
    if len(pages) < 3:
        return pages
    firsts: Counter[str] = Counter()
    lasts: Counter[str] = Counter()
    parsed: list[tuple[list[str], list[tuple[int, str]]]] = []
    for p in pages:
        lines = p.splitlines()
        non_empty = [(i, l) for i, l in enumerate(lines) if l.strip()]
        parsed.append((lines, non_empty))
        if non_empty:
            firsts[non_empty[0][1].strip()] += 1
            lasts[non_empty[-1][1].strip()] += 1
    threshold = max(2, len(pages) // 2)
    common_first = {l for l, c in firsts.items() if c >= threshold}
    common_last = {l for l, c in lasts.items() if c >= threshold}
    if not common_first and not common_last:
        return pages
    cleaned: list[str] = []
    for lines, non_empty in parsed:
        drop: set[int] = set()
        k = 0
        while k < len(non_empty) and non_empty[k][1].strip() in common_first:
            drop.add(non_empty[k][0])
            k += 1
        k = len(non_empty) - 1
        while k >= 0 and non_empty[k][1].strip() in common_last:
            drop.add(non_empty[k][0])
            k -= 1
        cleaned.append("\n".join(l for i, l in enumerate(lines) if i not in drop))
    return cleaned


def postprocess(pages: list[str], opts: ConvertOptions) -> list[str]:
    if opts.pp_strip_headers_footers:
        pages = _strip_headers_footers(pages)
    if opts.pp_merge_hyphens:
        pages = [re.sub(r"(\w)-\n(\w)", r"\1\2", p) for p in pages]
    return pages


def _assemble(pages: list[str], opts: ConvertOptions) -> str:
    parts: list[str] = []
    for k, p in enumerate(pages):
        parts.append(p)
        if opts.page_separator and k < len(pages) - 1:
            parts.append("\n---\n")
    text = "\n".join(parts)
    if opts.pp_collapse_blanks:
        text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ---------------------------------------------------------------------------
# Native PyMuPDF
# ---------------------------------------------------------------------------

def _native_page_markdown(page: pymupdf.Page) -> str:
    try:
        import pymupdf4llm  # type: ignore
        return pymupdf4llm.to_markdown(page.parent, pages=[page.number])
    except Exception:
        pass
    blocks = page.get_text("dict")["blocks"]
    parts: list[str] = []
    for b in blocks:
        if b.get("type", 0) != 0:
            continue
        for line in b.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue
            size = max((s.get("size", 0) for s in spans), default=0)
            flags = spans[0].get("flags", 0)
            bold = bool(flags & 16)
            if size >= 20:
                parts.append(f"# {text}")
            elif size >= 16:
                parts.append(f"## {text}")
            elif size >= 13:
                parts.append(f"### {text}")
            elif bold:
                parts.append(f"**{text}**")
            else:
                parts.append(text)
        parts.append("")
    return "\n".join(parts)


def convert_native(
    pdf_path: Path,
    opts: ConvertOptions,
    progress: ProgressCb | None = None,
) -> str:
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    indices = _page_indices(total, opts.page_range)
    pages: list[str] = []
    for n, i in enumerate(indices):
        _check_cancel(opts)
        page = doc[i]
        if progress:
            progress(n + 1, len(indices), f"Page {i+1}/{total} (native)")
        raw = page.get_text().strip()
        if opts.ocr_enabled and len(raw) < 8:
            try:
                md = _ocr_page(page, opts.ocr_language)
            except Exception as e:  # Tesseract missing / failed — keep going
                md = f"<!-- OCR unavailable for page {i+1}: {e} -->"
        else:
            md = _native_page_markdown(page)
        chunk = [md]
        if opts.include_images and opts.image_dir is not None:
            _extract_images(doc, page, opts.image_dir, opts.image_dir_name, chunk)
        pages.append("\n".join(chunk))
    doc.close()
    pages = postprocess(pages, opts)
    return _assemble(pages, opts)


def _extract_images(
    doc: pymupdf.Document,
    page: pymupdf.Page,
    image_dir: Path,
    image_dir_name: str | None,
    out: list[str],
) -> None:
    image_dir.mkdir(parents=True, exist_ok=True)
    for img_index, info in enumerate(page.get_images(full=True)):
        xref = info[0]
        try:
            pix = pymupdf.Pixmap(doc, xref)
            if pix.n - pix.alpha >= 4:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            name = f"page{page.number+1}_img{img_index+1}.png"
            path = image_dir / name
            pix.save(str(path))
            # use relative path so markdown previews work anywhere
            if image_dir_name:
                ref = f"./{image_dir_name}/{name}"
            else:
                ref = path.as_posix()
            out.append(f"\n![image]({ref})\n")
        except Exception:
            continue


# ---------------------------------------------------------------------------
# pdfplumber — offline, layout-aware extraction with table support
# ---------------------------------------------------------------------------

def _table_to_md(table: list[list[str | None]]) -> str:
    rows = [[(c or "").strip().replace("|", "\\|").replace("\n", " ") for c in row] for row in table]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    header = rows[0]
    sep = ["---"] * width
    body = rows[1:] if len(rows) > 1 else []
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def convert_pdfplumber(
    pdf_path: Path,
    opts: ConvertOptions,
    progress: ProgressCb | None = None,
) -> str:
    try:
        import pdfplumber  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "pdfplumber is not installed. Run: pip install pdfplumber"
        ) from e

    table_settings = opts.plumber_table_settings or None
    pages_md: list[str] = []
    with pdfplumber.open(str(pdf_path)) as doc:
        total = len(doc.pages)
        indices = _page_indices(total, opts.page_range)
        for n, i in enumerate(indices):
            _check_cancel(opts)
            page = doc.pages[i]
            if progress:
                progress(n + 1, len(indices), f"Page {i+1}/{total} (pdfplumber)")
            text = page.extract_text() or ""
            tables = []
            if opts.plumber_tables_enabled:
                try:
                    tables = page.extract_tables(table_settings) if table_settings else page.extract_tables()
                except Exception:
                    tables = []
            page_chunks: list[str] = []
            if text.strip():
                page_chunks.append(text.strip())
            elif opts.ocr_enabled:
                # pdfplumber can't OCR — fall back to PyMuPDF Tesseract
                try:
                    import pymupdf as _mu
                    _d = _mu.open(str(pdf_path))
                    ocr_text = _ocr_page(_d[i], opts.ocr_language)
                    _d.close()
                    if ocr_text:
                        page_chunks.append(ocr_text)
                except Exception as e:
                    page_chunks.append(f"<!-- OCR unavailable for page {i+1}: {e} -->")
            for t in tables or []:
                md_table = _table_to_md(t)
                if md_table:
                    page_chunks.append("\n" + md_table + "\n")
            if opts.include_images and opts.image_dir is not None:
                # pdfplumber doesn't extract embedded images directly; fall back
                # to PyMuPDF for the image side-pull so users still get them.
                try:
                    import pymupdf as _mu
                    _d = _mu.open(str(pdf_path))
                    _extract_images(_d, _d[i], opts.image_dir, opts.image_dir_name, page_chunks)
                    _d.close()
                except Exception:
                    pass
            pages_md.append("\n\n".join(page_chunks))
    pages_md = postprocess(pages_md, opts)
    return _assemble(pages_md, opts)


# ---------------------------------------------------------------------------
# Page rendering helper for vision-capable LLMs
# ---------------------------------------------------------------------------

def _render_page_png_b64(page: pymupdf.Page, dpi: int = 150) -> str:
    pix = page.get_pixmap(dpi=dpi)
    data = pix.tobytes("png")
    return base64.b64encode(data).decode("ascii")


PROMPT = (
    "Convert this PDF page to clean Markdown. Preserve headings, lists, "
    "tables (use GitHub-flavored markdown), code blocks, and inline emphasis. "
    "Do not add commentary. Output only the markdown."
)

MATH_PROMPT_ADDITION = (
    " Preserve mathematical formulas: wrap inline math with single dollar signs "
    "($x = a + b$) and display equations with double dollar signs ($$...$$). "
    "Use proper LaTeX notation."
)


def _resolve_prompt(opts: ConvertOptions) -> str:
    p = (opts.custom_prompt or "").strip() or PROMPT
    if opts.math_mode and MATH_PROMPT_ADDITION not in p:
        p = p + MATH_PROMPT_ADDITION
    return p


def is_likely_scanned(pdf_path: Path, sample_pages: int = 3, threshold: int = 50) -> bool:
    """Heuristic: very little extractable text per sampled page → probably scanned."""
    try:
        doc = pymupdf.open(pdf_path)
        n = min(sample_pages, doc.page_count)
        if n == 0:
            return False
        total = 0
        for i in range(n):
            total += len(doc[i].get_text().strip())
        doc.close()
        return total < threshold * n
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Generic LLM page runner (sequential or concurrent)
# ---------------------------------------------------------------------------

PageFn = Callable[[int, str], str]  # (page_idx_0based, image_b64) -> markdown


def _run_llm(
    pdf_path: Path,
    opts: ConvertOptions,
    progress: ProgressCb | None,
    label: str,
    page_fn: PageFn,
) -> str:
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    indices = _page_indices(total, opts.page_range)
    # Render all needed pages up front — PyMuPDF docs are not thread-safe, so
    # the parallel workers only ever touch the already-encoded PNG bytes.
    images: dict[int, str] = {}
    for i in indices:
        _check_cancel(opts)
        images[i] = _render_page_png_b64(doc[i])
    doc.close()

    n_total = len(indices)
    results: dict[int, str] = {}
    concurrency = max(1, opts.llm_concurrency)

    if concurrency == 1:
        for n, i in enumerate(indices):
            _check_cancel(opts)
            if progress:
                progress(n + 1, n_total, f"Page {i+1}/{total} ({label})")
            results[i] = page_fn(i, images[i])
    else:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        done = 0
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futs = {ex.submit(page_fn, i, images[i]): i for i in indices}
            try:
                for fut in as_completed(futs):
                    _check_cancel(opts)
                    results[futs[fut]] = fut.result()
                    done += 1
                    if progress:
                        progress(done, n_total, f"Page {done}/{n_total} ({label}, ×{concurrency})")
            except BaseException:
                for f in futs:
                    f.cancel()
                raise

    pages = [results[i] for i in indices]
    pages = postprocess(pages, opts)
    return _assemble(pages, opts)


# ---------------------------------------------------------------------------
# Ollama (local, offline)
# ---------------------------------------------------------------------------

def convert_ollama(
    pdf_path: Path,
    url: str,
    model: str,
    opts: ConvertOptions,
    progress: ProgressCb | None = None,
) -> str:
    prompt = _resolve_prompt(opts)
    streaming = opts.stream_cb is not None

    def page_fn(idx: int, img_b64: str) -> str:
        payload = {
            "model": model, "prompt": prompt,
            "images": [img_b64], "stream": streaming,
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url.rstrip("/") + "/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        if not streaming:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "")
        # Streaming: Ollama sends NDJSON lines
        out = []
        with urllib.request.urlopen(req, timeout=600) as resp:
            for raw in resp:
                if not raw.strip():
                    continue
                try:
                    d = json.loads(raw.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                chunk = d.get("response", "")
                if chunk:
                    out.append(chunk)
                    if opts.stream_cb:
                        opts.stream_cb(idx, chunk)
                if d.get("done"):
                    break
        return "".join(out)

    return _run_llm(pdf_path, opts, progress, f"ollama:{model}", page_fn)


# ---------------------------------------------------------------------------
# OpenAI / OpenAI-compatible
# ---------------------------------------------------------------------------

def convert_openai_compatible(
    pdf_path: Path,
    base_url: str,
    api_key: str,
    model: str,
    opts: ConvertOptions,
    progress: ProgressCb | None = None,
) -> str:
    prompt = _resolve_prompt(opts)
    streaming = opts.stream_cb is not None

    def page_fn(idx: int, img_b64: str) -> str:
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                ],
            }],
        }
        if streaming:
            payload["stream"] = True
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions",
            data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {api_key}"},
        )
        if not streaming:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        # Streaming: SSE — lines beginning with "data: " carry JSON deltas
        out = []
        with urllib.request.urlopen(req, timeout=600) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"):
                    continue
                payload_str = line[5:].strip()
                if payload_str == "[DONE]":
                    break
                try:
                    d = json.loads(payload_str)
                except json.JSONDecodeError:
                    continue
                try:
                    chunk = d["choices"][0]["delta"].get("content", "")
                except (KeyError, IndexError):
                    chunk = ""
                if chunk:
                    out.append(chunk)
                    if opts.stream_cb:
                        opts.stream_cb(idx, chunk)
        return "".join(out)

    return _run_llm(pdf_path, opts, progress, model, page_fn)


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------

def convert_anthropic(
    pdf_path: Path,
    api_key: str,
    model: str,
    opts: ConvertOptions,
    progress: ProgressCb | None = None,
) -> str:
    prompt = _resolve_prompt(opts)
    streaming = opts.stream_cb is not None

    def page_fn(idx: int, img_b64: str) -> str:
        payload = {
            "model": model, "max_tokens": 4096,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": prompt},
                ],
            }],
        }
        if streaming:
            payload["stream"] = True
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={"Content-Type": "application/json",
                     "x-api-key": api_key,
                     "anthropic-version": "2023-06-01"},
        )
        if not streaming:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            text_parts = [b.get("text", "")
                          for b in data.get("content", [])
                          if b.get("type") == "text"]
            return "".join(text_parts)
        # Streaming via SSE: content_block_delta events carry text_delta
        out = []
        with urllib.request.urlopen(req, timeout=600) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "ignore").strip()
                if not line.startswith("data:"):
                    continue
                try:
                    d = json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
                if d.get("type") == "content_block_delta":
                    delta = d.get("delta", {})
                    if delta.get("type") == "text_delta":
                        chunk = delta.get("text", "")
                        if chunk:
                            out.append(chunk)
                            if opts.stream_cb:
                                opts.stream_cb(idx, chunk)
                if d.get("type") == "message_stop":
                    break
        return "".join(out)

    return _run_llm(pdf_path, opts, progress, model, page_fn)


# ---------------------------------------------------------------------------
# Cost estimation (rough — for hosted LLM engines only)
# ---------------------------------------------------------------------------

# Approximate USD prices per 1K tokens: (input, output). Matched by substring.
LLM_PRICES: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.00015, 0.0006),
    "gpt-4o": (0.0025, 0.01),
    "gpt-4.1-mini": (0.0004, 0.0016),
    "gpt-4.1": (0.002, 0.008),
    "claude-haiku": (0.0008, 0.004),
    "claude-sonnet": (0.003, 0.015),
    "claude-opus": (0.015, 0.075),
}

# rough vision tokens consumed by one rendered page image, plus typical output
_IMG_TOKENS = 1100
_AVG_OUTPUT_TOKENS = 700


def _price_for(model: str) -> tuple[float, float]:
    m = (model or "").lower()
    for key, price in LLM_PRICES.items():
        if key in m:
            return price
    return (0.001, 0.004)  # generic fallback


def estimate_cost(engine: str, model: str, total_pages: int) -> float | None:
    """Return a rough USD estimate, or None for free/offline engines."""
    if engine in ("native", "pdfplumber", "compare", "ollama"):
        return None
    inp, out = _price_for(model)
    return total_pages * (_IMG_TOKENS / 1000 * inp + _AVG_OUTPUT_TOKENS / 1000 * out)


def count_pages(pdf_path: Path) -> int:
    try:
        doc = pymupdf.open(pdf_path)
        n = doc.page_count
        doc.close()
        return n
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Ollama helpers
# ---------------------------------------------------------------------------

def list_ollama_models(url: str) -> list[str]:
    try:
        req = urllib.request.Request(url.rstrip("/") + "/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [m["name"] for m in data.get("models", [])]
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return []


PullProgressCb = Callable[[str, int, int], None]  # (status, total, completed)


def pull_ollama_model(
    url: str,
    model: str,
    progress_cb: PullProgressCb,
) -> None:
    """Stream-pull an Ollama model. Calls progress_cb for each progress line."""
    payload = {"name": model, "stream": True}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + "/api/pull",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=7200) as resp:
        for raw in resp:
            raw = raw.strip()
            if not raw:
                continue
            try:
                d = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            progress_cb(
                d.get("status", ""),
                d.get("total", 0),
                d.get("completed", 0),
            )
