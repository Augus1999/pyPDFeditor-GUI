# -*- coding: utf-8 -*-
"""Distilmark main application — modern PyQt6 GUI."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap, QPainter, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QFrame,
    QGroupBox,
    QFormLayout,
    QCheckBox,
    QPlainTextEdit,
    QProgressBar,
    QStatusBar,
    QMessageBox,
    QSizePolicy,
    QScrollArea,
    QSplitter,
    QSpinBox,
    QTabWidget,
    QTextBrowser,
    QTreeWidget,
    QTreeWidgetItem,
    QInputDialog,
    QHeaderView,
)

from . import config, converters, styles, ollama_manager, exporters, projects
from ._version import __version__


# Inputs accepted by PyMuPDF (most natively) + DOCX (lightweight pre-convert path).
SUPPORTED_INPUT_EXTS = {
    ".pdf", ".xps", ".oxps", ".epub", ".fb2", ".cbz",
    ".svg", ".txt", ".docx", ".png", ".jpg", ".jpeg",
}

# Per-item data roles for the queue list.
_ROLE_ENGINE = Qt.ItemDataRole.UserRole + 1
_ROLE_SCANNED = Qt.ItemDataRole.UserRole + 2


# ---------------------------------------------------------------------------
# Worker: PDF → Markdown conversion
# ---------------------------------------------------------------------------

def _parse_page_range(cfg: dict) -> tuple[int, int] | None:
    f = str(cfg.get("page_range_from", "")).strip()
    t = str(cfg.get("page_range_to", "")).strip()
    if not f and not t:
        return None
    try:
        start = int(f) if f else 1
        end = int(t) if t else 0  # 0 → open-ended (handled by converters)
    except ValueError:
        return None
    return (start, end)


def _maybe_preconvert_to_pdf(src: Path) -> Path:
    """For input formats PyMuPDF can't open natively (currently .docx), try to
    pre-convert to PDF with Pandoc. Returns the PDF path if it succeeds, or the
    original ``src`` so the caller still gets a useful error.
    """
    if src.suffix.lower() != ".docx":
        return src
    import shutil, subprocess, tempfile
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return src
    out = Path(tempfile.gettempdir()) / f"{src.stem}.pdf"
    try:
        subprocess.run([pandoc, str(src), "-o", str(out)],
                       check=True, capture_output=True)
        return out
    except Exception:
        return src


def _build_opts(cfg: dict, image_dir, image_dir_name, cancel_check, stream_cb=None) -> "converters.ConvertOptions":
    table_settings = {
        "vertical_strategy": cfg.get("plumber_vertical_strategy", "lines"),
        "horizontal_strategy": cfg.get("plumber_horizontal_strategy", "lines"),
        "snap_tolerance": int(cfg.get("plumber_snap_tolerance", 3)),
    }
    return converters.ConvertOptions(
        include_images=cfg.get("include_images", True),
        page_separator=cfg.get("page_separator", True),
        image_dir=image_dir,
        image_dir_name=image_dir_name,
        page_range=_parse_page_range(cfg),
        ocr_enabled=cfg.get("ocr_enabled", False),
        ocr_language=cfg.get("ocr_language", "eng") or "eng",
        pp_merge_hyphens=cfg.get("pp_merge_hyphens", False),
        pp_collapse_blanks=cfg.get("pp_collapse_blanks", False),
        pp_strip_headers_footers=cfg.get("pp_strip_headers_footers", False),
        plumber_tables_enabled=cfg.get("plumber_tables_enabled", True),
        plumber_table_settings=table_settings,
        llm_concurrency=int(cfg.get("llm_concurrency", 1) or 1),
        cancel_check=cancel_check,
        custom_prompt=cfg.get("custom_prompt", "") or None,
        math_mode=cfg.get("math_mode", False),
        stream_cb=stream_cb,
    )


class ConvertWorker(QThread):
    progress = pyqtSignal(int, int, str)
    stream = pyqtSignal(str, int, str)            # (pdf, page_idx, partial_text)
    finished_ok = pyqtSignal(str, str, int)       # (markdown, source_pdf, page_count)
    finished_compare = pyqtSignal(str, str, str, int)  # (md_native, md_pdfplumber, source_pdf, page_count)
    failed = pyqtSignal(str, str)                 # (source_pdf, error)
    cancelled = pyqtSignal(str)                   # (source_pdf)

    def __init__(self, pdf: Path, cfg: dict, image_dir: Path | None, image_dir_name: str | None):
        super().__init__()
        self.pdf = pdf
        self.cfg = cfg
        self.image_dir = image_dir
        self.image_dir_name = image_dir_name
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        try:
            # PyMuPDF handles many formats besides .pdf; for inputs it can't open
            # (e.g. .docx) we transparently pre-convert to PDF using Pandoc.
            src = self.pdf
            self.pdf = _maybe_preconvert_to_pdf(self.pdf)
            import pymupdf as _mupdf
            _doc = _mupdf.open(self.pdf)
            page_count = _doc.page_count
            _doc.close()

            stream_cb = None
            engine_name = self.cfg.get("engine", "native")
            if self.cfg.get("stream_output", False) and engine_name in {"ollama", "openai", "anthropic", "openai_compatible"}:
                stream_cb = lambda idx, txt, _src=str(src): self.stream.emit(_src, idx, txt)

            opts = _build_opts(
                self.cfg, self.image_dir, self.image_dir_name,
                lambda: self._cancelled, stream_cb=stream_cb,
            )
            cb = lambda c, t, m: self.progress.emit(c, t, m)
            engine = engine_name

            if engine == "native":
                md = converters.convert_native(self.pdf, opts, cb)
            elif engine == "pdfplumber":
                md = converters.convert_pdfplumber(self.pdf, opts, cb)
            elif engine == "ollama":
                md = converters.convert_ollama(
                    self.pdf, self.cfg["ollama_url"], self.cfg["ollama_model"], opts, cb
                )
            elif engine == "openai":
                md = converters.convert_openai_compatible(
                    self.pdf, self.cfg["openai_base_url"],
                    self.cfg["openai_api_key"], self.cfg["openai_model"], opts, cb,
                )
            elif engine == "anthropic":
                md = converters.convert_anthropic(
                    self.pdf, self.cfg["anthropic_api_key"],
                    self.cfg["anthropic_model"], opts, cb,
                )
            elif engine == "openai_compatible":
                md = converters.convert_openai_compatible(
                    self.pdf, self.cfg["compat_base_url"],
                    self.cfg["compat_api_key"], self.cfg["compat_model"], opts, cb,
                )
            elif engine == "compare":
                def _prog_native(c, t, m):
                    self.progress.emit(c, t * 2, f"[native] {m}")
                def _prog_plumber(c, t, m):
                    self.progress.emit(t + c, t * 2, f"[pdfplumber] {m}")
                md_native = converters.convert_native(self.pdf, opts, _prog_native)
                md_pdfplumber = converters.convert_pdfplumber(self.pdf, opts, _prog_plumber)
                self.finished_compare.emit(md_native, md_pdfplumber, str(self.pdf), page_count)
                return
            else:
                raise ValueError(f"Unknown engine: {engine}")

            self.finished_ok.emit(md, str(self.pdf), page_count)
        except converters.CancelledError:
            self.cancelled.emit(str(self.pdf))
        except Exception:
            self.failed.emit(str(self.pdf), traceback.format_exc())


# ---------------------------------------------------------------------------
# Worker: Ollama model pull (download)
# ---------------------------------------------------------------------------

class PullWorker(QThread):
    """Direct downloader — pulls blobs from registry.ollama.ai, no daemon needed."""
    progress_update = pyqtSignal(object)  # DownloadProgress
    finished_ok = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, model_ref: str, dest_dir: Path | None):
        super().__init__()
        self.model_ref = model_ref
        self.dest_dir = dest_dir

    def run(self) -> None:
        try:
            ollama_manager.download_model_direct(
                self.model_ref,
                self.dest_dir,
                lambda p: self.progress_update.emit(p),
            )
            self.finished_ok.emit()
        except Exception:
            self.failed.emit(traceback.format_exc())


class ScanWorker(QThread):
    """Background filesystem scan for installed Ollama models."""
    done = pyqtSignal(list)

    def __init__(self, extra_roots: list[Path]):
        super().__init__()
        self.extra_roots = extra_roots

    def run(self) -> None:
        try:
            results = ollama_manager.scan_installed_models(self.extra_roots)
        except Exception:
            results = []
        self.done.emit(results)


# ---------------------------------------------------------------------------
# Helpers: drawn vector icons (no emoji — scalable, theme-controlled)
# ---------------------------------------------------------------------------

from PyQt6.QtCore import QRectF  # noqa: E402
from PyQt6.QtGui import QPen, QPainterPath  # noqa: E402


def _icon_add(color: str = "#2563eb") -> QIcon:
    """A document with a plus badge — 'add PDFs'."""
    pm = QPixmap(28, 28)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), 2.0)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawRoundedRect(QRectF(6, 4, 12, 16), 2, 2)        # page
    p.drawLine(15, 10, 22, 10)                            # plus badge
    p.drawLine(15, 10, 15, 10)
    pen2 = QPen(QColor(color), 2.2)
    p.setPen(pen2)
    p.drawLine(20, 14, 20, 22)                            # +
    p.drawLine(16, 18, 24, 18)
    p.end()
    return QIcon(pm)


def _brand_mark(size: int = 26) -> QPixmap:
    """Distilmark logo mark: a blue rounded tile with an orange distillation droplet."""
    import math
    ss = 4  # supersample for crisp edges
    s = size * ss
    pm = QPixmap(s, s)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor("#2563eb"))
    p.drawRoundedRect(QRectF(0, 0, s, s), s * 0.24, s * 0.24)
    # parametric teardrop, point up (matches icon.png)
    cx, cy, sx, sy, m = s * 0.5, s * 0.52, s * 0.30, s * 0.30, 3.0
    drop = QPainterPath()
    for i in range(241):
        t = 2 * math.pi * i / 240
        u = math.cos(t)
        v = math.sin(t) * (math.sin(t / 2) ** m)
        px, py = cx + sx * v, cy - sy * u
        drop.moveTo(px, py) if i == 0 else drop.lineTo(px, py)
    drop.closeSubpath()
    p.setBrush(QColor("#f97316"))
    p.drawPath(drop)
    p.end()
    return pm.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                     Qt.TransformationMode.SmoothTransformation)


def _icon_folder(color: str = "#f97316") -> QIcon:
    """A folder outline — 'add folder'."""
    pm = QPixmap(28, 28)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(QPen(QColor(color), 2.0))
    path = QPainterPath()
    path.moveTo(4, 8)
    path.lineTo(11, 8)
    path.lineTo(13, 11)
    path.lineTo(24, 11)
    path.lineTo(24, 22)
    path.lineTo(4, 22)
    path.closeSubpath()
    p.drawPath(path)
    p.end()
    return QIcon(pm)


# ---------------------------------------------------------------------------
# Convert page
# ---------------------------------------------------------------------------

class ConvertPage(QWidget):
    conversion_done = pyqtSignal()  # notify History tab
    preview_ready = pyqtSignal(dict)   # push last result to Preview tab
    stream_chunk = pyqtSignal(str, int, str)   # forward live LLM stream
    stream_started = pyqtSignal(str)   # forward "starting LLM streaming for X"

    def __init__(self, cfg: dict, status: QStatusBar, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.status = status
        self.queue: list[Path] = []
        self.worker: ConvertWorker | None = None
        self._out_dir: Path = Path(cfg.get("last_output_dir", str(Path.home())))
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("Convert")
        title.setObjectName("H1")
        layout.addWidget(title)

        subtitle = QLabel("Drop files or a folder, choose an engine, and distil to Markdown.")
        subtitle.setObjectName("H2")
        layout.addWidget(subtitle)

        # File / folder picker row
        file_row = QHBoxLayout()
        self.pick_btn = QPushButton(" Add PDFs")
        self.pick_btn.setIcon(_icon_add("#2563eb"))
        self.pick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pick_btn.clicked.connect(self.pick_files)

        self.folder_btn = QPushButton(" Add Folder")
        self.folder_btn.setIcon(_icon_folder("#f97316"))
        self.folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.folder_btn.clicked.connect(self.pick_folder)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("Ghost")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_queue)

        file_row.addWidget(self.pick_btn)
        file_row.addWidget(self.folder_btn)
        file_row.addWidget(self.clear_btn)
        file_row.addStretch()
        layout.addLayout(file_row)

        self.list = QListWidget()
        self.list.setAcceptDrops(True)
        self.list.setMinimumHeight(150)
        self.list.setMaximumHeight(260)
        from PyQt6.QtWidgets import QAbstractItemView
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self._queue_context_menu)
        self.list.setToolTip(
            "• Drag to reorder · double-click to open · Delete to remove\n"
            "• Right-click for per-file engine override and other actions"
        )
        self.setAcceptDrops(True)
        layout.addWidget(self.list)

        self.queue_label = QLabel("Drag PDF files or a folder here to get started.")
        self.queue_label.setObjectName("Hint")
        layout.addWidget(self.queue_label)

        # Engine + options
        opts_box = QGroupBox("Conversion options")
        opts_layout = QFormLayout(opts_box)

        self.engine_combo = QComboBox()
        self.engine_combo.addItem("Native — offline · PyMuPDF", "native")
        self.engine_combo.addItem("pdfplumber — offline · layout + tables", "pdfplumber")
        self.engine_combo.addItem("Compare — native + pdfplumber (two files)", "compare")
        self.engine_combo.addItem("Ollama — local LLM", "ollama")
        self.engine_combo.addItem("OpenAI", "openai")
        self.engine_combo.addItem("Anthropic Claude", "anthropic")
        self.engine_combo.addItem("OpenAI-compatible — Groq · OpenRouter · LM Studio", "openai_compatible")
        self.engine_combo.setToolTip(
            "Choose the back-end that turns your PDF into Markdown.\n"
            "Offline engines run locally and are free; hosted engines call an API."
        )
        cur = self.cfg.get("engine", "native")
        for i in range(self.engine_combo.count()):
            if self.engine_combo.itemData(i) == cur:
                self.engine_combo.setCurrentIndex(i)
                break
        opts_layout.addRow("Engine:", self.engine_combo)

        self.images_cb = QCheckBox("Extract embedded images")
        self.images_cb.setChecked(self.cfg.get("include_images", True))
        self.images_cb.setToolTip(
            "Save embedded images from the PDF into a sibling folder named "
            "<stem>_images/ and reference them with relative paths in the "
            "Markdown, so previews work in VS Code, Obsidian, Typora, etc."
        )
        opts_layout.addRow("", self.images_cb)

        self.sep_cb = QCheckBox("Insert --- between pages")
        self.sep_cb.setChecked(self.cfg.get("page_separator", True))
        self.sep_cb.setToolTip(
            "Insert a Markdown horizontal-rule (---) between pages, making "
            "page boundaries easy to spot in the output."
        )
        opts_layout.addRow("", self.sep_cb)

        # Page range row
        range_row = QHBoxLayout()
        self.range_from = QLineEdit(str(self.cfg.get("page_range_from", "")))
        self.range_from.setPlaceholderText("first")
        self.range_from.setFixedWidth(70)
        self.range_from.setToolTip(
            "First page to convert (1-based). Leave blank to start from page 1."
        )
        self.range_to = QLineEdit(str(self.cfg.get("page_range_to", "")))
        self.range_to.setPlaceholderText("last")
        self.range_to.setFixedWidth(70)
        self.range_to.setToolTip(
            "Last page to convert (1-based, inclusive). Leave blank to go to the "
            "end of the document."
        )
        range_row.addWidget(QLabel("From"))
        range_row.addWidget(self.range_from)
        range_row.addWidget(QLabel("to"))
        range_row.addWidget(self.range_to)
        range_row.addWidget(QLabel("(blank = all pages)"))
        range_row.addStretch()
        opts_layout.addRow("Page range:", range_row)

        layout.addWidget(opts_box)

        # ---- Advanced options (collapsible) ----
        self.adv_toggle = QPushButton("Advanced options  ▾")
        self.adv_toggle.setCheckable(True)
        self.adv_toggle.setObjectName("NavItem")
        self.adv_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.adv_toggle.toggled.connect(self._toggle_advanced)
        layout.addWidget(self.adv_toggle)
        self.adv_box = self._build_advanced()
        self.adv_box.setVisible(False)
        layout.addWidget(self.adv_box)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.progress_label = QLabel("")
        self.progress_label.setObjectName("Hint")
        layout.addWidget(self.progress_label)

        action_row = QHBoxLayout()
        self.estimate_btn = QPushButton("Estimate cost")
        self.estimate_btn.setObjectName("Ghost")
        self.estimate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.estimate_btn.setToolTip(
            "Estimate the rough USD cost for hosted LLM engines "
            "(OpenAI, Anthropic, OpenAI-compatible) before converting. "
            "Free for offline engines."
        )
        self.estimate_btn.clicked.connect(self._estimate_cost)
        self.cancel_conv_btn = QPushButton("Cancel")
        self.cancel_conv_btn.setObjectName("Danger")
        self.cancel_conv_btn.setEnabled(False)
        self.cancel_conv_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_conv_btn.setToolTip(
            "Stop the current batch. The page in progress finishes first, "
            "remaining queued files are skipped."
        )
        self.cancel_conv_btn.clicked.connect(self._cancel_conversion)
        self.convert_btn = QPushButton("Convert  →")
        self.convert_btn.setObjectName("Primary")
        self.convert_btn.setMinimumHeight(40)
        self.convert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convert_btn.setToolTip("Start converting every PDF in the queue.")
        self.convert_btn.clicked.connect(self.start_conversion)
        action_row.addWidget(self.estimate_btn)
        action_row.addStretch()
        action_row.addWidget(self.cancel_conv_btn)
        action_row.addWidget(self.convert_btn)
        layout.addLayout(action_row)

        # ---- Quick actions (after a conversion) ----
        self.quick_actions = self._build_quick_actions()
        self.quick_actions.setVisible(False)
        layout.addWidget(self.quick_actions)

        scroll.setWidget(inner)
        outer.addWidget(scroll)

        # ---- Keyboard shortcuts ----
        from PyQt6.QtGui import QShortcut, QKeySequence
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.pick_files)
        QShortcut(QKeySequence("Ctrl+Shift+O"), self, activated=self.pick_folder)
        QShortcut(QKeySequence("Ctrl+Return"), self, activated=self.start_conversion)
        QShortcut(QKeySequence("Ctrl+Enter"), self, activated=self.start_conversion)
        QShortcut(QKeySequence("Escape"), self, activated=self._cancel_conversion)

    def _build_quick_actions(self) -> QWidget:
        box = QGroupBox("Last result")
        row = QHBoxLayout(box)
        self.open_folder_btn = QPushButton("📂 Open output folder")
        self.open_folder_btn.setObjectName("Ghost")
        self.open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_folder_btn.clicked.connect(
            lambda: self._open_in_file_browser(self._out_dir)
        )

        self.copy_md_btn = QPushButton("Copy Markdown")
        self.copy_md_btn.setObjectName("Ghost")
        self.copy_md_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_md_btn.clicked.connect(self._copy_last_markdown)

        self.export_html_btn = QPushButton("Export HTML")
        self.export_html_btn.setObjectName("Ghost")
        self.export_html_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_html_btn.clicked.connect(lambda: self._export("html"))

        self.export_docx_btn = QPushButton("Export DOCX")
        self.export_docx_btn.setObjectName("Ghost")
        self.export_docx_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_docx_btn.clicked.connect(lambda: self._export("docx"))

        self.combine_btn = QPushButton("Combine all → one .md")
        self.combine_btn.setObjectName("Ghost")
        self.combine_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combine_btn.clicked.connect(self._combine_outputs)

        self.obsidian_btn = QPushButton("Open in Obsidian")
        self.obsidian_btn.setObjectName("Ghost")
        self.obsidian_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.obsidian_btn.clicked.connect(self._open_in_obsidian)

        for b in (self.open_folder_btn, self.copy_md_btn,
                  self.export_html_btn, self.export_docx_btn,
                  self.combine_btn, self.obsidian_btn):
            row.addWidget(b)
        row.addStretch()
        return box

    def _show_quick_actions(self):
        if self._outputs_for_quick_actions:
            self.quick_actions.setVisible(True)
            multi = len(self._outputs_for_quick_actions) > 1
            self.combine_btn.setVisible(multi)

    def _copy_last_markdown(self):
        if not self._outputs_for_quick_actions:
            return
        from PyQt6.QtWidgets import QApplication
        try:
            text = self._outputs_for_quick_actions[-1].read_text(encoding="utf-8")
        except OSError as e:
            self.status.showMessage(f"Copy failed: {e}", 4000)
            return
        QApplication.clipboard().setText(text)
        self.status.showMessage("✓ Markdown copied to clipboard", 3000)

    def _export(self, fmt: str):
        if not self._outputs_for_quick_actions:
            return
        src = self._outputs_for_quick_actions[-1]
        try:
            md = src.read_text(encoding="utf-8")
        except OSError as e:
            QMessageBox.critical(self, "Export", f"Could not read {src}\n\n{e}"); return
        target = src.with_suffix("." + fmt)
        try:
            if fmt == "html":
                exporters.to_html(md, target)
            elif fmt == "docx":
                exporters.to_docx(md, target, md_source=src)
        except Exception as e:
            QMessageBox.critical(self, "Export failed", f"{fmt.upper()} export failed:\n\n{e}")
            return
        self.status.showMessage(f"✓ Exported → {target.name}", 4000)
        self._open_in_file_browser(target)

    def _combine_outputs(self):
        if len(self._outputs_for_quick_actions) < 2:
            return
        target = self._out_dir / "combined.md"
        try:
            exporters.combine_markdown(self._outputs_for_quick_actions, target)
        except Exception as e:
            QMessageBox.critical(self, "Combine failed", str(e)); return
        self.status.showMessage(f"✓ Combined → {target.name}", 4000)
        self._open_in_file_browser(target)

    def _open_in_obsidian(self):
        if not self._outputs_for_quick_actions:
            return
        from PyQt6.QtGui import QDesktopServices
        last = self._outputs_for_quick_actions[-1]
        # Obsidian URI: open vault file by absolute path
        url = QUrl(f"obsidian://open?path={last}")
        if not QDesktopServices.openUrl(url):
            QMessageBox.information(
                self, "Obsidian",
                "Could not launch Obsidian via the obsidian:// URL.\n\n"
                "Make sure Obsidian is installed and that the file is inside "
                "a vault.\n\nFile path:\n" + str(last),
            )

    def _build_advanced(self) -> QWidget:
        box = QGroupBox("")
        form = QFormLayout(box)

        # ---- OCR ----
        self.ocr_cb = QCheckBox("Enable OCR fallback for scanned pages")
        self.ocr_cb.setChecked(self.cfg.get("ocr_enabled", False))
        self.ocr_cb.setToolTip(
            "When a page has no extractable text (a scanned image or a photo of a "
            "document), run it through Tesseract OCR to recover the text.\n\n"
            "Requires Tesseract installed on your system — use the\n"
            "“Install Tesseract” button on the right for guidance."
        )
        ocr_row = QHBoxLayout()
        ocr_row.addWidget(self.ocr_cb, 1)
        self.tesseract_btn = QPushButton("Install Tesseract ↗")
        self.tesseract_btn.setObjectName("Ghost")
        self.tesseract_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tesseract_btn.setToolTip(
            "Open the Tesseract installation guide in your browser."
        )
        self.tesseract_btn.clicked.connect(self._show_tesseract_help)
        ocr_row.addWidget(self.tesseract_btn)
        form.addRow("OCR:", ocr_row)

        self.ocr_lang = QLineEdit(self.cfg.get("ocr_language", "eng"))
        self.ocr_lang.setPlaceholderText("eng, fas, eng+fas, …")
        self.ocr_lang.setFixedWidth(180)
        self.ocr_lang.setToolTip(
            "Tesseract language code(s). Examples:\n"
            "  eng        — English (default)\n"
            "  fas        — Persian / Farsi\n"
            "  eng+fas    — both, combined\n"
            "  deu, jpn, chi_sim, ara, rus  — other languages\n\n"
            "Each language needs its data pack installed alongside Tesseract."
        )
        form.addRow("OCR language:", self.ocr_lang)

        # ---- Post-processing ----
        self.pp_hyphen_cb = QCheckBox("Merge hyphenated line breaks")
        self.pp_hyphen_cb.setChecked(self.cfg.get("pp_merge_hyphens", False))
        self.pp_hyphen_cb.setToolTip(
            "Re-join words split across line breaks with a hyphen.\n"
            "Example:  “exam-\\nple” → “example”.\n"
            "Useful for two-column papers and PDFs with tight line wrapping."
        )
        form.addRow("Clean-up:", self.pp_hyphen_cb)

        self.pp_blanks_cb = QCheckBox("Collapse multiple blank lines")
        self.pp_blanks_cb.setChecked(self.cfg.get("pp_collapse_blanks", False))
        self.pp_blanks_cb.setToolTip(
            "Replace runs of 3+ consecutive blank lines with a single blank line, "
            "for a tidier Markdown output."
        )
        form.addRow("", self.pp_blanks_cb)

        self.pp_hf_cb = QCheckBox("Strip repeating headers / footers / page numbers")
        self.pp_hf_cb.setChecked(self.cfg.get("pp_strip_headers_footers", False))
        self.pp_hf_cb.setToolTip(
            "Detect the first/last line of each page; when the same text repeats "
            "across most pages (a running header, footer, or page number), drop "
            "it from the output. Needs at least 3 pages."
        )
        form.addRow("", self.pp_hf_cb)

        # ---- pdfplumber table tuning ----
        self.tables_cb = QCheckBox("Extract tables (pdfplumber engine)")
        self.tables_cb.setChecked(self.cfg.get("plumber_tables_enabled", True))
        self.tables_cb.setToolTip(
            "When using the pdfplumber engine, detect tables on each page and "
            "convert them to GitHub-flavored Markdown tables.\n"
            "Disable if pdfplumber is mistakenly turning paragraphs into tables."
        )
        form.addRow("Tables:", self.tables_cb)

        self.vstrat = QComboBox()
        self.vstrat.addItems(["lines", "text", "lines_strict"])
        self.vstrat.setCurrentText(self.cfg.get("plumber_vertical_strategy", "lines"))
        self.vstrat.setToolTip(
            "How pdfplumber finds column boundaries inside a table:\n"
            "  lines         — use ruled vertical lines (best for bordered tables)\n"
            "  text          — infer from column-aligned text (best for borderless)\n"
            "  lines_strict  — require explicit lines (avoids false positives)"
        )
        form.addRow("Table vertical strategy:", self.vstrat)

        self.hstrat = QComboBox()
        self.hstrat.addItems(["lines", "text", "lines_strict"])
        self.hstrat.setCurrentText(self.cfg.get("plumber_horizontal_strategy", "lines"))
        self.hstrat.setToolTip(
            "How pdfplumber finds row boundaries inside a table. Same options as "
            "the vertical strategy above. Default ‘lines’ works for most ruled "
            "tables; switch to ‘text’ for tables with no visible row separators."
        )
        form.addRow("Table horizontal strategy:", self.hstrat)

        self.snap = QSpinBox()
        self.snap.setRange(0, 50)
        self.snap.setValue(int(self.cfg.get("plumber_snap_tolerance", 3)))
        self.snap.setToolTip(
            "Pixel distance within which pdfplumber merges nearby table edges. "
            "Lower (1–2) = stricter, more tables found but more false splits. "
            "Higher (5–10) = lenient, joins wobbly cell borders. Default: 3."
        )
        form.addRow("Table snap tolerance:", self.snap)

        # ---- Math mode (LLM engines) ----
        self.math_cb = QCheckBox("Preserve math formulas (LaTeX)")
        self.math_cb.setChecked(self.cfg.get("math_mode", False))
        self.math_cb.setToolTip(
            "When using an LLM engine, instruct the model to wrap inline math "
            "with $…$ and display equations with $$…$$ — and to use proper "
            "LaTeX notation. Useful for academic papers, lecture notes, and "
            "anything with equations."
        )
        form.addRow("Math:", self.math_cb)

        # ---- Streaming output ----
        self.stream_cb_w = QCheckBox("Stream live tokens into Preview")
        self.stream_cb_w.setChecked(self.cfg.get("stream_output", False))
        self.stream_cb_w.setToolTip(
            "For LLM engines, show Markdown appearing token-by-token in the "
            "Preview tab as the model generates it, instead of waiting for "
            "each page to complete. (Provider may not support streaming.)"
        )
        form.addRow("Streaming:", self.stream_cb_w)

        # ---- Auto-open output folder ----
        self.auto_open_cb = QCheckBox("Open the output folder when a batch finishes")
        self.auto_open_cb.setChecked(self.cfg.get("auto_open_output", False))
        self.auto_open_cb.setToolTip(
            "Automatically open the output folder in your file browser the "
            "moment a batch conversion completes."
        )
        form.addRow("After convert:", self.auto_open_cb)

        # ---- LLM concurrency ----
        self.concurrency = QSpinBox()
        self.concurrency.setRange(1, 16)
        self.concurrency.setValue(int(self.cfg.get("llm_concurrency", 1)))
        self.concurrency.setToolTip(
            "How many pages to process in parallel for hosted LLM engines\n"
            "(OpenAI, Anthropic, OpenAI-compatible).\n\n"
            "  1   = sequential, safest\n"
            "  4   = ~4× faster on most providers\n"
            "  8+  = may hit provider rate limits — back off if requests fail"
        )
        form.addRow("LLM parallel pages:", self.concurrency)

        return box

    def _show_tesseract_help(self):
        from PyQt6.QtGui import QDesktopServices
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Install Tesseract for OCR")
        box.setTextFormat(Qt.TextFormat.RichText)
        box.setText(
            "<b>Tesseract</b> is the OCR engine that turns scanned/image-only PDF "
            "pages into searchable text. Install it once on your system, then "
            "enable OCR fallback here."
        )
        box.setInformativeText(
            "<b>Windows</b><br>"
            "Download the official installer:<br>"
            "&nbsp;&nbsp;<a href='https://github.com/UB-Mannheim/tesseract/wiki'>"
            "github.com/UB-Mannheim/tesseract/wiki</a><br>"
            "During install, tick extra <b>language packs</b> you need "
            "(e.g. Persian = <code>fas</code>).<br><br>"
            "<b>macOS</b> &nbsp; <code>brew install tesseract tesseract-lang</code><br>"
            "<b>Ubuntu / Debian</b> &nbsp; <code>sudo apt install tesseract-ocr tesseract-ocr-fas</code><br>"
            "<b>Fedora</b> &nbsp; <code>sudo dnf install tesseract tesseract-langpack-fas</code><br><br>"
            "<a href='https://tesseract-ocr.github.io/tessdoc/Installation.html'>"
            "Full installation docs ↗</a>"
        )
        open_btn = box.addButton("Open Tesseract site", QMessageBox.ButtonRole.AcceptRole)
        box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        box.exec()
        if box.clickedButton() is open_btn:
            QDesktopServices.openUrl(
                QUrl("https://tesseract-ocr.github.io/tessdoc/Installation.html")
            )

    def _toggle_advanced(self, checked: bool):
        self.adv_box.setVisible(checked)
        self.adv_toggle.setText("Advanced options  ▴" if checked else "Advanced options  ▾")

    # ---- drag & drop ----
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            p = Path(url.toLocalFile())
            if p.is_dir():
                self._scan_folder(p)
            elif p.suffix.lower() in SUPPORTED_INPUT_EXTS and p.exists():
                self._add(p)

    def _add(self, p: Path):
        if p in self.queue:
            return
        self.queue.append(p)
        label = f"  {p.name}    —    {p.parent}"
        # Scanned-PDF heuristic (only for .pdf, cheap)
        scanned = False
        try:
            if p.suffix.lower() == ".pdf":
                scanned = converters.is_likely_scanned(p)
        except Exception:
            scanned = False
        if scanned:
            label += "    [scanned?]"
        item = QListWidgetItem(label)
        item.setData(Qt.ItemDataRole.UserRole, str(p))
        item.setData(_ROLE_ENGINE, "")  # "" = use default engine
        item.setData(_ROLE_SCANNED, scanned)
        if scanned:
            item.setForeground(QColor("#fbbf24"))
            item.setToolTip(
                "This PDF appears to contain little or no extractable text "
                "— it's likely a scan. Enable OCR in Advanced options to "
                "recover the text."
            )
        self.list.addItem(item)
        self._update_queue_label()

    def _scan_folder(self, folder: Path) -> int:
        found: set[Path] = set()
        for ext in SUPPORTED_INPUT_EXTS:
            found.update(folder.rglob(f"*{ext}"))
            found.update(folder.rglob(f"*{ext.upper()}"))
        ordered = sorted(found)
        for p in ordered:
            self._add(p)
        self._update_queue_label()
        return len(ordered)

    def _update_queue_label(self):
        n = len(self.queue)
        scanned = sum(
            1 for i in range(self.list.count())
            if self.list.item(i).data(_ROLE_SCANNED)
        )
        msg = f"{n} file{'s' if n != 1 else ''} in queue"
        if scanned:
            msg += f"   ·   {scanned} look scanned — enable OCR"
        self.queue_label.setText(msg)

    @staticmethod
    def _input_filter() -> str:
        all_pat = " ".join(f"*{e}" for e in SUPPORTED_INPUT_EXTS)
        return (
            f"All supported ({all_pat});;"
            "PDF (*.pdf);;Word (*.docx);;EPUB (*.epub);;"
            "XPS (*.xps *.oxps);;FictionBook (*.fb2);;Comic (*.cbz);;"
            "SVG (*.svg);;Text (*.txt);;Images (*.png *.jpg *.jpeg);;"
            "All files (*)"
        )

    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Pick files to convert", str(Path.home()), self._input_filter()
        )
        for f in files:
            self._add(Path(f))

    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Pick folder to scan", str(Path.home())
        )
        if folder:
            n = self._scan_folder(Path(folder))
            self.status.showMessage(f"Found {n} document(s) in folder.", 4000)

    # ---- queue: context menu + delete key ----
    def _queue_context_menu(self, pos):
        from PyQt6.QtWidgets import QMenu
        item = self.list.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        # Per-file engine override submenu
        engine_menu = menu.addMenu("Use engine for this file")
        cur_override = item.data(_ROLE_ENGINE) or ""
        for i in range(self.engine_combo.count()):
            data = self.engine_combo.itemData(i)
            text = self.engine_combo.itemText(i)
            a = engine_menu.addAction(("✓ " if data == cur_override else "  ") + text)
            a.triggered.connect(lambda _=False, d=data, it=item: self._set_item_engine(it, d))
        if cur_override:
            reset = engine_menu.addAction("Clear override (use default)")
            reset.triggered.connect(lambda: self._set_item_engine(item, ""))
        menu.addSeparator()
        open_loc = menu.addAction("Open file location")
        open_loc.triggered.connect(lambda: self._open_in_file_browser(Path(item.data(Qt.ItemDataRole.UserRole))))
        rm = menu.addAction("Remove from queue   (Del)")
        rm.triggered.connect(lambda: self._remove_item(item))
        menu.exec(self.list.mapToGlobal(pos))

    def _set_item_engine(self, item, engine: str):
        item.setData(_ROLE_ENGINE, engine or "")
        path = item.data(Qt.ItemDataRole.UserRole)
        base = f"  {Path(path).name}    —    {Path(path).parent}"
        if item.data(_ROLE_SCANNED):
            base += "    [scanned?]"
        if engine:
            base += f"    [{engine}]"
        item.setText(base)

    def _remove_item(self, item):
        row = self.list.row(item)
        if row < 0:
            return
        path_str = item.data(Qt.ItemDataRole.UserRole)
        self.list.takeItem(row)
        try:
            self.queue.remove(Path(path_str))
        except ValueError:
            pass
        self._update_queue_label()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace) and self.list.hasFocus():
            for item in self.list.selectedItems():
                self._remove_item(item)
            return
        super().keyPressEvent(event)

    @staticmethod
    def _open_in_file_browser(path: Path):
        import sys, subprocess
        target = path.parent if path.is_file() else path
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen(["explorer", "/select,", str(path)] if path.is_file() else ["explorer", str(target)])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-R", str(path)] if path.is_file() else ["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])
        except Exception:
            pass

    def clear_queue(self):
        self.queue.clear()
        self.list.clear()
        self._update_queue_label()

    # ---- conversion ----
    def _sync_cfg(self):
        self.cfg["engine"] = self.engine_combo.currentData()
        self.cfg["include_images"] = self.images_cb.isChecked()
        self.cfg["page_separator"] = self.sep_cb.isChecked()
        self.cfg["page_range_from"] = self.range_from.text().strip()
        self.cfg["page_range_to"] = self.range_to.text().strip()
        self.cfg["ocr_enabled"] = self.ocr_cb.isChecked()
        self.cfg["ocr_language"] = self.ocr_lang.text().strip() or "eng"
        self.cfg["pp_merge_hyphens"] = self.pp_hyphen_cb.isChecked()
        self.cfg["pp_collapse_blanks"] = self.pp_blanks_cb.isChecked()
        self.cfg["pp_strip_headers_footers"] = self.pp_hf_cb.isChecked()
        self.cfg["plumber_tables_enabled"] = self.tables_cb.isChecked()
        self.cfg["plumber_vertical_strategy"] = self.vstrat.currentText()
        self.cfg["plumber_horizontal_strategy"] = self.hstrat.currentText()
        self.cfg["plumber_snap_tolerance"] = self.snap.value()
        self.cfg["llm_concurrency"] = self.concurrency.value()
        self.cfg["math_mode"] = self.math_cb.isChecked()
        self.cfg["stream_output"] = self.stream_cb_w.isChecked()
        self.cfg["auto_open_output"] = self.auto_open_cb.isChecked()
        config.save(self.cfg)

    def _estimate_cost(self):
        if not self.queue:
            self.status.showMessage("Add files first to estimate cost.", 4000)
            return
        self._sync_cfg()
        engine = self.cfg.get("engine", "native")
        total_pages = sum(converters.count_pages(p) for p in self.queue)
        model = {
            "openai": self.cfg.get("openai_model", ""),
            "anthropic": self.cfg.get("anthropic_model", ""),
            "openai_compatible": self.cfg.get("compat_model", ""),
        }.get(engine, "")
        cost = converters.estimate_cost(engine, model, total_pages)
        if cost is None:
            QMessageBox.information(
                self, "Cost estimate",
                f"{total_pages} page(s) · engine '{engine}' runs locally — "
                f"no API cost. 🎉",
            )
        else:
            QMessageBox.information(
                self, "Cost estimate",
                f"{total_pages} page(s) · model '{model}'\n\n"
                f"Estimated cost: ~${cost:.2f} USD\n\n"
                f"(rough estimate — actual cost depends on page complexity "
                f"and provider pricing)",
            )

    def _cancel_conversion(self):
        self._remaining = []
        if self.worker and self.worker.isRunning():
            self.worker.cancel()
            self.status.showMessage("Cancelling…", 3000)

    def start_conversion(self):
        if not self.queue:
            self.status.showMessage("No files queued.", 4000)
            return
        if self.worker and self.worker.isRunning():
            return
        self._sync_cfg()
        out_dir = QFileDialog.getExistingDirectory(
            self, "Output folder", self.cfg.get("last_output_dir", str(Path.home()))
        )
        if not out_dir:
            return
        self.cfg["last_output_dir"] = out_dir
        config.save(self.cfg)
        self._out_dir = Path(out_dir)
        # Read the queue from the list widget so user-reordering is honored,
        # carrying per-item engine overrides alongside the path.
        self._remaining = []
        for i in range(self.list.count()):
            it = self.list.item(i)
            self._remaining.append((
                Path(it.data(Qt.ItemDataRole.UserRole)),
                it.data(_ROLE_ENGINE) or "",
            ))
        self._total_files = len(self._remaining)
        self._done_files = 0
        self._outputs_for_quick_actions: list[Path] = []
        self.convert_btn.setEnabled(False)
        self.cancel_conv_btn.setEnabled(True)
        self.quick_actions.setVisible(False)
        self._convert_next()

    def _convert_next(self):
        if not self._remaining:
            self.convert_btn.setEnabled(True)
            self.cancel_conv_btn.setEnabled(False)
            self.status.showMessage(
                f"All done — {self._done_files} file(s) converted.", 8000
            )
            self.progress.setValue(100)
            self.progress_label.setText("")
            self._show_quick_actions()
            if self.cfg.get("auto_open_output", False) and self._done_files:
                self._open_in_file_browser(self._out_dir)
            self.conversion_done.emit()
            return
        pdf, engine_override = self._remaining.pop(0)
        # Build a per-file cfg copy so the worker picks up the override
        run_cfg = dict(self.cfg)
        if engine_override:
            run_cfg["engine"] = engine_override
        img_dir_name = f"{pdf.stem}_images" if run_cfg.get("include_images") else None
        img_dir = self._out_dir / img_dir_name if img_dir_name else None
        self.worker = ConvertWorker(pdf, run_cfg, img_dir, img_dir_name)
        if run_cfg.get("stream_output", False) and run_cfg.get("engine") in {
            "ollama", "openai", "anthropic", "openai_compatible"
        }:
            self.stream_started.emit(str(pdf))
        self.worker.progress.connect(self._on_progress)
        self.worker.stream.connect(self._on_stream)
        self.worker.finished_ok.connect(self._on_done)
        self.worker.finished_compare.connect(self._on_done_compare)
        self.worker.failed.connect(self._on_failed)
        self.worker.cancelled.connect(self._on_cancelled)
        done_so_far = self._total_files - len(self._remaining) - 1
        self.progress_label.setText(
            f"File {done_so_far + 1}/{self._total_files}: {pdf.name}"
        )
        self.worker.start()

    def _on_progress(self, cur: int, total: int, msg: str):
        self.progress.setValue(int(cur / max(total, 1) * 100))
        self.status.showMessage(msg)

    def _on_done(self, md: str, src: str, pages: int):
        src_path = Path(src)
        out = self._out_dir / f"{src_path.stem}.md"
        out.write_text(md, encoding="utf-8")
        self._outputs_for_quick_actions.append(out)
        self._done_files += 1
        config.append_history({
            "source": src_path.name,
            "source_path": src,
            "output": out.name,
            "output_path": str(out),
            "engine": self.cfg.get("engine", "native"),
            "pages": pages,
            "status": "ok",
        })
        self.status.showMessage(f"✓ {src_path.name} → {out.name}", 4000)
        self.preview_ready.emit({
            "pdf": src,
            "compare": False,
            "md": md,
            "output": str(out),
        })
        self._convert_next()

    def _on_done_compare(self, md_native: str, md_pdfplumber: str, src: str, pages: int):
        src_path = Path(src)
        out_native = self._out_dir / f"{src_path.stem}_native.md"
        out_plumber = self._out_dir / f"{src_path.stem}_pdfplumber.md"
        out_native.write_text(md_native, encoding="utf-8")
        self._outputs_for_quick_actions.append(out_native)
        self._outputs_for_quick_actions.append(out_plumber)
        out_plumber.write_text(md_pdfplumber, encoding="utf-8")
        self._done_files += 1
        config.append_history({
            "source": src_path.name,
            "source_path": src,
            "output": out_native.name,
            "output_path": str(out_native),
            "engine": "native (compare)",
            "pages": pages,
            "status": "ok",
        })
        config.append_history({
            "source": src_path.name,
            "source_path": src,
            "output": out_plumber.name,
            "output_path": str(out_plumber),
            "engine": "pdfplumber (compare)",
            "pages": pages,
            "status": "ok",
        })
        self.status.showMessage(
            f"✓ {src_path.name} → {out_native.name} + {out_plumber.name}", 5000
        )
        self.preview_ready.emit({
            "pdf": src,
            "compare": True,
            "md_native": md_native,
            "md_pdfplumber": md_pdfplumber,
            "output_native": str(out_native),
            "output_pdfplumber": str(out_plumber),
        })
        self._convert_next()

    def _on_stream(self, src: str, page_idx: int, chunk: str):
        self.stream_chunk.emit(src, page_idx, chunk)

    def _on_cancelled(self, src: str):
        self._remaining = []
        self.convert_btn.setEnabled(True)
        self.cancel_conv_btn.setEnabled(False)
        self.progress.setValue(0)
        self.progress_label.setText("")
        self.status.showMessage("Conversion cancelled.", 4000)

    def _on_failed(self, src: str, err: str):
        src_path = Path(src)
        config.append_history({
            "source": src_path.name,
            "source_path": src,
            "output": "",
            "output_path": "",
            "engine": self.cfg.get("engine", "native"),
            "pages": 0,
            "status": "error",
            "error": err[:500],
        })
        QMessageBox.critical(self, "Conversion failed", f"{src_path.name}\n\n{err}")
        self._convert_next()


# ---------------------------------------------------------------------------
# Settings page
# ---------------------------------------------------------------------------

class SettingsPage(QWidget):
    settings_saved = pyqtSignal()

    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self._pull_worker: PullWorker | None = None
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Engines")
        title.setObjectName("H1")
        layout.addWidget(title)
        subtitle = QLabel("Configure offline and hosted conversion back-ends.")
        subtitle.setObjectName("H2")
        layout.addWidget(subtitle)

        # ---- Ollama ----
        olm = QGroupBox("Ollama  ·  offline, local")
        f = QFormLayout(olm)

        # Hidden state inputs used for save()
        self.ollama_url = QLineEdit(self.cfg["ollama_url"])
        self.ollama_model = QLineEdit(self.cfg["ollama_model"])

        # Service status row
        status_row = QHBoxLayout()
        self.service_label = QLabel("Checking…")
        self.service_label.setWordWrap(True)
        self.start_service_btn = QPushButton("▶ Start Ollama")
        self.start_service_btn.setVisible(False)
        self.start_service_btn.clicked.connect(self._start_service)
        recheck_btn = QPushButton("↻ Re-check")
        recheck_btn.clicked.connect(self._refresh_service_status)
        status_row.addWidget(self.service_label, 1)
        status_row.addWidget(self.start_service_btn)
        status_row.addWidget(recheck_btn)
        f.addRow("Service:", status_row)

        f.addRow("Server URL:", self.ollama_url)

        # Recommendations / presets
        preset_row = QHBoxLayout()
        for key, info in config.OLLAMA_PRESETS.items():
            btn = QPushButton(info["label"])
            btn.setToolTip(info["desc"])
            btn.clicked.connect(lambda _=False, m=info["model"]: self._apply_preset(m))
            preset_row.addWidget(btn)
        preset_row.addStretch()
        f.addRow("Recommend:", preset_row)

        # Detected installed models (filesystem scan)
        self.installed_combo = QComboBox()
        self.installed_combo.setEditable(False)
        self.installed_combo.currentTextChanged.connect(self._on_installed_selected)
        scan_btn = QPushButton("🔍 Scan")
        scan_btn.setToolTip("Scan filesystem for installed Ollama models (works even if Ollama is off)")
        scan_btn.clicked.connect(self._scan_filesystem)
        update_all_btn = QPushButton("⟳ Update all")
        update_all_btn.setToolTip(
            "Re-download every installed model from registry.ollama.ai "
            "(inspired by tz-ollama-utils)."
        )
        update_all_btn.clicked.connect(self._update_all)
        installed_row = QHBoxLayout()
        installed_row.addWidget(self.installed_combo, 1)
        installed_row.addWidget(scan_btn)
        installed_row.addWidget(update_all_btn)
        f.addRow("Installed:", installed_row)

        # Active model used for conversion
        f.addRow("Active model:", self.ollama_model)

        # Custom scan path
        scanpath_row = QHBoxLayout()
        self.custom_scan_path = QLineEdit(self.cfg.get("ollama_extra_scan_path", ""))
        self.custom_scan_path.setPlaceholderText("Optional — extra folder to scan (e.g. D:\\.ollama\\models)")
        browse_btn = QPushButton("…")
        browse_btn.setFixedWidth(32)
        browse_btn.clicked.connect(self._browse_scan_path)
        scanpath_row.addWidget(self.custom_scan_path, 1)
        scanpath_row.addWidget(browse_btn)
        f.addRow("Extra scan path:", scanpath_row)

        # Direct download
        pull_row = QHBoxLayout()
        self.pull_input = QLineEdit()
        self.pull_input.setPlaceholderText("e.g. llama3.2-vision:11b  (downloads directly, no daemon needed)")
        self.pull_btn = QPushButton("⬇ Download")
        self.pull_btn.clicked.connect(self._pull_model)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self._cancel_pull)
        pull_row.addWidget(self.pull_input, 1)
        pull_row.addWidget(self.pull_btn)
        pull_row.addWidget(self.cancel_btn)
        f.addRow("Direct download:", pull_row)

        self.pull_progress = QProgressBar()
        self.pull_progress.setRange(0, 100)
        self.pull_progress.setValue(0)
        self.pull_progress.setVisible(False)
        f.addRow("", self.pull_progress)

        self.pull_status = QLabel("")
        self.pull_status.setWordWrap(True)
        self.pull_status.setStyleSheet("color: #8a909c; font-size: 11px;")
        f.addRow("", self.pull_status)

        layout.addWidget(olm)

        # ---- OpenAI ----
        op = QGroupBox("OpenAI")
        of = QFormLayout(op)
        self.openai_key = QLineEdit(self.cfg["openai_api_key"])
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_model = QLineEdit(self.cfg["openai_model"])
        self.openai_base = QLineEdit(self.cfg["openai_base_url"])
        of.addRow("API key:", self.openai_key)
        of.addRow("Model:", self.openai_model)
        of.addRow("Base URL:", self.openai_base)
        layout.addWidget(op)

        # ---- Anthropic ----
        an = QGroupBox("Anthropic Claude")
        af = QFormLayout(an)
        self.an_key = QLineEdit(self.cfg["anthropic_api_key"])
        self.an_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.an_model = QLineEdit(self.cfg["anthropic_model"])
        af.addRow("API key:", self.an_key)
        af.addRow("Model:", self.an_model)
        layout.addWidget(an)

        # ---- Custom OpenAI-compatible ----
        cm = QGroupBox("Custom OpenAI-compatible  ·  Groq · OpenRouter · LM Studio · vLLM")
        cf = QFormLayout(cm)
        self.compat_key = QLineEdit(self.cfg["compat_api_key"])
        self.compat_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.compat_base = QLineEdit(self.cfg["compat_base_url"])
        self.compat_model = QLineEdit(self.cfg["compat_model"])
        cf.addRow("API key:", self.compat_key)
        cf.addRow("Base URL:", self.compat_base)
        cf.addRow("Model:", self.compat_model)
        layout.addWidget(cm)

        # ---- LLM prompt (shared by all LLM engines) ----
        pm = QGroupBox("LLM conversion prompt")
        pf = QVBoxLayout(pm)
        pf_hint = QLabel(
            "Prompt sent to <b>Ollama / OpenAI / Anthropic</b> alongside each "
            "rendered PDF page. Leave blank to use the built-in default."
        )
        pf_hint.setWordWrap(True); pf_hint.setObjectName("Hint")
        pf.addWidget(pf_hint)
        self.prompt_edit = QPlainTextEdit()
        self.prompt_edit.setPlaceholderText(converters.PROMPT)
        self.prompt_edit.setPlainText(self.cfg.get("custom_prompt", "") or "")
        self.prompt_edit.setMinimumHeight(110)
        self.prompt_edit.setToolTip(
            "Override the system/user prompt for LLM engines. Useful for:\n"
            "  • Preserving LaTeX math\n"
            "  • Asking for specific Markdown dialects (CommonMark, GFM, …)\n"
            "  • Domain hints (academic paper, recipe, invoice, code, …)"
        )
        pf.addWidget(self.prompt_edit)
        preset_row = QHBoxLayout()
        presets = [
            ("Reset to default", ""),
            ("Academic paper", converters.PROMPT + " This is an academic paper — preserve citations like [1], equations (LaTeX with $ delimiters), figure/table captions, and section numbering."),
            ("Code-heavy", converters.PROMPT + " Wrap every code snippet in a fenced code block with the appropriate language tag. Preserve indentation exactly."),
            ("Tables only", "Extract every table from this PDF page as GitHub-flavored Markdown tables. Ignore all other text. Output only the tables."),
        ]
        for label, text in presets:
            b = QPushButton(label)
            b.setObjectName("Ghost")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _=False, t=text: self.prompt_edit.setPlainText(t))
            preset_row.addWidget(b)
        preset_row.addStretch()
        pf.addLayout(preset_row)
        layout.addWidget(pm)

        # ---- Watch folder ----
        wf = QGroupBox("Watch folder  ·  auto-import new PDFs")
        wff = QFormLayout(wf)
        wf_hint = QLabel(
            "Distilmark can watch a folder and automatically add every new "
            "PDF that appears to the queue (great for scanner workflows). "
            "Optionally start the conversion right away."
        )
        wf_hint.setWordWrap(True); wf_hint.setObjectName("Hint")
        wff.addRow("", wf_hint)
        watch_row = QHBoxLayout()
        self.watch_path = QLineEdit(self.cfg.get("watch_folder", ""))
        self.watch_path.setPlaceholderText("Pick a folder to watch …")
        self.watch_path.setToolTip("Path of the folder Distilmark should watch for new PDFs.")
        watch_browse = QPushButton("…"); watch_browse.setFixedWidth(32)
        watch_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        watch_browse.clicked.connect(self._browse_watch_path)
        watch_row.addWidget(self.watch_path, 1)
        watch_row.addWidget(watch_browse)
        wff.addRow("Folder:", watch_row)
        self.watch_auto_cb = QCheckBox("Convert each new PDF immediately")
        self.watch_auto_cb.setChecked(self.cfg.get("watch_auto_convert", False))
        self.watch_auto_cb.setToolTip(
            "When a new PDF appears in the watch folder, kick off the queue "
            "automatically. If off, files are just added so you can review "
            "and press Convert yourself."
        )
        wff.addRow("", self.watch_auto_cb)
        layout.addWidget(wf)

        save_btn = QPushButton("Save settings")
        save_btn.setObjectName("Accent")
        save_btn.setMinimumHeight(38)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(save_btn)
        layout.addLayout(row)
        layout.addStretch()

        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def showEvent(self, event):
        super().showEvent(event)
        # Lazy first scan / status check when the tab is opened
        self._refresh_service_status()
        self._scan_filesystem()

    def _apply_preset(self, model: str):
        self.ollama_model.setText(model)
        self.pull_input.setText(model)

    # ----- Service status -----
    def _refresh_service_status(self):
        url = self.ollama_url.text().strip()
        running = ollama_manager.is_running(url)
        if running:
            self.service_label.setStyleSheet("color: #9ece6a;")
            self.service_label.setText("● Running")
            self.start_service_btn.setVisible(False)
        else:
            binary = ollama_manager.has_ollama_binary()
            if binary:
                self.service_label.setStyleSheet("color: #e0af68;")
                self.service_label.setText("○ Not running")
                self.start_service_btn.setVisible(True)
            else:
                self.service_label.setStyleSheet("color: #f7768e;")
                self.service_label.setText(
                    "✗ Ollama not installed — get it at ollama.com/download"
                )
                self.start_service_btn.setVisible(False)

    def _start_service(self):
        ok, msg = ollama_manager.start_service()
        self.service_label.setText(msg)
        if ok:
            QApplication.processEvents()
            # Give the daemon a moment to come up
            self.start_service_btn.setEnabled(False)
            self.start_service_btn.setText("Starting…")
            self.startTimer(2000)  # one-shot via timerEvent
        else:
            QMessageBox.warning(self, "Ollama", msg)

    def timerEvent(self, event):
        self.killTimer(event.timerId())
        self.start_service_btn.setEnabled(True)
        self.start_service_btn.setText("▶ Start Ollama")
        self._refresh_service_status()

    # ----- Filesystem scan -----
    def _scan_filesystem(self):
        extra: list[Path] = []
        custom = self.custom_scan_path.text().strip()
        if custom:
            extra.append(Path(custom))
        self._scan_worker = ScanWorker(extra)
        self._scan_worker.done.connect(self._on_scan_done)
        self.installed_combo.clear()
        self.installed_combo.addItem("Scanning…")
        self._scan_worker.start()

    def _on_scan_done(self, models):
        self.installed_combo.clear()
        if not models:
            self.installed_combo.addItem("(none found — try installing a model)")
            self.installed_combo.setEnabled(False)
            return
        self.installed_combo.setEnabled(True)
        for m in models:
            size = self._human(m.size_bytes) if m.size_bytes else "?"
            self.installed_combo.addItem(f"{m.name}    ({size})", m.name)
        # Pre-select current
        cur = self.ollama_model.text().strip()
        for i in range(self.installed_combo.count()):
            if self.installed_combo.itemData(i) == cur:
                self.installed_combo.setCurrentIndex(i)
                break

    def _update_all(self):
        # Build list of detected model names and queue them through the pull
        names: list[str] = []
        for i in range(self.installed_combo.count()):
            data = self.installed_combo.itemData(i)
            if data:
                names.append(data)
        if not names:
            QMessageBox.information(self, "Update all", "No installed models detected.")
            return
        r = QMessageBox.question(
            self, "Update all",
            f"Re-download {len(names)} installed model(s) from registry.ollama.ai?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if r != QMessageBox.StandardButton.Yes:
            return
        self._update_queue = names[1:]
        self.pull_input.setText(names[0])
        self._pull_model()

    def _on_installed_selected(self, text: str):
        data = self.installed_combo.currentData()
        if data:
            self.ollama_model.setText(data)

    @staticmethod
    def _human(n: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        f = float(n)
        for u in units:
            if f < 1024:
                return f"{f:.1f} {u}"
            f /= 1024
        return f"{f:.1f} PB"

    def _browse_scan_path(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Extra Ollama models folder to scan", str(Path.home())
        )
        if folder:
            self.custom_scan_path.setText(folder)
            self._scan_filesystem()

    # ----- Direct download -----
    def _pull_model(self):
        if self._pull_worker and self._pull_worker.isRunning():
            return
        model = self.pull_input.text().strip()
        if not model:
            return
        # Choose destination: first existing candidate dir, else default
        dirs = ollama_manager.candidate_models_dirs()
        dest = dirs[0] if dirs else ollama_manager.default_models_dir()
        self.pull_progress.setVisible(True)
        self.pull_progress.setValue(0)
        self.pull_status.setStyleSheet("color: #8a909c;")
        self.pull_status.setText(f"Starting direct download of {model} → {dest}")
        self.pull_btn.setEnabled(False)
        self.cancel_btn.setVisible(True)
        self._pull_worker = PullWorker(model, dest)
        self._pull_worker.progress_update.connect(self._on_pull_progress)
        self._pull_worker.finished_ok.connect(self._on_pull_done)
        self._pull_worker.failed.connect(self._on_pull_failed)
        self._pull_worker.start()

    def _cancel_pull(self):
        if self._pull_worker and self._pull_worker.isRunning():
            self._pull_worker.terminate()
            self.pull_status.setStyleSheet("color: #e0af68;")
            self.pull_status.setText("Download cancelled.")
            self.pull_btn.setEnabled(True)
            self.cancel_btn.setVisible(False)

    def _on_pull_progress(self, p):
        self.pull_progress.setValue(int(p.overall_pct))
        self.pull_status.setText(p.message)

    def _on_pull_done(self):
        self.pull_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.pull_progress.setValue(100)
        self.pull_status.setStyleSheet("color: #9ece6a;")
        self.pull_status.setText("✓ Download complete — model is ready to use.")
        self._scan_filesystem()
        self._refresh_service_status()
        # Chain "Update all" queue if active
        queue = getattr(self, "_update_queue", None)
        if queue:
            next_model = queue.pop(0)
            self.pull_input.setText(next_model)
            self._pull_model()

    def _on_pull_failed(self, err: str):
        self.pull_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)
        self.pull_progress.setVisible(False)
        self.pull_status.setStyleSheet("color: #f7768e;")
        # First line of traceback as friendly summary
        last = err.strip().splitlines()[-1] if err.strip() else "Unknown error"
        self.pull_status.setText(f"✗ {last}")

    def _save(self):
        self.cfg["ollama_url"] = self.ollama_url.text().strip()
        self.cfg["ollama_model"] = self.ollama_model.text().strip()
        self.cfg["ollama_extra_scan_path"] = self.custom_scan_path.text().strip()
        self.cfg["openai_api_key"] = self.openai_key.text().strip()
        self.cfg["openai_model"] = self.openai_model.text().strip()
        self.cfg["openai_base_url"] = self.openai_base.text().strip()
        self.cfg["anthropic_api_key"] = self.an_key.text().strip()
        self.cfg["anthropic_model"] = self.an_model.text().strip()
        self.cfg["compat_api_key"] = self.compat_key.text().strip()
        self.cfg["compat_base_url"] = self.compat_base.text().strip()
        self.cfg["compat_model"] = self.compat_model.text().strip()
        self.cfg["custom_prompt"] = self.prompt_edit.toPlainText().strip()
        self.cfg["watch_folder"] = self.watch_path.text().strip()
        self.cfg["watch_auto_convert"] = self.watch_auto_cb.isChecked()
        config.save(self.cfg)
        # Signal MainWindow to refresh the watcher
        self.settings_saved.emit()
        QMessageBox.information(self, "Saved", "Settings saved.")

    def _browse_watch_path(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Pick a folder to watch", str(Path.home())
        )
        if folder:
            self.watch_path.setText(folder)


# ---------------------------------------------------------------------------
# History page
# ---------------------------------------------------------------------------

class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title_row = QHBoxLayout()
        title = QLabel("History")
        title.setObjectName("H1")
        title_row.addWidget(title)
        title_row.addStretch()
        clear_btn = QPushButton("Clear history")
        clear_btn.setObjectName("Danger")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear)
        title_row.addWidget(clear_btn)
        layout.addLayout(title_row)

        subtitle = QLabel("All conversions this session and across sessions. Most recent first.")
        subtitle.setObjectName("H2")
        layout.addWidget(subtitle)

        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        layout.addWidget(self.list, 1)

        self.summary = QLabel("")
        self.summary.setObjectName("Hint")
        layout.addWidget(self.summary)

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh()

    def refresh(self):
        self.list.clear()
        history = config.load_history()
        ok = sum(1 for e in history if e.get("status") == "ok")
        err = len(history) - ok
        self.summary.setText(
            f"{len(history)} total  ·  {ok} succeeded  ·  {err} failed"
        )
        for entry in reversed(history):
            status = entry.get("status", "?")
            ts = entry.get("ts", "")
            source = entry.get("source", "?")
            engine = entry.get("engine", "?")
            pages = entry.get("pages", "?")
            output = entry.get("output", "")
            icon = "✓" if status == "ok" else "✗"
            text = (
                f" {icon}  {ts}  |  {source}  →  {output}  "
                f"|  {engine}  |  {pages} page(s)"
            )
            item = QListWidgetItem(text)
            if status == "error":
                item.setForeground(QColor("#f7768e"))
            else:
                item.setForeground(QColor("#9ece6a"))
            self.list.addItem(item)

    def _clear(self):
        r = QMessageBox.question(
            self, "Clear history",
            "Delete all history entries?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if r == QMessageBox.StandardButton.Yes:
            config.clear_history()
            self.refresh()


# ---------------------------------------------------------------------------
# Preview page — source PDF beside rendered Markdown
# ---------------------------------------------------------------------------

class PreviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf_path: str | None = None
        self._page_index = 0
        self._page_count = 0
        self._data: dict | None = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("Preview")
        title.setObjectName("H1")
        layout.addWidget(title)

        self.subtitle = QLabel(
            "Convert a file to preview the source PDF beside the rendered Markdown."
        )
        self.subtitle.setObjectName("H2")
        layout.addWidget(self.subtitle)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left — rendered PDF page with navigation
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        nav = QHBoxLayout()
        self.prev_btn = QPushButton("◀ Prev")
        self.prev_btn.setObjectName("Ghost")
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.clicked.connect(self._prev_page)
        self.next_btn = QPushButton("Next ▶")
        self.next_btn.setObjectName("Ghost")
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(self._next_page)
        self.page_label = QLabel("—")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav.addWidget(self.prev_btn)
        nav.addWidget(self.page_label, 1)
        nav.addWidget(self.next_btn)
        lv.addLayout(nav)
        self.pdf_scroll = QScrollArea()
        self.pdf_scroll.setWidgetResizable(False)
        self.pdf_scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pdf_label = QLabel("No PDF loaded yet.")
        self.pdf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pdf_scroll.setWidget(self.pdf_label)
        lv.addWidget(self.pdf_scroll, 1)
        splitter.addWidget(left)

        # Right — markdown output tabs
        self.tabs = QTabWidget()
        splitter.addWidget(self.tabs)
        splitter.setSizes([460, 660])
        layout.addWidget(splitter, 1)

    def load(self, data: dict):
        self._data = data
        self._pdf_path = data.get("pdf")
        self._page_index = 0
        name = Path(self._pdf_path).name if self._pdf_path else ""
        mode = "compare" if data.get("compare") else "single"
        self.subtitle.setText(f"{name}  ·  {mode} mode")
        try:
            import pymupdf
            doc = pymupdf.open(self._pdf_path)
            self._page_count = doc.page_count
            doc.close()
        except Exception:
            self._page_count = 0
        self._render_pdf_page()
        self._build_tabs(data)

    @staticmethod
    def _render_md(browser: QTextBrowser, md: str, output_path: str | None) -> None:
        """Render markdown with the right base URL so relative image paths
        (e.g. ``./name_images/page1_img1.png``) resolve to real files."""
        if output_path:
            base = Path(output_path).parent
            browser.setSearchPaths([str(base)])
            browser.document().setBaseUrl(QUrl.fromLocalFile(str(base) + "/"))
        browser.setOpenExternalLinks(True)
        browser.setMarkdown(md)

    def _build_tabs(self, data: dict):
        self.tabs.clear()
        self._rendered_browsers = {}  # for streaming updates
        self._editor_source: QPlainTextEdit | None = None
        self._editor_output: str | None = None
        if data.get("compare"):
            nb = QTextBrowser()
            self._render_md(nb, data.get("md_native", ""), data.get("output_native"))
            self.tabs.addTab(nb, "⚡ Native")
            self._rendered_browsers[0] = nb
            pb = QTextBrowser()
            self._render_md(pb, data.get("md_pdfplumber", ""), data.get("output_pdfplumber"))
            self.tabs.addTab(pb, "📐 pdfplumber")
            self._rendered_browsers[1] = pb
            diff = QTextBrowser()
            diff.setHtml(self._make_diff(
                data.get("md_native", ""), data.get("md_pdfplumber", "")
            ))
            self.tabs.addTab(diff, "≠ Diff")
        else:
            rendered = QTextBrowser()
            self._render_md(rendered, data.get("md", ""), data.get("output"))
            self.tabs.addTab(rendered, "Rendered")
            self._rendered_browsers[0] = rendered
            # Editable Source tab
            src_widget = QWidget()
            sv = QVBoxLayout(src_widget); sv.setContentsMargins(0, 0, 0, 0); sv.setSpacing(8)
            src = QPlainTextEdit(); src.setPlainText(data.get("md", "")); src.setReadOnly(False)
            src.setToolTip("Edit the Markdown freely. Click 'Save edits' to write back to disk.")
            self._editor_source = src
            self._editor_output = data.get("output")
            sv.addWidget(src, 1)
            row = QHBoxLayout()
            save_btn = QPushButton("💾 Save edits")
            save_btn.setObjectName("Accent")
            save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            save_btn.setToolTip("Save the edited Markdown back to the output file.")
            save_btn.clicked.connect(self._save_edits)
            revert_btn = QPushButton("Revert")
            revert_btn.setObjectName("Ghost")
            revert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            revert_btn.clicked.connect(lambda: src.setPlainText(data.get("md", "")))
            self._edit_status = QLabel(""); self._edit_status.setObjectName("Hint")
            row.addWidget(revert_btn); row.addStretch()
            row.addWidget(self._edit_status); row.addWidget(save_btn)
            sv.addLayout(row)
            self.tabs.addTab(src_widget, "Source / Edit")

    def _save_edits(self):
        if not (self._editor_source and self._editor_output):
            return
        try:
            Path(self._editor_output).write_text(
                self._editor_source.toPlainText(), encoding="utf-8"
            )
            self._edit_status.setText("✓ Saved")
            # Re-render the Rendered tab in place
            br = self._rendered_browsers.get(0)
            if br is not None:
                self._render_md(br, self._editor_source.toPlainText(), self._editor_output)
        except OSError as e:
            self._edit_status.setText(f"✗ {e}")

    def start_stream(self, pdf_path: str):
        """Initialise the Preview tab with an empty Rendered area ready to
        receive live LLM stream chunks for the file ``pdf_path``."""
        from PyQt6.QtCore import Qt as _Qt
        self._pdf_path = pdf_path
        try:
            import pymupdf
            doc = pymupdf.open(pdf_path); self._page_count = doc.page_count; doc.close()
        except Exception:
            self._page_count = 0
        self._page_index = 0
        self._render_pdf_page()
        name = Path(pdf_path).name if pdf_path else ""
        self.subtitle.setText(f"{name}  ·  streaming")
        # Reset the right-side tabs to a single live "Rendered" tab.
        self.tabs.clear()
        self._rendered_browsers = {}
        self._editor_source = None
        live = QTextBrowser()
        live.setOpenExternalLinks(True)
        self._rendered_browsers[0] = live
        self.tabs.addTab(live, "🟢 Live")

    # Streaming hook: append a chunk of tokens to the most recent Rendered tab.
    def append_stream(self, page_idx: int, chunk: str):
        # We only display the live stream for the single-engine case; in compare
        # mode the writes interleave both engines.
        br = self._rendered_browsers.get(0)
        if br is None:
            return
        cur = br.toPlainText()
        if not cur.endswith("\n") and chunk and chunk[0] not in "\n ":
            cur += ""
        br.setPlainText(cur + chunk)

    @staticmethod
    def _make_diff(a: str, b: str) -> str:
        import difflib
        return difflib.HtmlDiff(wrapcolumn=70).make_table(
            a.splitlines(), b.splitlines(),
            fromdesc="native", todesc="pdfplumber",
            context=True, numlines=2,
        )

    def _render_pdf_page(self):
        if not self._pdf_path or self._page_count == 0:
            self.pdf_label.setText("No PDF loaded yet.")
            self.pdf_label.adjustSize()
            self.page_label.setText("—")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        try:
            import pymupdf
            doc = pymupdf.open(self._pdf_path)
            page = doc[self._page_index]
            pix = page.get_pixmap(dpi=110)
            data = pix.tobytes("png")
            doc.close()
            img = QPixmap()
            img.loadFromData(data)
            self.pdf_label.setPixmap(img)
            self.pdf_label.resize(img.size())
        except Exception as e:
            self.pdf_label.setText(f"Could not render page: {e}")
            self.pdf_label.adjustSize()
        self.page_label.setText(f"Page {self._page_index + 1} / {self._page_count}")
        self.prev_btn.setEnabled(self._page_index > 0)
        self.next_btn.setEnabled(self._page_index < self._page_count - 1)

    def _prev_page(self):
        if self._page_index > 0:
            self._page_index -= 1
            self._render_pdf_page()

    def _next_page(self):
        if self._page_index < self._page_count - 1:
            self._page_index += 1
            self._render_pdf_page()


# ---------------------------------------------------------------------------
# Courses page — organise PDFs into courses with chapters (library view)
# ---------------------------------------------------------------------------

_ROLE_KIND = Qt.ItemDataRole.UserRole + 10      # "chapter" | "document"
_ROLE_CID = Qt.ItemDataRole.UserRole + 11       # chapter id
_ROLE_SOURCE = Qt.ItemDataRole.UserRole + 12    # document source path


class CoursesPage(QWidget):
    conversion_done = pyqtSignal()
    preview_ready = pyqtSignal(dict)

    def __init__(self, cfg: dict, status: QStatusBar, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.status = status
        self._pid: str | None = None
        self._worker: ConvertWorker | None = None
        self._convert_jobs: list[tuple[str, str, Path]] = []  # (cid, source, out_dir)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("Courses")
        title.setObjectName("H1")
        layout.addWidget(title)
        subtitle = QLabel(
            "Group your PDFs into courses and chapters — perfect for exam prep. "
            "See at a glance which files are added and which are converted."
        )
        subtitle.setObjectName("H2")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Course selector row
        crow = QHBoxLayout()
        self.course_combo = QComboBox()
        self.course_combo.setToolTip("Select a course to view its chapters and documents.")
        self.course_combo.currentIndexChanged.connect(self._on_course_changed)
        new_btn = QPushButton("New course")
        new_btn.setObjectName("Accent")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.clicked.connect(self._new_course)
        ren_btn = QPushButton("Rename")
        ren_btn.setObjectName("Ghost")
        ren_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ren_btn.clicked.connect(self._rename_course)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("Danger")
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.clicked.connect(self._delete_course)
        crow.addWidget(QLabel("Course:"))
        crow.addWidget(self.course_combo, 1)
        crow.addWidget(new_btn)
        crow.addWidget(ren_btn)
        crow.addWidget(del_btn)
        layout.addLayout(crow)

        # Toolbar
        trow = QHBoxLayout()
        self.add_chapter_btn = QPushButton("＋ Chapter")
        self.add_chapter_btn.setObjectName("Ghost")
        self.add_pdfs_btn = QPushButton("＋ Add PDFs to chapter")
        self.add_pdfs_btn.setObjectName("Ghost")
        self.convert_btn = QPushButton("Convert pending  →")
        self.convert_btn.setObjectName("Primary")
        self.open_btn = QPushButton("Open output")
        self.open_btn.setObjectName("Ghost")
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setObjectName("Danger")
        for b, fn, tip in [
            (self.add_chapter_btn, self._add_chapter, "Add a new chapter to this course."),
            (self.add_pdfs_btn, self._add_pdfs, "Add PDF files to the selected chapter."),
            (self.convert_btn, self._convert_pending, "Convert every not-yet-converted document in this course."),
            (self.open_btn, self._open_selected_output, "Open the converted Markdown / its folder."),
            (self.remove_btn, self._remove_selected, "Remove the selected chapter or document."),
        ]:
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setToolTip(tip)
            b.clicked.connect(fn)
        trow.addWidget(self.add_chapter_btn)
        trow.addWidget(self.add_pdfs_btn)
        trow.addStretch()
        trow.addWidget(self.open_btn)
        trow.addWidget(self.remove_btn)
        trow.addWidget(self.convert_btn)
        layout.addLayout(trow)

        # Library tree
        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels(["Name", "Status", "Engine", "Pages"])
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(True)
        self.tree.setUniformRowHeights(True)
        self.tree.itemDoubleClicked.connect(self._on_double_click)
        hdr = self.tree.header()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in (1, 2, 3):
            hdr.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.tree, 1)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.summary = QLabel("")
        self.summary.setObjectName("Hint")
        layout.addWidget(self.summary)

    # ---- lifecycle ----
    def showEvent(self, event):
        super().showEvent(event)
        self._reload_courses()

    def _reload_courses(self):
        data = projects.load()
        self.course_combo.blockSignals(True)
        self.course_combo.clear()
        for p in data["projects"]:
            self.course_combo.addItem(p["name"], p["id"])
        # restore selection
        if self._pid:
            idx = self.course_combo.findData(self._pid)
            if idx >= 0:
                self.course_combo.setCurrentIndex(idx)
        self.course_combo.blockSignals(False)
        if self.course_combo.count() and self.course_combo.currentIndex() < 0:
            self.course_combo.setCurrentIndex(0)
        self._pid = self.course_combo.currentData()
        self._refresh_tree()

    def _current_project(self) -> dict | None:
        if not self._pid:
            return None
        return next((p for p in projects.load()["projects"] if p["id"] == self._pid), None)

    def _on_course_changed(self, _idx):
        self._pid = self.course_combo.currentData()
        self._refresh_tree()

    # ---- course CRUD ----
    def _new_course(self):
        name, ok = QInputDialog.getText(self, "New course", "Course name:")
        if ok and name.strip():
            p = projects.add_project(name)
            self._pid = p["id"]
            self._reload_courses()

    def _rename_course(self):
        p = self._current_project()
        if not p:
            return
        name, ok = QInputDialog.getText(self, "Rename course", "New name:", text=p["name"])
        if ok and name.strip():
            projects.rename_project(p["id"], name)
            self._reload_courses()

    def _delete_course(self):
        p = self._current_project()
        if not p:
            return
        if QMessageBox.question(
            self, "Delete course",
            f"Delete course “{p['name']}” and its chapter list?\n"
            "(Your PDFs and converted files are not deleted.)",
        ) == QMessageBox.StandardButton.Yes:
            projects.delete_project(p["id"])
            self._pid = None
            self._reload_courses()

    # ---- chapters / docs ----
    def _add_chapter(self):
        if not self._pid:
            QMessageBox.information(self, "Courses", "Create a course first."); return
        name, ok = QInputDialog.getText(self, "New chapter", "Chapter name:")
        if ok and name.strip():
            projects.add_chapter(self._pid, name)
            self._refresh_tree()

    def _selected_chapter_id(self) -> str | None:
        item = self.tree.currentItem()
        if item is None:
            return None
        if item.data(0, _ROLE_KIND) == "document":
            item = item.parent()
        if item is None:
            return None
        return item.data(0, _ROLE_CID)

    def _add_pdfs(self):
        if not self._pid:
            QMessageBox.information(self, "Courses", "Create a course first."); return
        cid = self._selected_chapter_id()
        if not cid:
            QMessageBox.information(self, "Courses", "Select a chapter to add PDFs to."); return
        files, _ = QFileDialog.getOpenFileNames(
            self, "Add PDFs to chapter", str(Path.home()), "PDF files (*.pdf)"
        )
        added = 0
        for f in files:
            if projects.add_document(self._pid, cid, f):
                added += 1
        if added:
            self.status.showMessage(f"Added {added} document(s) to chapter.", 4000)
        self._refresh_tree()

    def _remove_selected(self):
        item = self.tree.currentItem()
        if item is None or not self._pid:
            return
        kind = item.data(0, _ROLE_KIND)
        if kind == "chapter":
            cid = item.data(0, _ROLE_CID)
            if QMessageBox.question(self, "Remove chapter",
                                    "Remove this chapter and its document list?") == QMessageBox.StandardButton.Yes:
                projects.delete_chapter(self._pid, cid)
        elif kind == "document":
            cid = item.parent().data(0, _ROLE_CID)
            src = item.data(0, _ROLE_SOURCE)
            projects.remove_document(self._pid, cid, src)
        self._refresh_tree()

    # ---- tree rendering ----
    def _refresh_tree(self):
        self.tree.clear()
        p = self._current_project()
        if not p:
            self.summary.setText("No course selected. Click “New course” to begin.")
            return
        for chapter in p.get("chapters", []):
            docs = chapter.get("documents", [])
            conv = sum(1 for d in docs if d.get("status") == projects.CONVERTED)
            citem = QTreeWidgetItem([
                chapter["name"], f"{conv}/{len(docs)} converted", "", ""
            ])
            citem.setData(0, _ROLE_KIND, "chapter")
            citem.setData(0, _ROLE_CID, chapter["id"])
            f = citem.font(0); f.setBold(True); citem.setFont(0, f)
            self.tree.addTopLevelItem(citem)
            for d in docs:
                name = Path(d["source"]).name
                status = d.get("status", projects.ADDED)
                ditem = QTreeWidgetItem([
                    name, _STATUS_LABEL.get(status, status),
                    d.get("engine", ""), str(d.get("pages") or ""),
                ])
                ditem.setData(0, _ROLE_KIND, "document")
                ditem.setData(0, _ROLE_SOURCE, d["source"])
                ditem.setToolTip(0, d["source"])
                color = {
                    projects.CONVERTED: "#22c55e",
                    projects.FAILED: "#f87171",
                    projects.ADDED: "#fbbf24",
                }.get(status)
                if color:
                    ditem.setForeground(1, QColor(color))
                citem.addChild(ditem)
            citem.setExpanded(True)
        ch, docs, conv = projects.project_stats(p)
        pending = docs - conv
        self.summary.setText(
            f"{ch} chapter(s)  ·  {docs} document(s)  ·  {conv} converted  ·  {pending} pending"
        )

    def _on_double_click(self, item, _col):
        if item.data(0, _ROLE_KIND) != "document":
            return
        # Open converted markdown in Preview if available
        cid = item.parent().data(0, _ROLE_CID)
        p = self._current_project()
        chapter = next((c for c in p.get("chapters", []) if c["id"] == cid), None)
        if not chapter:
            return
        src = item.data(0, _ROLE_SOURCE)
        doc = next((d for d in chapter["documents"] if d["source"] == src), None)
        if doc and doc.get("status") == projects.CONVERTED and doc.get("output") and Path(doc["output"]).exists():
            md = Path(doc["output"]).read_text(encoding="utf-8")
            self.preview_ready.emit({"pdf": src, "compare": False, "md": md, "output": doc["output"]})
            self.status.showMessage("Opened in Preview tab.", 3000)
        else:
            self.status.showMessage("Not converted yet — use “Convert pending”.", 4000)

    def _open_selected_output(self):
        item = self.tree.currentItem()
        if item is None or item.data(0, _ROLE_KIND) != "document":
            return
        cid = item.parent().data(0, _ROLE_CID)
        p = self._current_project()
        chapter = next((c for c in p.get("chapters", []) if c["id"] == cid), None)
        src = item.data(0, _ROLE_SOURCE)
        doc = next((d for d in chapter["documents"] if d["source"] == src), None) if chapter else None
        if doc and doc.get("output") and Path(doc["output"]).exists():
            ConvertPage._open_in_file_browser(Path(doc["output"]))
        else:
            self.status.showMessage("No converted output for this document yet.", 4000)

    # ---- conversion of pending docs ----
    def _convert_pending(self):
        p = self._current_project()
        if not p:
            return
        if self._worker and self._worker.isRunning():
            return
        # gather pending docs
        pending: list[tuple[str, str]] = []
        for c in p.get("chapters", []):
            for d in c.get("documents", []):
                if d.get("status") != projects.CONVERTED:
                    pending.append((c["id"], d["source"]))
        if not pending:
            QMessageBox.information(self, "Courses", "Nothing pending — all documents are converted.")
            return
        out_dir = QFileDialog.getExistingDirectory(
            self, "Output folder for this course",
            self.cfg.get("last_output_dir", str(Path.home())),
        )
        if not out_dir:
            return
        self.cfg["last_output_dir"] = out_dir
        config.save(self.cfg)
        out = Path(out_dir)
        self._convert_jobs = [(cid, src, out) for cid, src in pending]
        self._convert_total = len(self._convert_jobs)
        self._convert_done = 0
        self.convert_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self._convert_next()

    def _convert_next(self):
        if not self._convert_jobs:
            self.convert_btn.setEnabled(True)
            self.progress.setVisible(False)
            self.status.showMessage(
                f"Course conversion complete — {self._convert_done} file(s).", 8000
            )
            self.conversion_done.emit()
            self._refresh_tree()
            return
        cid, src, out = self._convert_jobs.pop(0)
        pdf = Path(src)
        if not pdf.exists():
            projects.update_document(self._pid, cid, src, status=projects.FAILED, output="")
            self._convert_next()
            return
        img_name = f"{pdf.stem}_images" if self.cfg.get("include_images") else None
        img_dir = out / img_name if img_name else None
        self._cur_job = (cid, src, out)
        self._worker = ConvertWorker(pdf, dict(self.cfg), img_dir, img_name)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_ok.connect(self._on_doc_done)
        self._worker.finished_compare.connect(self._on_doc_done_compare)
        self._worker.failed.connect(self._on_doc_failed)
        self._worker.cancelled.connect(lambda *_: self._convert_next())
        n = self._convert_total - len(self._convert_jobs)
        self.status.showMessage(f"Converting {n}/{self._convert_total}: {pdf.name}")
        self._worker.start()

    def _on_progress(self, cur, total, msg):
        self.progress.setValue(int(cur / max(total, 1) * 100))
        self.status.showMessage(msg)

    def _on_doc_done(self, md: str, src: str, pages: int):
        cid, jsrc, out = self._cur_job
        out_path = out / f"{Path(src).stem}.md"
        out_path.write_text(md, encoding="utf-8")
        projects.update_document(
            self._pid, cid, jsrc,
            status=projects.CONVERTED, output=str(out_path),
            engine=self.cfg.get("engine", "native"), pages=pages,
        )
        self._convert_done += 1
        self._refresh_tree()
        self._convert_next()

    def _on_doc_done_compare(self, md_native: str, md_plumber: str, src: str, pages: int):
        cid, jsrc, out = self._cur_job
        out_path = out / f"{Path(src).stem}_native.md"
        out_path.write_text(md_native, encoding="utf-8")
        (out / f"{Path(src).stem}_pdfplumber.md").write_text(md_plumber, encoding="utf-8")
        projects.update_document(
            self._pid, cid, jsrc,
            status=projects.CONVERTED, output=str(out_path),
            engine="compare", pages=pages,
        )
        self._convert_done += 1
        self._refresh_tree()
        self._convert_next()

    def _on_doc_failed(self, src: str, err: str):
        cid, jsrc, out = self._cur_job
        projects.update_document(self._pid, cid, jsrc, status=projects.FAILED)
        self._refresh_tree()
        self._convert_next()


_STATUS_LABEL = {
    projects.ADDED: "● added",
    projects.CONVERTED: "✓ converted",
    projects.FAILED: "✗ failed",
}


# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        version = __version__

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("Distilmark")
        title.setObjectName("H1")
        title.setStyleSheet("font-size: 28px;")
        layout.addWidget(title)

        ver = QLabel(f"Version {version}  ·  Distil any PDF into clean Markdown")
        ver.setObjectName("Hint")
        layout.addWidget(ver)

        tagline = QLabel(
            "A modern, multi-engine desktop app for turning PDFs into clean Markdown — "
            "works fully offline or with any hosted LLM."
        )
        tagline.setWordWrap(True)
        tagline.setStyleSheet("font-size: 14px; padding-top: 8px; padding-bottom: 8px;")
        layout.addWidget(tagline)

        engines = QGroupBox("Conversion engines")
        eg = QVBoxLayout(engines)
        for line in (
            "• <b>Native</b> — offline, fast. PyMuPDF + pymupdf4llm.",
            "• <b>pdfplumber</b> — offline, layout-aware. Best for table-heavy PDFs.",
            "• <b>Compare</b> — runs native + pdfplumber simultaneously, outputs two files side-by-side for quality comparison.",
            "• <b>Ollama</b> — local vision LLMs (llama3.2-vision, llava, …). Fully offline.",
            "• <b>OpenAI</b> — hosted vision models (gpt-4o-mini and friends).",
            "• <b>Anthropic Claude</b> — Claude Haiku / Sonnet / Opus with vision.",
            "• <b>OpenAI-compatible</b> — Groq, OpenRouter, LM Studio, vLLM, custom endpoints.",
        ):
            lbl = QLabel(line)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            eg.addWidget(lbl)
        layout.addWidget(engines)

        features = QGroupBox("Features")
        fg = QVBoxLayout(features)
        for line in (
            "• Courses & chapters — organise PDFs into courses with a library view of added vs converted files",
            "• Editable live preview — edit the Markdown and save back; HTML / DOCX / combined-md export",
            "• Custom LLM prompts, math (LaTeX) mode, streaming output, and a watch folder",
            "• Dual-engine compare mode — native + pdfplumber outputs two files for easy quality comparison",
            "• Live preview — source PDF page beside rendered Markdown, with a diff view in compare mode",
            "• OCR fallback for scanned PDFs (via Tesseract)",
            "• Page-range selection — convert only the pages you need",
            "• Cancellable conversions with a Cancel button",
            "• Cost estimator for hosted LLM engines before you convert",
            "• Parallel page processing for hosted LLM engines (configurable)",
            "• Post-processing — merge hyphenated breaks, collapse blanks, strip headers/footers",
            "• pdfplumber table tuning in Advanced options",
            "• Drag-and-drop batch conversion with file queue",
            "• Smart folder scanning — finds all PDFs recursively",
            "• Background worker thread — UI stays responsive",
            "• Per-page progress bar and live status messages",
            "• Embedded image extraction with relative paths (native engine)",
            "• Conversion history with timestamps, persisted across sessions",
            "• Ollama model management — preset tiers, download from UI",
            "• Dark and light themes",
            "• Persistent settings at <code>~/.distilmark/config.json</code>",
            "• Pre-built Windows .exe via GitHub Actions",
        ):
            lbl = QLabel(line)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            fg.addWidget(lbl)
        layout.addWidget(features)

        stack = QGroupBox("Built with")
        sg = QVBoxLayout(stack)
        sg.addWidget(QLabel("PyQt6 · PyMuPDF · pymupdf4llm · Python 3.10+ · MIT licensed"))
        layout.addWidget(stack)

        repo = QLabel(
            '<a style="color:#7aa2f7;" '
            'href="https://github.com/Hesamsamani/distilmark">'
            "github.com/Hesamsamani/distilmark</a>"
        )
        repo.setTextFormat(Qt.TextFormat.RichText)
        repo.setOpenExternalLinks(True)
        layout.addWidget(repo)
        layout.addStretch()

        scroll.setWidget(inner)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, cfg: dict):
        super().__init__()
        self.cfg = cfg
        self.setWindowTitle("Distilmark — PDF to Markdown")
        self.resize(1180, 760)
        self.setMinimumSize(QSize(920, 600))
        self._build()
        self._apply_theme()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(238)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        logo_row = QHBoxLayout()
        logo_row.setContentsMargins(18, 18, 18, 0)
        logo_row.setSpacing(10)
        logo_mark = QLabel()
        logo_mark.setPixmap(_brand_mark(26))
        logo_mark.setFixedSize(26, 26)
        logo_text = QLabel("Distilmark")
        logo_text.setStyleSheet("font-size: 19px; font-weight: 800;")
        logo_row.addWidget(logo_mark)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        logo_wrap = QWidget()
        logo_wrap.setLayout(logo_row)
        sb.addWidget(logo_wrap)
        sub = QLabel("PDF → Markdown converter")
        sub.setObjectName("Subtitle")
        sb.addWidget(sub)

        section = QLabel("NAVIGATION")
        section.setObjectName("SectionLabel")
        sb.addWidget(section)

        self.nav_buttons: list[QPushButton] = []
        for label, idx in [("Convert", 0), ("Courses", 1), ("Preview", 2), ("Engines", 3), ("History", 4), ("About", 5)]:
            b = QPushButton(f"  {label}")
            b.setObjectName("NavItem")
            b.setCheckable(True)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _checked, i=idx: self._switch(i))
            sb.addWidget(b)
            self.nav_buttons.append(b)
        self.nav_buttons[0].setChecked(True)

        sb.addStretch()

        section2 = QLabel("THEME")
        section2.setObjectName("SectionLabel")
        sb.addWidget(section2)

        theme_row = QHBoxLayout()
        theme_row.setContentsMargins(8, 4, 8, 12)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(self.cfg.get("theme", "dark"))
        self.theme_combo.currentTextChanged.connect(self._on_theme)
        theme_row.addWidget(self.theme_combo)
        wrap = QWidget()
        wrap.setLayout(theme_row)
        sb.addWidget(wrap)

        root.addWidget(sidebar)

        # Pages stack
        self.stack = QStackedWidget()
        status = QStatusBar()
        self.setStatusBar(status)

        self.convert_page = ConvertPage(self.cfg, status)
        self.courses_page = CoursesPage(self.cfg, status)
        self.preview_page = PreviewPage()
        self.settings_page = SettingsPage(self.cfg)
        self.history_page = HistoryPage()
        self.about_page = AboutPage()

        self.stack.addWidget(self.convert_page)
        self.stack.addWidget(self.courses_page)
        self.stack.addWidget(self.preview_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.about_page)

        # Refresh history tab when a conversion completes
        self.convert_page.conversion_done.connect(self.history_page.refresh)
        self.courses_page.conversion_done.connect(self.history_page.refresh)
        # Feed the Preview tab with the latest conversion result
        self.convert_page.preview_ready.connect(self.preview_page.load)
        self.courses_page.preview_ready.connect(self._preview_from_course)
        # Stream live LLM chunks into the Preview tab
        self.convert_page.stream_started.connect(self.preview_page.start_stream)
        self.convert_page.stream_chunk.connect(
            lambda src, idx, chunk: self.preview_page.append_stream(idx, chunk)
        )
        # Refresh the folder watcher when settings change
        self.settings_page.settings_saved.connect(self._refresh_watcher)

        root.addWidget(self.stack, 1)

        # ---- Global navigation shortcuts: Ctrl+1..6 ----
        from PyQt6.QtGui import QShortcut, QKeySequence
        for i in range(6):
            QShortcut(QKeySequence(f"Ctrl+{i+1}"), self,
                      activated=lambda _i=i: self._switch(_i))

        # ---- Folder watcher (auto-import new PDFs) ----
        from PyQt6.QtCore import QFileSystemWatcher, QTimer
        self._fs_watcher = QFileSystemWatcher(self)
        self._fs_watcher.directoryChanged.connect(self._on_watch_dir_changed)
        # Debounce: many editors create files in bursts
        self._watch_seen: set[str] = set()
        QTimer.singleShot(400, self._refresh_watcher)

    def _switch(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_buttons):
            b.setChecked(i == idx)

    def _preview_from_course(self, data: dict):
        # Courses page asked to show a converted doc — load it and jump to Preview.
        self.preview_page.load(data)
        self._switch(2)  # Preview is index 2 now

    def _refresh_watcher(self):
        # Re-arm QFileSystemWatcher to point at the configured folder (if any).
        for d in list(self._fs_watcher.directories()):
            self._fs_watcher.removePath(d)
        folder = self.cfg.get("watch_folder", "").strip()
        if not folder:
            self._watch_seen.clear()
            return
        p = Path(folder)
        if not p.is_dir():
            return
        self._fs_watcher.addPath(str(p))
        # Seed the seen-set with the current contents so we only pick up *new* PDFs
        self._watch_seen = {
            str(f) for f in p.glob("*")
            if f.suffix.lower() in SUPPORTED_INPUT_EXTS
        }

    def _on_watch_dir_changed(self, path: str):
        from PyQt6.QtCore import QTimer
        # Wait a beat so partially-written scans aren't read mid-stream
        QTimer.singleShot(800, lambda: self._collect_new_from(path))

    def _collect_new_from(self, path: str):
        p = Path(path)
        if not p.is_dir():
            return
        new_files = []
        for f in p.glob("*"):
            if f.suffix.lower() not in SUPPORTED_INPUT_EXTS:
                continue
            if str(f) in self._watch_seen:
                continue
            try:
                # Skip files still being written (size 0 / growing)
                if f.stat().st_size == 0:
                    continue
            except OSError:
                continue
            new_files.append(f)
            self._watch_seen.add(str(f))
        if not new_files:
            return
        # Add to the queue (switch to Convert tab so user sees them)
        self._switch(0)
        for f in new_files:
            self.convert_page._add(f)
        self.statusBar().showMessage(
            f"Watch folder: added {len(new_files)} new file(s).", 4000
        )
        if self.cfg.get("watch_auto_convert", False):
            self.convert_page.start_conversion()

    def _on_theme(self, name: str):
        self.cfg["theme"] = name
        config.save(self.cfg)
        self._apply_theme()

    def _apply_theme(self):
        app = QApplication.instance()
        if not app:
            return
        if self.cfg.get("theme", "dark") == "light":
            app.setStyleSheet(styles.LIGHT)
        else:
            app.setStyleSheet(styles.DARK)


def main() -> None:
    cfg = config.load()
    app = QApplication(sys.argv)
    app.setApplicationName("Distilmark")
    app.setWindowIcon(QIcon(_brand_mark(64)))
    w = MainWindow(cfg)
    w.setWindowIcon(QIcon(_brand_mark(64)))
    w.show()
    sys.exit(app.exec())
