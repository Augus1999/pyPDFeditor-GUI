# -*- coding: utf-8 -*-
"""pdf2md main application — modern PyQt6 GUI."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
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
)

from . import config, converters, styles
from ._version import __version__


# ---------------------------------------------------------------------------
# Worker: PDF → Markdown conversion
# ---------------------------------------------------------------------------

class ConvertWorker(QThread):
    progress = pyqtSignal(int, int, str)
    finished_ok = pyqtSignal(str, str, int)   # (markdown, source_pdf, page_count)
    failed = pyqtSignal(str, str)             # (source_pdf, error)

    def __init__(self, pdf: Path, cfg: dict, image_dir: Path | None, image_dir_name: str | None):
        super().__init__()
        self.pdf = pdf
        self.cfg = cfg
        self.image_dir = image_dir
        self.image_dir_name = image_dir_name

    def run(self) -> None:
        try:
            import pymupdf as _mupdf
            _doc = _mupdf.open(self.pdf)
            page_count = _doc.page_count
            _doc.close()

            opts = converters.ConvertOptions(
                include_images=self.cfg.get("include_images", True),
                page_separator=self.cfg.get("page_separator", True),
                image_dir=self.image_dir,
                image_dir_name=self.image_dir_name,
            )
            cb = lambda c, t, m: self.progress.emit(c, t, m)
            engine = self.cfg.get("engine", "native")

            if engine == "native":
                md = converters.convert_native(self.pdf, opts, cb)
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
            else:
                raise ValueError(f"Unknown engine: {engine}")

            self.finished_ok.emit(md, str(self.pdf), page_count)
        except Exception:
            self.failed.emit(str(self.pdf), traceback.format_exc())


# ---------------------------------------------------------------------------
# Worker: Ollama model pull (download)
# ---------------------------------------------------------------------------

class PullWorker(QThread):
    pull_progress = pyqtSignal(str, int, int)  # (status, total, completed)
    finished_ok = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, url: str, model: str):
        super().__init__()
        self.url = url
        self.model = model

    def run(self) -> None:
        try:
            converters.pull_ollama_model(
                self.url, self.model,
                lambda s, t, c: self.pull_progress.emit(s, t, c),
            )
            self.finished_ok.emit()
        except Exception:
            self.failed.emit(traceback.format_exc())


# ---------------------------------------------------------------------------
# Helper: procedural icon
# ---------------------------------------------------------------------------

def _make_icon(color: str, glyph: str) -> QIcon:
    pm = QPixmap(28, 28)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(2, 2, 24, 24)
    p.setPen(QColor("#ffffff"))
    f = QFont("Segoe UI", 12, QFont.Weight.Bold)
    p.setFont(f)
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, glyph)
    p.end()
    return QIcon(pm)


# ---------------------------------------------------------------------------
# Convert page
# ---------------------------------------------------------------------------

class ConvertPage(QWidget):
    conversion_done = pyqtSignal()  # notify History tab

    def __init__(self, cfg: dict, status: QStatusBar, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.status = status
        self.queue: list[Path] = []
        self.worker: ConvertWorker | None = None
        self._out_dir: Path = Path(cfg.get("last_output_dir", str(Path.home())))
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("PDF → Markdown")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        subtitle = QLabel("Drop files or a folder · pick an engine · hit Convert.")
        subtitle.setStyleSheet("color: #8a909c;")
        layout.addWidget(subtitle)

        # File / folder picker row
        file_row = QHBoxLayout()
        self.pick_btn = QPushButton(" Add PDFs")
        self.pick_btn.setIcon(_make_icon("#7aa2f7", "+"))
        self.pick_btn.clicked.connect(self.pick_files)

        self.folder_btn = QPushButton(" Add Folder")
        self.folder_btn.setIcon(_make_icon("#9ece6a", "📁"))
        self.folder_btn.clicked.connect(self.pick_folder)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_queue)

        file_row.addWidget(self.pick_btn)
        file_row.addWidget(self.folder_btn)
        file_row.addWidget(self.clear_btn)
        file_row.addStretch()
        layout.addLayout(file_row)

        self.list = QListWidget()
        self.list.setAcceptDrops(True)
        self.list.setMinimumHeight(160)
        self.setAcceptDrops(True)
        layout.addWidget(self.list, 1)

        self.queue_label = QLabel("")
        self.queue_label.setStyleSheet("color: #8a909c; font-size: 11px;")
        layout.addWidget(self.queue_label)

        # Engine + options
        opts_box = QGroupBox("Conversion options")
        opts_layout = QFormLayout(opts_box)

        self.engine_combo = QComboBox()
        self.engine_combo.addItem("⚡ Native (offline · PyMuPDF)", "native")
        self.engine_combo.addItem("🦙 Ollama (local LLM)", "ollama")
        self.engine_combo.addItem("🤖 OpenAI", "openai")
        self.engine_combo.addItem("🧠 Anthropic Claude", "anthropic")
        self.engine_combo.addItem("🌐 OpenAI-compatible (Groq · OpenRouter · LM Studio…)", "openai_compatible")
        cur = self.cfg.get("engine", "native")
        for i in range(self.engine_combo.count()):
            if self.engine_combo.itemData(i) == cur:
                self.engine_combo.setCurrentIndex(i)
                break
        opts_layout.addRow("Engine:", self.engine_combo)

        self.images_cb = QCheckBox("Extract embedded images (native engine)")
        self.images_cb.setChecked(self.cfg.get("include_images", True))
        opts_layout.addRow("", self.images_cb)

        self.sep_cb = QCheckBox("Insert --- between pages")
        self.sep_cb.setChecked(self.cfg.get("page_separator", True))
        opts_layout.addRow("", self.sep_cb)

        layout.addWidget(opts_box)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #8a909c; font-size: 11px;")
        layout.addWidget(self.progress_label)

        action_row = QHBoxLayout()
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("Primary")
        self.convert_btn.setMinimumHeight(38)
        self.convert_btn.clicked.connect(self.start_conversion)
        action_row.addStretch()
        action_row.addWidget(self.convert_btn)
        layout.addLayout(action_row)

    # ---- drag & drop ----
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            p = Path(url.toLocalFile())
            if p.is_dir():
                self._scan_folder(p)
            elif p.suffix.lower() == ".pdf" and p.exists():
                self._add(p)

    def _add(self, p: Path):
        if p in self.queue:
            return
        self.queue.append(p)
        item = QListWidgetItem(f"  {p.name}    —    {p.parent}")
        item.setData(Qt.ItemDataRole.UserRole, str(p))
        self.list.addItem(item)
        self._update_queue_label()

    def _scan_folder(self, folder: Path) -> int:
        found = sorted(
            set(folder.rglob("*.pdf")) | set(folder.rglob("*.PDF"))
        )
        for p in found:
            self._add(p)
        self._update_queue_label()
        return len(found)

    def _update_queue_label(self):
        n = len(self.queue)
        self.queue_label.setText(f"{n} file{'s' if n != 1 else ''} in queue")

    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Pick PDFs", str(Path.home()), "PDF files (*.pdf)"
        )
        for f in files:
            self._add(Path(f))

    def pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Pick folder to scan for PDFs", str(Path.home())
        )
        if folder:
            n = self._scan_folder(Path(folder))
            self.status.showMessage(f"Found {n} PDF(s) in folder.", 4000)

    def clear_queue(self):
        self.queue.clear()
        self.list.clear()
        self._update_queue_label()

    # ---- conversion ----
    def _sync_cfg(self):
        self.cfg["engine"] = self.engine_combo.currentData()
        self.cfg["include_images"] = self.images_cb.isChecked()
        self.cfg["page_separator"] = self.sep_cb.isChecked()
        config.save(self.cfg)

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
        self._remaining = list(self.queue)
        self._total_files = len(self._remaining)
        self._done_files = 0
        self.convert_btn.setEnabled(False)
        self._convert_next()

    def _convert_next(self):
        if not self._remaining:
            self.convert_btn.setEnabled(True)
            self.status.showMessage(
                f"All done — {self._done_files} file(s) converted.", 8000
            )
            self.progress.setValue(100)
            self.progress_label.setText("")
            self.conversion_done.emit()
            return
        pdf = self._remaining.pop(0)
        img_dir_name = f"{pdf.stem}_images" if self.cfg.get("include_images") else None
        img_dir = self._out_dir / img_dir_name if img_dir_name else None
        self.worker = ConvertWorker(pdf, dict(self.cfg), img_dir, img_dir_name)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self._on_done)
        self.worker.failed.connect(self._on_failed)
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
        self._convert_next()

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

        title = QLabel("Engine settings")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        # ---- Ollama ----
        olm = QGroupBox("🦙 Ollama (offline, local)")
        f = QFormLayout(olm)

        self.ollama_url = QLineEdit(self.cfg["ollama_url"])
        self.ollama_model = QLineEdit(self.cfg["ollama_model"])

        url_row = QHBoxLayout()
        url_row.addWidget(self.ollama_url)
        test_btn = QPushButton("Test")
        test_btn.clicked.connect(self._test_ollama)
        url_row.addWidget(test_btn)

        f.addRow("Server URL:", url_row)

        # Presets
        preset_row = QHBoxLayout()
        preset_lbl = QLabel("Presets:")
        preset_row.addWidget(preset_lbl)
        for key, info in config.OLLAMA_PRESETS.items():
            btn = QPushButton(info["label"])
            btn.setToolTip(info["desc"])
            btn.clicked.connect(lambda _=False, m=info["model"]: self._apply_preset(m))
            preset_row.addWidget(btn)
        preset_row.addStretch()
        f.addRow("", preset_row)

        # Available model selector
        self.model_combo = QComboBox()
        self.model_combo.addItem(self.cfg["ollama_model"])
        self.model_combo.currentTextChanged.connect(
            lambda t: self.ollama_model.setText(t)
        )
        refresh_btn = QPushButton("↻")
        refresh_btn.setFixedWidth(32)
        refresh_btn.setToolTip("Refresh model list from Ollama")
        refresh_btn.clicked.connect(self._refresh_models)
        model_row = QHBoxLayout()
        model_row.addWidget(self.model_combo)
        model_row.addWidget(refresh_btn)
        f.addRow("Model:", model_row)
        f.addRow("Custom model:", self.ollama_model)

        # Pull / download model
        pull_row = QHBoxLayout()
        self.pull_input = QLineEdit()
        self.pull_input.setPlaceholderText("e.g. llama3.2-vision:11b")
        self.pull_btn = QPushButton("⬇ Pull / Download")
        self.pull_btn.clicked.connect(self._pull_model)
        pull_row.addWidget(self.pull_input)
        pull_row.addWidget(self.pull_btn)
        f.addRow("Download model:", pull_row)

        self.pull_progress = QProgressBar()
        self.pull_progress.setRange(0, 100)
        self.pull_progress.setValue(0)
        self.pull_progress.setVisible(False)
        f.addRow("", self.pull_progress)

        self.pull_status = QLabel("")
        self.pull_status.setWordWrap(True)
        f.addRow("", self.pull_status)

        self.ollama_status = QLabel("")
        self.ollama_status.setWordWrap(True)
        f.addRow("", self.ollama_status)

        layout.addWidget(olm)

        # ---- OpenAI ----
        op = QGroupBox("🤖 OpenAI")
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
        an = QGroupBox("🧠 Anthropic Claude")
        af = QFormLayout(an)
        self.an_key = QLineEdit(self.cfg["anthropic_api_key"])
        self.an_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.an_model = QLineEdit(self.cfg["anthropic_model"])
        af.addRow("API key:", self.an_key)
        af.addRow("Model:", self.an_model)
        layout.addWidget(an)

        # ---- Custom OpenAI-compatible ----
        cm = QGroupBox("🌐 Custom OpenAI-compatible (Groq · OpenRouter · LM Studio · vLLM…)")
        cf = QFormLayout(cm)
        self.compat_key = QLineEdit(self.cfg["compat_api_key"])
        self.compat_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.compat_base = QLineEdit(self.cfg["compat_base_url"])
        self.compat_model = QLineEdit(self.cfg["compat_model"])
        cf.addRow("API key:", self.compat_key)
        cf.addRow("Base URL:", self.compat_base)
        cf.addRow("Model:", self.compat_model)
        layout.addWidget(cm)

        save_btn = QPushButton("Save settings")
        save_btn.setObjectName("Accent")
        save_btn.setMinimumHeight(38)
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

    def _apply_preset(self, model: str):
        self.ollama_model.setText(model)
        self.pull_input.setText(model)

    def _refresh_models(self):
        url = self.ollama_url.text().strip()
        models = converters.list_ollama_models(url)
        self.model_combo.clear()
        if models:
            for m in models:
                self.model_combo.addItem(m)
            cur = self.ollama_model.text().strip()
            idx = self.model_combo.findText(cur)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
            self._set_ollama_status(f"✓ {len(models)} model(s): " + ", ".join(models[:5]), "ok")
        else:
            self.model_combo.addItem(self.ollama_model.text())
            self._set_ollama_status("✗ Ollama unreachable — is `ollama serve` running?", "err")

    def _set_ollama_status(self, msg: str, kind: str):
        colors = {"ok": "#9ece6a", "err": "#f7768e", "warn": "#e0af68"}
        self.ollama_status.setStyleSheet(f"color: {colors.get(kind, '#8a909c')};")
        self.ollama_status.setText(msg)

    def _test_ollama(self):
        self._refresh_models()

    def _pull_model(self):
        if self._pull_worker and self._pull_worker.isRunning():
            return
        model = self.pull_input.text().strip()
        if not model:
            return
        url = self.ollama_url.text().strip()
        self.pull_progress.setVisible(True)
        self.pull_progress.setValue(0)
        self.pull_status.setText(f"Pulling {model}…")
        self.pull_btn.setEnabled(False)
        self._pull_worker = PullWorker(url, model)
        self._pull_worker.pull_progress.connect(self._on_pull_progress)
        self._pull_worker.finished_ok.connect(self._on_pull_done)
        self._pull_worker.failed.connect(self._on_pull_failed)
        self._pull_worker.start()

    def _on_pull_progress(self, status: str, total: int, completed: int):
        if total > 0:
            pct = int(completed / total * 100)
            self.pull_progress.setValue(pct)
            gb_done = completed / 1e9
            gb_total = total / 1e9
            self.pull_status.setText(f"{status}  {gb_done:.1f} GB / {gb_total:.1f} GB")
        else:
            self.pull_status.setText(status)

    def _on_pull_done(self):
        self.pull_btn.setEnabled(True)
        self.pull_progress.setValue(100)
        self.pull_status.setStyleSheet("color: #9ece6a;")
        self.pull_status.setText("✓ Download complete!")
        self._refresh_models()

    def _on_pull_failed(self, err: str):
        self.pull_btn.setEnabled(True)
        self.pull_progress.setVisible(False)
        self.pull_status.setStyleSheet("color: #f7768e;")
        self.pull_status.setText("✗ Download failed — see console for details.")

    def _save(self):
        self.cfg["ollama_url"] = self.ollama_url.text().strip()
        self.cfg["ollama_model"] = self.ollama_model.text().strip()
        self.cfg["openai_api_key"] = self.openai_key.text().strip()
        self.cfg["openai_model"] = self.openai_model.text().strip()
        self.cfg["openai_base_url"] = self.openai_base.text().strip()
        self.cfg["anthropic_api_key"] = self.an_key.text().strip()
        self.cfg["anthropic_model"] = self.an_model.text().strip()
        self.cfg["compat_api_key"] = self.compat_key.text().strip()
        self.cfg["compat_base_url"] = self.compat_base.text().strip()
        self.cfg["compat_model"] = self.compat_model.text().strip()
        config.save(self.cfg)
        QMessageBox.information(self, "Saved", "Settings saved.")


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
        title = QLabel("Conversion history")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        title_row.addWidget(title)
        title_row.addStretch()
        clear_btn = QPushButton("Clear history")
        clear_btn.clicked.connect(self._clear)
        title_row.addWidget(clear_btn)
        layout.addLayout(title_row)

        subtitle = QLabel("All conversions this session and across sessions. Most recent first.")
        subtitle.setStyleSheet("color: #8a909c;")
        layout.addWidget(subtitle)

        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        layout.addWidget(self.list, 1)

        self.summary = QLabel("")
        self.summary.setStyleSheet("color: #8a909c; font-size: 11px;")
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

        title = QLabel("pdf2md")
        title.setStyleSheet("font-size: 26px; font-weight: 700;")
        layout.addWidget(title)

        ver = QLabel(f"Version {version}  ·  PDF → Markdown converter")
        ver.setStyleSheet("color: #8a909c; font-size: 12px;")
        layout.addWidget(ver)

        tagline = QLabel(
            "A modern, multi-engine GUI for turning PDFs into clean Markdown — "
            "works fully offline or with any hosted LLM."
        )
        tagline.setWordWrap(True)
        tagline.setStyleSheet("font-size: 14px; padding-top: 8px; padding-bottom: 8px;")
        layout.addWidget(tagline)

        engines = QGroupBox("Conversion engines")
        eg = QVBoxLayout(engines)
        for line in (
            "• <b>Native</b> — offline, fast. PyMuPDF + pymupdf4llm.",
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
            "• Drag-and-drop batch conversion with file queue",
            "• Smart folder scanning — finds all PDFs recursively",
            "• Background worker thread — UI stays responsive",
            "• Per-page progress bar and live status messages",
            "• Embedded image extraction with relative paths (native engine)",
            "• Conversion history with timestamps, persisted across sessions",
            "• Ollama model management — preset tiers, download from UI",
            "• Dark and light themes",
            "• Persistent settings at <code>~/.pdf2md/config.json</code>",
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
            'href="https://github.com/Hesamsamani/pymupdfgui">'
            "github.com/Hesamsamani/pymupdfgui</a>"
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
        self.setWindowTitle("pdf2md — PDF to Markdown")
        self.resize(1150, 740)
        self.setMinimumSize(QSize(900, 600))
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
        sidebar.setFixedWidth(230)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        logo = QLabel("◆ pdf2md")
        logo.setObjectName("Logo")
        sb.addWidget(logo)
        sub = QLabel("PDF → Markdown converter")
        sub.setObjectName("Subtitle")
        sb.addWidget(sub)

        section = QLabel("NAVIGATION")
        section.setObjectName("SectionLabel")
        sb.addWidget(section)

        self.nav_buttons: list[QPushButton] = []
        for label, idx in [("Convert", 0), ("Engines", 1), ("History", 2), ("About", 3)]:
            b = QPushButton(f"  {label}")
            b.setObjectName("NavItem")
            b.setCheckable(True)
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
        self.settings_page = SettingsPage(self.cfg)
        self.history_page = HistoryPage()
        self.about_page = AboutPage()

        self.stack.addWidget(self.convert_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.about_page)

        # Refresh history tab when a conversion completes
        self.convert_page.conversion_done.connect(self.history_page.refresh)

        root.addWidget(self.stack, 1)

    def _switch(self, idx: int):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_buttons):
            b.setChecked(i == idx)

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
    app.setApplicationName("pdf2md")
    w = MainWindow(cfg)
    w.show()
    sys.exit(app.exec())
