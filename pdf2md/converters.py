# -*- coding: utf-8 -*-
"""Conversion engines: native PyMuPDF, Ollama, OpenAI-compatible, Anthropic."""
from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pymupdf


ProgressCb = Callable[[int, int, str], None]  # (current_page, total_pages, message)


@dataclass
class ConvertOptions:
    include_images: bool = True
    page_separator: bool = True
    image_dir: Path | None = None
    # folder name (not full path) used for relative markdown image refs
    image_dir_name: str | None = None


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
    out: list[str] = []
    for i, page in enumerate(doc):
        if progress:
            progress(i + 1, total, f"Page {i+1}/{total} (native)")
        md = _native_page_markdown(page)
        out.append(md)
        if opts.include_images and opts.image_dir is not None:
            _extract_images(doc, page, opts.image_dir, opts.image_dir_name, out)
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


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

    out: list[str] = []
    with pdfplumber.open(str(pdf_path)) as doc:
        total = len(doc.pages)
        for i, page in enumerate(doc.pages):
            if progress:
                progress(i + 1, total, f"Page {i+1}/{total} (pdfplumber)")
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            page_chunks: list[str] = []
            if text.strip():
                page_chunks.append(text.strip())
            for t in tables:
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
            out.append("\n\n".join(page_chunks))
            if opts.page_separator and i < total - 1:
                out.append("\n---\n")
    return "\n".join(out)


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
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    out: list[str] = []
    for i, page in enumerate(doc):
        if progress:
            progress(i + 1, total, f"Page {i+1}/{total} (ollama:{model})")
        img_b64 = _render_page_png_b64(page)
        payload = {
            "model": model,
            "prompt": PROMPT,
            "images": [img_b64],
            "stream": False,
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url.rstrip("/") + "/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        out.append(data.get("response", ""))
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


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
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    out: list[str] = []
    for i, page in enumerate(doc):
        if progress:
            progress(i + 1, total, f"Page {i+1}/{total} ({model})")
        img_b64 = _render_page_png_b64(page)
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                        },
                    ],
                }
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            base_url.rstrip("/") + "/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        out.append(content)
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


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
    doc = pymupdf.open(pdf_path)
    total = doc.page_count
    out: list[str] = []
    for i, page in enumerate(doc):
        if progress:
            progress(i + 1, total, f"Page {i+1}/{total} ({model})")
        img_b64 = _render_page_png_b64(page)
        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_b64,
                            },
                        },
                        {"type": "text", "text": PROMPT},
                    ],
                }
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text_parts = [
            b.get("text", "")
            for b in data.get("content", [])
            if b.get("type") == "text"
        ]
        out.append("".join(text_parts))
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


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
