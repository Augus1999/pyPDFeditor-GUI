# -*- coding: utf-8 -*-
"""Persistent settings and history for Distilmark."""
import json
import shutil
import datetime
from pathlib import Path
from typing import Any

APP_HOME = Path.home() / ".distilmark"
_LEGACY_HOME = Path.home() / ".pdf2md"  # pre-1.0 location
CONFIG_FILE = APP_HOME / "config.json"
HISTORY_FILE = APP_HOME / "history.json"

MAX_HISTORY = 500


def _migrate_legacy() -> None:
    """One-time migration of pre-1.0 ``~/.pdf2md`` settings/history."""
    try:
        if _LEGACY_HOME.exists() and not APP_HOME.exists():
            shutil.copytree(_LEGACY_HOME, APP_HOME)
    except OSError:
        pass

# Ollama preset models
OLLAMA_PRESETS = {
    "powerful": {
        "label": "🚀 Powerful (90B)",
        "model": "llama3.2-vision:90b",
        "desc": "Best quality · needs 64GB+ VRAM",
    },
    "balanced": {
        "label": "⚡ Balanced (11B)",
        "model": "llama3.2-vision:11b",
        "desc": "Great quality · needs 8GB+ VRAM",
    },
    "light": {
        "label": "💨 Light (7B)",
        "model": "moondream:latest",
        "desc": "Fast · needs 4GB+ VRAM",
    },
}

DEFAULTS: dict[str, Any] = {
    "engine": "native",
    "ollama_url": "http://localhost:11434",
    "ollama_model": "llama3.2-vision:11b",
    "ollama_extra_scan_path": "",
    "openai_api_key": "",
    "openai_model": "gpt-4o-mini",
    "openai_base_url": "https://api.openai.com/v1",
    "anthropic_api_key": "",
    "anthropic_model": "claude-haiku-4-5-20251001",
    "compat_api_key": "",
    "compat_base_url": "",
    "compat_model": "",
    "theme": "dark",
    "include_images": True,
    "page_separator": True,
    "last_output_dir": str(Path.home()),
    # page range (blank = all pages)
    "page_range_from": "",
    "page_range_to": "",
    # OCR fallback (needs Tesseract installed)
    "ocr_enabled": False,
    "ocr_language": "eng",
    # post-processing pipeline
    "pp_merge_hyphens": False,
    "pp_collapse_blanks": False,
    "pp_strip_headers_footers": False,
    # pdfplumber table tuning
    "plumber_tables_enabled": True,
    "plumber_vertical_strategy": "lines",
    "plumber_horizontal_strategy": "lines",
    "plumber_snap_tolerance": 3,
    # parallel page processing for hosted LLM engines
    "llm_concurrency": 1,
    # LLM custom prompt — blank = built-in default
    "custom_prompt": "",
    # math-mode prompt augmentation
    "math_mode": False,
    # stream live tokens from LLM engines into Preview
    "stream_output": False,
    # auto-open output folder when a batch finishes
    "auto_open_output": False,
    # watch a folder for new PDFs and auto-add them
    "watch_folder": "",
    "watch_auto_convert": False,
}


def load() -> dict[str, Any]:
    _migrate_legacy()
    APP_HOME.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save(DEFAULTS)
        return dict(DEFAULTS)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        merged = dict(DEFAULTS)
        merged.update(data)
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULTS)


def save(cfg: dict[str, Any]) -> None:
    APP_HOME.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------

def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return []


def append_history(entry: dict) -> None:
    APP_HOME.mkdir(parents=True, exist_ok=True)
    history = load_history()
    entry.setdefault("ts", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    history.append(entry)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2, ensure_ascii=False)


def clear_history() -> None:
    if HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")
