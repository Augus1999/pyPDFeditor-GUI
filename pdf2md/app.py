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
)

from . import config, converters, styles


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

class ConvertWorker(QThread):
    progress = pyqtSignal(int, int, str)
    finished_ok = pyqtSignal(str, str)  # (markdown, source pdf)
    failed = pyqtSignal(str, str)  # (source pdf, error)

    def __init__(self, pdf: Path, cfg: dict, image_dir: Path | None):
        super().__init__()
        self.pdf = pdf
        self.cfg = cfg
        self.image_dir = image_dir

    def run(self) -> None:
        try:
            opts = converters.ConvertOptions(
                include_images=self.cfg.get("include_images", True),
                page_separator=self.cfg.get("page_separator", True),
                image_dir=self.image_dir,
            )
            cb = lambda c, t, m: self.progress.emit(c, t, m)
            engine = self.cfg.get("engine", "native")
            if engine == "native":
                md = converters.convert_native(self.pdf, opts, cb)
            elif engine == "ollama":
                md = converters.convert_ollama(
                    self.pdf,
                    self.cfg["ollama_url"],
                    self.cfg["ollama_model"],
                    opts,
                    cb,
                )
            elif engine == "openai":
                md = converters.convert_openai_compatible(
                    self.pdf,
                    self.cfg["openai_base_url"],
                    self.cfg["openai_api_key"],
                    self.cfg["openai_model"],
                    opts,
                    cb,
                )
            elif engine == "anthropic":
                md = converters.convert_anthropic(
                    self.pdf,
                    self.cfg["anthropic_api_key"],
                    self.cfg["anthropic_model"],
                    opts,
                    cb,
                )
            elif engine == "openai_compatible":
                md = converters.convert_openai_compatible(
                    self.pdf,
                    self.cfg["compat_base_url"],
                    self.cfg["compat_api_key"],
                    self.cfg["compat_model"],
                    opts,
                    cb,
                )
            else:
                raise ValueError(f"Unknown engine: {engine}")
            self.finished_ok.emit(md, str(self.pdf))
        except Exception:
            self.failed.emit(str(self.pdf), traceback.format_exc())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_icon(color: str, glyph: str) -> QIcon:
    """Build a tiny round glyph icon procedurally — no asset files needed."""
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
# Pages
# ---------------------------------------------------------------------------

class ConvertPage(QWidget):
    def __init__(self, cfg: dict, status: QStatusBar, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.status = status
        self.queue: list[Path] = []
        self.worker: ConvertWorker | None = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("PDF → Markdown")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        subtitle = QLabel("Drop files, pick an engine, hit convert.")
        subtitle.setStyleSheet("color: #8a909c;")
        layout.addWidget(subtitle)

        # File picker row
        file_row = QHBoxLayout()
        self.pick_btn = QPushButton(" Add PDFs")
        self.pick_btn.setIcon(_make_icon("#7aa2f7", "+"))
        self.pick_btn.clicked.connect(self.pick_files)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_queue)
        file_row.addWidget(self.pick_btn)
        file_row.addWidget(self.clear_btn)
        file_row.addStretch()
        layout.addLayout(file_row)

        self.list = QListWidget()
        self.list.setAcceptDrops(True)
        self.list.setMinimumHeight(160)
        self.setAcceptDrops(True)
        layout.addWidget(self.list, 1)

        # Engine + options row
        opts_box = QGroupBox("Conversion options")
        opts_layout = QFormLayout(opts_box)
        self.engine_combo = QComboBox()
        self.engine_combo.addItem("Native (offline, PyMuPDF)", "native")
        self.engine_combo.addItem("Ollama (local LLM)", "ollama")
        self.engine_combo.addItem("OpenAI", "openai")
        self.engine_combo.addItem("Anthropic Claude", "anthropic")
        self.engine_combo.addItem("OpenAI-compatible (Groq, OpenRouter, LM Studio...)", "openai_compatible")
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

        # Progress + convert
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

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
            if p.suffix.lower() == ".pdf" and p.exists():
                self._add(p)

    def _add(self, p: Path):
        if p in self.queue:
            return
        self.queue.append(p)
        item = QListWidgetItem(f"  {p.name}    —    {p.parent}")
        item.setData(Qt.ItemDataRole.UserRole, str(p))
        self.list.addItem(item)

    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Pick PDFs", str(Path.home()), "PDF files (*.pdf)"
        )
        for f in files:
            self._add(Path(f))

    def clear_queue(self):
        self.queue.clear()
        self.list.clear()

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
        self.convert_btn.setEnabled(False)
        self._convert_next()

    def _convert_next(self):
        if not self._remaining:
            self.convert_btn.setEnabled(True)
            self.status.showMessage("All done.", 6000)
            self.progress.setValue(100)
            return
        pdf = self._remaining.pop(0)
        img_dir = self._out_dir / f"{pdf.stem}_images" if self.cfg.get("include_images") else None
        self.worker = ConvertWorker(pdf, dict(self.cfg), img_dir)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self._on_done)
        self.worker.failed.connect(self._on_failed)
        self.worker.start()

    def _on_progress(self, cur: int, total: int, msg: str):
        self.progress.setValue(int(cur / max(total, 1) * 100))
        self.status.showMessage(msg)

    def _on_done(self, md: str, src: str):
        src_path = Path(src)
        out = self._out_dir / f"{src_path.stem}.md"
        out.write_text(md, encoding="utf-8")
        self.status.showMessage(f"Wrote {out}", 4000)
        self._convert_next()

    def _on_failed(self, src: str, err: str):
        QMessageBox.critical(self, "Conversion failed", f"{Path(src).name}\n\n{err}")
        self._convert_next()


