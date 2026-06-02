# -*- coding: utf-8 -*-
"""Courses / Projects — organise PDFs into courses with chapters.

A *course* (project) groups source PDFs into ordered *chapters*. Each chapter
holds *documents*, where a document tracks its source PDF and — once converted —
its Markdown output, engine, page count, and status. This powers a library view
so you can see, per course, which files you've added and which are converted
(e.g. when revising for an exam from many per-chapter PDFs).

Persisted as JSON at ``~/.distilmark/projects.json``.
"""
from __future__ import annotations

import json
import uuid
import datetime
from pathlib import Path
from typing import Any

from .config import APP_HOME

PROJECTS_FILE = APP_HOME / "projects.json"

# Document status values
ADDED = "added"          # queued in the course, not yet converted
CONVERTED = "converted"  # successfully converted to Markdown
FAILED = "failed"        # last conversion attempt failed


def _now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def load() -> dict[str, Any]:
    if not PROJECTS_FILE.exists():
        return {"projects": []}
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data.setdefault("projects", [])
        return data
    except (json.JSONDecodeError, OSError):
        return {"projects": []}


def save(data: dict[str, Any]) -> None:
    APP_HOME.mkdir(parents=True, exist_ok=True)
    with open(PROJECTS_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def _find_project(data: dict, pid: str) -> dict | None:
    return next((p for p in data["projects"] if p["id"] == pid), None)


def _find_chapter(project: dict, cid: str) -> dict | None:
    return next((c for c in project.get("chapters", []) if c["id"] == cid), None)


# ---------------------------------------------------------------------------
# Projects (courses)
# ---------------------------------------------------------------------------

def add_project(name: str) -> dict:
    data = load()
    project = {
        "id": _new_id(),
        "name": name.strip() or "Untitled course",
        "created": _now(),
        "chapters": [],
    }
    data["projects"].append(project)
    save(data)
    return project


def rename_project(pid: str, name: str) -> None:
    data = load()
    p = _find_project(data, pid)
    if p:
        p["name"] = name.strip() or p["name"]
        save(data)


def delete_project(pid: str) -> None:
    data = load()
    data["projects"] = [p for p in data["projects"] if p["id"] != pid]
    save(data)


# ---------------------------------------------------------------------------
# Chapters
# ---------------------------------------------------------------------------

def add_chapter(pid: str, name: str) -> dict | None:
    data = load()
    p = _find_project(data, pid)
    if not p:
        return None
    chapter = {"id": _new_id(), "name": name.strip() or "New chapter", "documents": []}
    p.setdefault("chapters", []).append(chapter)
    save(data)
    return chapter


def rename_chapter(pid: str, cid: str, name: str) -> None:
    data = load()
    p = _find_project(data, pid)
    if not p:
        return
    c = _find_chapter(p, cid)
    if c:
        c["name"] = name.strip() or c["name"]
        save(data)


def delete_chapter(pid: str, cid: str) -> None:
    data = load()
    p = _find_project(data, pid)
    if not p:
        return
    p["chapters"] = [c for c in p.get("chapters", []) if c["id"] != cid]
    save(data)


def move_chapter(pid: str, cid: str, delta: int) -> None:
    """Move a chapter up (delta<0) or down (delta>0) in the ordering."""
    data = load()
    p = _find_project(data, pid)
    if not p:
        return
    chapters = p.get("chapters", [])
    idx = next((i for i, c in enumerate(chapters) if c["id"] == cid), None)
    if idx is None:
        return
    new = max(0, min(len(chapters) - 1, idx + delta))
    chapters.insert(new, chapters.pop(idx))
    save(data)


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

def add_document(pid: str, cid: str, source: str) -> bool:
    """Add a source PDF to a chapter. Returns False if already present."""
    data = load()
    p = _find_project(data, pid)
    if not p:
        return False
    c = _find_chapter(p, cid)
    if c is None:
        return False
    if any(d["source"] == source for d in c.setdefault("documents", [])):
        return False
    c["documents"].append({
        "source": source,
        "output": "",
        "engine": "",
        "pages": 0,
        "status": ADDED,
        "ts": _now(),
    })
    save(data)
    return True


def update_document(pid: str, cid: str, source: str, **fields) -> None:
    data = load()
    p = _find_project(data, pid)
    if not p:
        return
    c = _find_chapter(p, cid)
    if c is None:
        return
    for d in c.get("documents", []):
        if d["source"] == source:
            d.update(fields)
            d["ts"] = _now()
            break
    save(data)


def remove_document(pid: str, cid: str, source: str) -> None:
    data = load()
    p = _find_project(data, pid)
    if not p:
        return
    c = _find_chapter(p, cid)
    if c is None:
        return
    c["documents"] = [d for d in c.get("documents", []) if d["source"] != source]
    save(data)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def project_stats(project: dict) -> tuple[int, int, int]:
    """Return (chapters, total_documents, converted_documents)."""
    chapters = project.get("chapters", [])
    docs = 0
    converted = 0
    for c in chapters:
        for d in c.get("documents", []):
            docs += 1
            if d.get("status") == CONVERTED:
                converted += 1
    return len(chapters), docs, converted
