# -*- coding: utf-8 -*-
"""Conversion engines: native PyMuPDF, Ollama, OpenAI-compatible, Anthropic."""
from __future__ import annotations

import base64
import io
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import pymupdf


ProgressCb = Callable[[int, int, str], None]  # (current_page, total_pages, message)


@dataclass
class ConvertOptions:
    include_images: bool = True
    page_separator: bool = True
    image_dir: Path | None = None  # if set, embedded images saved here


# ---------------------------------------------------------------------------
# Native PyMuPDF — offline, no LLM. Uses MuPDF's built-in markdown extraction
# (pymupdf4llm style heuristics, fallback to get_text("markdown") / blocks).
# ---------------------------------------------------------------------------

def _native_page_markdown(page: pymupdf.Page) -> str:
    # PyMuPDF >= 1.24 supports "markdown" via pymupdf4llm; fall back if missing.
    try:
        import pymupdf4llm  # type: ignore
        return pymupdf4llm.to_markdown(page.parent, pages=[page.number])
    except Exception:
        pass
    # Fallback: heuristic from blocks + font sizes.
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
            _extract_images(doc, page, opts.image_dir, out)
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


def _extract_images(
    doc: pymupdf.Document, page: pymupdf.Page, image_dir: Path, out: list[str]
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
            out.append(f"\n![image]({path.as_posix()})\n")
        except Exception:
            continue


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
# OpenAI / OpenAI-compatible (works for OpenAI, Groq, OpenRouter, LM Studio, etc.)
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
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            },
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
        # Anthropic returns content as a list of blocks
        text_parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
        out.append("".join(text_parts))
        if opts.page_separator and i < total - 1:
            out.append("\n---\n")
    doc.close()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Health / connectivity checks
# ---------------------------------------------------------------------------

def list_ollama_models(url: str) -> list[str]:
    try:
        req = urllib.request.Request(url.rstrip("/") + "/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [m["name"] for m in data.get("models", [])]
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return []