class SettingsPage(QWidget):
    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Engine settings")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        # Ollama
        olm = QGroupBox("Ollama (offline, local)")
        f = QFormLayout(olm)
        self.ollama_url = QLineEdit(self.cfg["ollama_url"])
        self.ollama_model = QLineEdit(self.cfg["ollama_model"])
        test_btn = QPushButton("Test connection")
        test_btn.clicked.connect(self._test_ollama)
        self.ollama_status = QLabel("")
        f.addRow("Server URL:", self.ollama_url)
        f.addRow("Model:", self.ollama_model)
        f.addRow("", test_btn)
        f.addRow("", self.ollama_status)
        layout.addWidget(olm)

        # OpenAI
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

        # Anthropic
        an = QGroupBox("Anthropic Claude")
        af = QFormLayout(an)
        self.an_key = QLineEdit(self.cfg["anthropic_api_key"])
        self.an_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.an_model = QLineEdit(self.cfg["anthropic_model"])
        af.addRow("API key:", self.an_key)
        af.addRow("Model:", self.an_model)
        layout.addWidget(an)

        # Custom OpenAI-compatible
        cm = QGroupBox("Custom (OpenAI-compatible: Groq, OpenRouter, LM Studio, vLLM, ...)")
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

    def _test_ollama(self):
        url = self.ollama_url.text().strip()
        models = converters.list_ollama_models(url)
        if models:
            self.ollama_status.setObjectName("StatusOk")
            self.ollama_status.setText(f"✓ Connected — {len(models)} models: " + ", ".join(models[:5]))
        else:
            self.ollama_status.setObjectName("StatusErr")
            self.ollama_status.setText("✗ Unreachable. Is `ollama serve` running?")
        self.ollama_status.style().unpolish(self.ollama_status)
        self.ollama_status.style().polish(self.ollama_status)


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        title = QLabel("pdf2md")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        layout.addWidget(title)
        desc = QLabel(
            "Convert PDF files to clean Markdown using multiple engines:\n\n"
            "• Native: offline, fast, PyMuPDF-based heuristics.\n"
            "• Ollama: local vision-capable LLMs (llama3.2-vision, llava, ...).\n"
            "• OpenAI / Anthropic: hosted vision models.\n"
            "• Custom OpenAI-compatible: Groq, OpenRouter, LM Studio, vLLM.\n\n"
            "Drag-and-drop PDFs, batch convert, embedded image extraction.\n"
            "Built on PyQt6 + PyMuPDF."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #8a909c; font-size: 13px; line-height: 1.6;")
        layout.addWidget(desc)
        layout.addStretch()


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, cfg: dict):
        super().__init__()
        self.cfg = cfg
        self.setWindowTitle("pdf2md — PDF to Markdown")
        self.resize(1100, 720)
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
        sidebar.setFixedWidth(220)
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
        for label, idx in [("Convert", 0), ("Engines", 1), ("About", 2)]:
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
        self.about_page = AboutPage()
        self.stack.addWidget(self.convert_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.about_page)
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
