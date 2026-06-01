# -*- coding: utf-8 -*-
"""Ollama service detection, model discovery, and direct downloader.

The direct downloader bypasses the Ollama daemon entirely and pulls
blobs from registry.ollama.ai over plain HTTP, mirroring the layout
expected by Ollama (manifests/ + blobs/). Inspired by
https://github.com/Gholamrezadar/ollama-direct-downloader.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


# ---------------------------------------------------------------------------
# Service health & startup
# ---------------------------------------------------------------------------

def is_running(url: str = "http://localhost:11434", timeout: float = 2.0) -> bool:
    try:
        req = urllib.request.Request(url.rstrip("/") + "/api/tags")
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except (urllib.error.URLError, OSError):
        return False


def has_ollama_binary() -> str | None:
    """Return absolute path to the ollama binary if installed, else None."""
    found = shutil.which("ollama")
    if found:
        return found
    # Common Windows locations
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
        Path("C:/Program Files/Ollama/ollama.exe"),
        Path("C:/Program Files (x86)/Ollama/ollama.exe"),
    ]
    for c in candidates:
        try:
            if c.is_file():
                return str(c)
        except OSError:
            continue
    return None


def start_service() -> tuple[bool, str]:
    """Launch `ollama serve` in the background. Returns (ok, message)."""
    binary = has_ollama_binary()
    if not binary:
        return False, (
            "Ollama is not installed.\n"
            "Download it from https://ollama.com/download"
        )
    try:
        if platform.system() == "Windows":
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                [binary, "serve"],
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )
        else:
            subprocess.Popen(
                [binary, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        return True, "Started `ollama serve`. Give it a few seconds…"
    except Exception as e:
        return False, f"Failed to start Ollama: {e}"


# ---------------------------------------------------------------------------
# Model discovery via filesystem (works even when daemon is down)
# ---------------------------------------------------------------------------

@dataclass
class InstalledModel:
    name: str       # e.g. "llama3.2-vision:11b"
    namespace: str  # "library" or other
    path: Path      # path to the manifest file
    size_bytes: int = 0


def default_models_dir() -> Path:
    env = os.environ.get("OLLAMA_MODELS")
    if env:
        return Path(env)
    return Path.home() / ".ollama" / "models"


def candidate_models_dirs() -> list[Path]:
    """All sensible places to look for an existing Ollama models tree."""
    cands: list[Path] = []
    env = os.environ.get("OLLAMA_MODELS")
    if env:
        cands.append(Path(env))
    cands.append(Path.home() / ".ollama" / "models")
    if platform.system() == "Windows":
        users = Path("C:/Users")
        try:
            if users.is_dir():
                for u in users.iterdir():
                    p = u / ".ollama" / "models"
                    if p.is_dir():
                        cands.append(p)
        except OSError:
            pass
        cands.extend([
            Path("C:/Program Files/Ollama/models"),
            Path("C:/ProgramData/Ollama/models"),
            Path(os.environ.get("LOCALAPPDATA", "C:/")) / "Programs" / "Ollama" / "models",
        ])
        # Other drives
        for letter in "DEFGHIJ":
            p = Path(f"{letter}:/.ollama/models")
            try:
                if p.is_dir():
                    cands.append(p)
            except OSError:
                continue
    # De-dup, keep existing
    out: list[Path] = []
    seen: set[Path] = set()
    for c in cands:
        try:
            if c not in seen and c.is_dir():
                seen.add(c)
                out.append(c)
        except OSError:
            continue
    return out


def scan_installed_models(extra_roots: Iterable[Path] | None = None) -> list[InstalledModel]:
    """Walk all candidate Ollama models dirs and return everything found."""
    roots = list(candidate_models_dirs())
    if extra_roots:
        for r in extra_roots:
            p = Path(r)
            try:
                if p.is_dir() and p not in roots:
                    roots.append(p)
            except OSError:
                continue

    found: list[InstalledModel] = []
    seen: set[str] = set()
    for root in roots:
        manifests = root / "manifests"
        if not manifests.is_dir():
            continue
        # Structure: manifests/<registry>/<namespace>/<model>/<tag>
        # where <tag> is a FILE.
        for tag_file in manifests.rglob("*"):
            try:
                if not tag_file.is_file():
                    continue
            except OSError:
                continue
            parts = tag_file.relative_to(manifests).parts
            if len(parts) < 4:
                continue
            _registry, namespace, model, tag = parts[0], parts[1], parts[2], "/".join(parts[3:])
            if namespace == "library":
                name = f"{model}:{tag}"
            else:
                name = f"{namespace}/{model}:{tag}"
            key = f"{root}::{name}"
            if key in seen:
                continue
            seen.add(key)
            size = 0
            try:
                with open(tag_file, "r", encoding="utf-8") as fh:
                    manifest = json.load(fh)
                for layer in manifest.get("layers", []):
                    size += int(layer.get("size", 0))
            except (OSError, json.JSONDecodeError, ValueError):
                pass
            found.append(InstalledModel(
                name=name, namespace=namespace, path=tag_file, size_bytes=size,
            ))
    return found


# ---------------------------------------------------------------------------
# Direct downloader
# ---------------------------------------------------------------------------

REGISTRY = "https://registry.ollama.ai"
MANIFEST_ACCEPT = "application/vnd.docker.distribution.manifest.v2+json"


@dataclass
class DownloadProgress:
    phase: str          # "manifest" | "blob" | "done"
    blob_index: int = 0
    blob_total: int = 0
    blob_digest: str = ""
    bytes_done: int = 0
    bytes_total: int = 0
    overall_pct: int = 0
    message: str = ""


ProgressCb = Callable[[DownloadProgress], None]


def parse_model_ref(ref: str) -> tuple[str, str, str]:
    """Parse e.g. 'llama3.2-vision:11b' → (namespace, model, tag).

    Custom namespace: 'huihui/foo:8b' → ('huihui', 'foo', '8b').
    """
    namespace = "library"
    if "/" in ref:
        namespace, ref = ref.split("/", 1)
    if ":" in ref:
        model, tag = ref.rsplit(":", 1)
    else:
        model, tag = ref, "latest"
    return namespace, model, tag


def download_model_direct(
    model_ref: str,
    dest_models_dir: Path | None,
    progress_cb: ProgressCb,
) -> None:
    """Download an Ollama model directly from registry.ollama.ai.

    Writes the manifest to
        <dest>/manifests/registry.ollama.ai/<ns>/<model>/<tag>
    and each blob to
        <dest>/blobs/sha256-<HEX>
    matching Ollama's on-disk layout.
    """
    namespace, model, tag = parse_model_ref(model_ref)
    dest = Path(dest_models_dir) if dest_models_dir else default_models_dir()
    blobs_dir = dest / "blobs"
    manifest_dir = dest / "manifests" / "registry.ollama.ai" / namespace / model
    blobs_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    # 1. Fetch the manifest
    progress_cb(DownloadProgress(
        phase="manifest", message=f"Fetching manifest for {model}:{tag}…"
    ))
    manifest_url = f"{REGISTRY}/v2/{namespace}/{model}/manifests/{tag}"
    req = urllib.request.Request(manifest_url, headers={"Accept": MANIFEST_ACCEPT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        manifest_bytes = resp.read()
    manifest = json.loads(manifest_bytes.decode("utf-8"))

    # Save manifest exactly as bytes received
    (manifest_dir / tag).write_bytes(manifest_bytes)

    # Collect blobs (config + layers)
    blobs: list[dict] = []
    if "config" in manifest and "digest" in manifest["config"]:
        blobs.append(manifest["config"])
    blobs.extend(manifest.get("layers", []))
    total_layers = len(blobs)
    total_bytes = sum(int(b.get("size", 0)) for b in blobs)
    bytes_done_global = 0

    for i, blob in enumerate(blobs, 1):
        digest = blob.get("digest", "")  # "sha256:HEX"
        if not digest.startswith("sha256:"):
            continue
        blob_filename = "sha256-" + digest[len("sha256:"):]
        blob_path = blobs_dir / blob_filename
        size = int(blob.get("size", 0))

        # Skip if already present and matches expected size
        if blob_path.exists() and blob_path.stat().st_size == size and size > 0:
            bytes_done_global += size
            progress_cb(DownloadProgress(
                phase="blob",
                blob_index=i, blob_total=total_layers,
                blob_digest=digest, bytes_done=size, bytes_total=size,
                overall_pct=int(bytes_done_global / max(total_bytes, 1) * 100),
                message=f"Already have layer {i}/{total_layers} ({_human(size)})",
            ))
            continue

        blob_url = f"{REGISTRY}/v2/{namespace}/{model}/blobs/{digest}"
        tmp = blob_path.with_suffix(".partial")
        try:
            with urllib.request.urlopen(blob_url, timeout=60) as resp, open(tmp, "wb") as fh:
                bytes_done_blob = 0
                while True:
                    chunk = resp.read(1024 * 256)
                    if not chunk:
                        break
                    fh.write(chunk)
                    bytes_done_blob += len(chunk)
                    bytes_done_global += len(chunk)
                    progress_cb(DownloadProgress(
                        phase="blob",
                        blob_index=i, blob_total=total_layers,
                        blob_digest=digest,
                        bytes_done=bytes_done_blob, bytes_total=size,
                        overall_pct=int(bytes_done_global / max(total_bytes, 1) * 100),
                        message=(
                            f"Layer {i}/{total_layers}  "
                            f"{_human(bytes_done_blob)} / {_human(size)}"
                        ),
                    ))
            tmp.rename(blob_path)
        except Exception:
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
            raise

    progress_cb(DownloadProgress(
        phase="done", overall_pct=100,
        message=f"✓ {model}:{tag} downloaded ({_human(total_bytes)}).",
    ))


def _human(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    f = float(n)
    for u in units:
        if f < 1024:
            return f"{f:.1f} {u}"
        f /= 1024
    return f"{f:.1f} PB"
