# -*- coding: utf-8 -*-
"""Persistent settings for pdf2md."""
import json
import os
from pathlib import Path
from typing import Any

APP_HOME = Path.home() / ".pdf2md"
CONFIG_FILE = APP_HOME / "config.json"

DEFAULTS: dict[str, Any] = {
    "engine": "native",  # native | ollama | openai | anthropic | openai_compatible
    "ollama_url": "http://localhost:11434",
    "ollama_model": "llama3.2-vision",
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
}


def load() -> dict[str, Any]:
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
