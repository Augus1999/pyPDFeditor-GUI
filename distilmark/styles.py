# -*- coding: utf-8 -*-
"""Stylesheets for Distilmark.

Design system (generated with the ui-ux-pro-max design intelligence skill):
  • Style      : Dark Mode (OLED) — deep surfaces, high contrast (WCAG AAA target)
  • Brand/blue : #2563eb  (navigation, focus, selection, secondary CTA)
  • Action CTA : #f97316  (orange — the single primary action: Convert)
  • Typeface   : Inter (falls back to Segoe UI Variable / Segoe UI)
  • Motion     : not expressible in QSS, but states stay visually distinct
"""

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
# Brand blue   #2563eb  hover #3b82f6  pressed #1d4ed8  subtle #1b2740
# Action orange#f97316  hover #fb8a3c  pressed #ea6a06
# Semantics    ok #22c55e   warn #f59e0b   danger #ef4444
# Dark surfaces bg #0c0e13  rail #08090d  card #12151d  input #161a22
# Borders      #1e232d / #2a3140    Text #e7eaf0  muted #8b93a5

_FONT = '"Inter", "Segoe UI Variable", "Segoe UI", "SF Pro Text", sans-serif'

DARK = f"""
* {{ font-family: {_FONT}; font-size: 13px; }}
QMainWindow, QWidget {{ background-color: #0c0e13; color: #e7eaf0; }}

/* ---- Sidebar rail ---- */
QFrame#Sidebar {{ background-color: #08090d; border-right: 1px solid #1a1e27; }}
QLabel#Logo {{ color: #ffffff; font-size: 20px; font-weight: 800; padding: 20px 18px 0 18px; }}
QLabel#Subtitle {{ color: #6b7280; padding: 2px 18px 18px 18px; font-size: 11px; }}
QLabel#SectionLabel {{
    color: #545b6a; font-size: 10px; font-weight: 700;
    padding: 18px 18px 8px 18px; letter-spacing: 1.4px;
}}

/* ---- Buttons (secondary / default) ---- */
QPushButton {{
    background-color: #181c25;
    color: #e7eaf0;
    border: 1px solid #262c38;
    border-radius: 10px;
    padding: 9px 16px;
    font-weight: 500;
}}
QPushButton:hover {{ background-color: #20262f; border-color: #38404e; }}
QPushButton:pressed {{ background-color: #12151d; }}
QPushButton:disabled {{ color: #495061; background-color: #12151d; border-color: #1a1e27; }}

/* ---- Primary action: Convert (orange CTA, one per screen) ---- */
QPushButton#Primary {{
    background-color: #f97316;
    color: #1a0f02;
    border: none;
    font-weight: 800;
    padding: 11px 26px;
}}
QPushButton#Primary:hover {{ background-color: #fb8a3c; }}
QPushButton#Primary:pressed {{ background-color: #ea6a06; }}
QPushButton#Primary:disabled {{ background-color: #4a3520; color: #8a704f; }}

/* ---- Brand action (blue): Save settings etc. ---- */
QPushButton#Accent {{
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    font-weight: 700;
}}
QPushButton#Accent:hover {{ background-color: #3b82f6; }}
QPushButton#Accent:pressed {{ background-color: #1d4ed8; }}

QPushButton#Ghost {{ background: transparent; border: 1px solid #2a3140; color: #aab1c0; }}
QPushButton#Ghost:hover {{ background-color: #181c25; color: #e7eaf0; }}

QPushButton#Danger {{ background: transparent; border: 1px solid #5a2330; color: #f87171; }}
QPushButton#Danger:hover {{ background-color: #2a1117; border-color: #ef4444; color: #fca5a5; }}
QPushButton#Danger:disabled {{ color: #495061; border-color: #1a1e27; }}

/* ---- Nav items & collapsible toggles ---- */
QPushButton#NavItem {{
    text-align: left;
    background: transparent;
    border: none;
    border-radius: 10px;
    padding: 11px 14px;
    margin: 2px 12px;
    color: #aab1c0;
    font-weight: 500;
}}
QPushButton#NavItem:hover {{ background-color: #14171f; color: #e7eaf0; }}
QPushButton#NavItem:checked {{ background-color: #16233f; color: #60a5fa; font-weight: 700; }}

/* ---- Inputs ---- */
QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {{
    background-color: #161a22;
    border: 1px solid #262c38;
    border-radius: 9px;
    padding: 8px 11px;
    color: #e7eaf0;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
QTextEdit:focus, QPlainTextEdit:focus {{ border-color: #2563eb; }}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{ border-color: #38404e; }}

QComboBox::drop-down {{ border: none; width: 26px; }}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #8b93a5;
    margin-right: 11px;
}}
QComboBox QAbstractItemView {{
    background-color: #161a22;
    border: 1px solid #262c38;
    border-radius: 9px;
    selection-background-color: #16233f;
    selection-color: #60a5fa;
    padding: 5px;
    outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 18px; border: none; background: #181c25; }}
QSpinBox::up-button {{ border-top-right-radius: 9px; }}
QSpinBox::down-button {{ border-bottom-right-radius: 9px; }}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: #262c38; }}
QSpinBox::up-arrow {{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #8b93a5; }}
QSpinBox::down-arrow {{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #8b93a5; }}

/* ---- Lists ---- */
QListWidget {{
    background-color: #0a0c11;
    border: 1px solid #1a1e27;
    border-radius: 13px;
    padding: 6px;
    outline: none;
}}
QListWidget::item {{ padding: 11px; border-radius: 9px; color: #c3c9d6; }}
QListWidget::item:hover {{ background-color: #14171f; }}
QListWidget::item:selected {{ background-color: #16233f; color: #60a5fa; }}
QListWidget::item:alternate {{ background-color: #0d1016; }}

/* ---- Tree (Courses library) ---- */
QTreeWidget, QTreeView {{
    background-color: #0a0c11;
    alternate-background-color: #0e1118;
    border: 1px solid #1a1e27;
    border-radius: 13px;
    padding: 4px;
    outline: none;
}}
QTreeWidget::item, QTreeView::item {{ padding: 6px 4px; color: #c3c9d6; border-radius: 6px; }}
QTreeWidget::item:hover, QTreeView::item:hover {{ background-color: #14171f; }}
QTreeWidget::item:selected, QTreeView::item:selected {{ background-color: #16233f; color: #e7eaf0; }}
QHeaderView::section {{
    background-color: #11141b;
    color: #8b93a5;
    padding: 7px 10px;
    border: none;
    border-bottom: 1px solid #1a1e27;
    font-weight: 700;
}}
QTreeWidget::branch {{ background: transparent; }}

/* ---- Progress ---- */
QProgressBar {{
    background-color: #161a22;
    border: none;
    border-radius: 6px;
    height: 10px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{ border-radius: 6px; background-color: #2563eb; }}

/* ---- Group boxes (cards) ---- */
QGroupBox {{
    background-color: #11141b;
    border: 1px solid #1a1e27;
    border-radius: 15px;
    margin-top: 18px;
    padding: 18px 16px 14px 16px;
    font-weight: 700;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 16px;
    top: 2px;
    padding: 2px 9px;
    color: #60a5fa;
    background-color: #0c0e13;
    border-radius: 7px;
}}

/* ---- Tabs (Preview) ---- */
QTabWidget::pane {{ border: 1px solid #1a1e27; border-radius: 13px; top: -1px; background: #0a0c11; }}
QTabBar::tab {{
    background: transparent; color: #8b93a5; padding: 10px 18px; margin-right: 4px; border: none;
    border-top-left-radius: 10px; border-top-right-radius: 10px; font-weight: 600;
}}
QTabBar::tab:hover {{ color: #e7eaf0; background: #14171f; }}
QTabBar::tab:selected {{ color: #60a5fa; background: #16233f; }}

/* ---- Status text helpers ---- */
QLabel#StatusOk {{ color: #22c55e; }}
QLabel#StatusErr {{ color: #f87171; }}
QLabel#StatusWarn {{ color: #fbbf24; }}
QLabel#Hint {{ color: #6b7280; font-size: 11px; }}
QLabel#H1 {{ font-size: 24px; font-weight: 800; color: #f4f6fa; }}
QLabel#H2 {{ color: #6b7280; font-size: 13px; }}

/* ---- Checkboxes ---- */
QCheckBox {{ padding: 5px; spacing: 9px; color: #c3c9d6; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border: 1px solid #38404e; border-radius: 5px; background-color: #161a22;
}}
QCheckBox::indicator:hover {{ border-color: #2563eb; }}
QCheckBox::indicator:checked {{ background-color: #2563eb; border-color: #2563eb; }}

/* ---- Status bar ---- */
QStatusBar {{ background-color: #08090d; color: #8b93a5; border-top: 1px solid #1a1e27; }}
QStatusBar::item {{ border: none; }}

/* ---- Tooltips ---- */
QToolTip {{ background-color: #16233f; color: #e7eaf0; border: 1px solid #38404e; border-radius: 7px; padding: 6px 10px; }}

/* ---- Scrollbars ---- */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 12px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: #262c38; border-radius: 5px; min-height: 36px; }}
QScrollBar::handle:vertical:hover {{ background: #38404e; }}
QScrollBar:horizontal {{ background: transparent; height: 12px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: #262c38; border-radius: 5px; min-width: 36px; }}
QScrollBar::handle:horizontal:hover {{ background: #38404e; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
"""

LIGHT = f"""
* {{ font-family: {_FONT}; font-size: 13px; }}
QMainWindow, QWidget {{ background-color: #f6f7fb; color: #1e2230; }}

QFrame#Sidebar {{ background-color: #ffffff; border-right: 1px solid #e6e8f0; }}
QLabel#Logo {{ color: #161a26; font-size: 20px; font-weight: 800; padding: 20px 18px 0 18px; }}
QLabel#Subtitle {{ color: #8a90a0; padding: 2px 18px 18px 18px; font-size: 11px; }}
QLabel#SectionLabel {{ color: #9aa0b0; font-size: 10px; font-weight: 700; padding: 18px 18px 8px 18px; letter-spacing: 1.4px; }}

QPushButton {{
    background-color: #ffffff; color: #1e2230; border: 1px solid #d8dbe6;
    border-radius: 10px; padding: 9px 16px; font-weight: 500;
}}
QPushButton:hover {{ background-color: #eef0f6; border-color: #c2c7d4; }}
QPushButton:pressed {{ background-color: #e2e5ee; }}
QPushButton:disabled {{ color: #aab0be; background-color: #f0f1f6; }}

QPushButton#Primary {{
    background-color: #f97316; color: #ffffff; border: none; font-weight: 800; padding: 11px 26px;
}}
QPushButton#Primary:hover {{ background-color: #fb8a3c; }}
QPushButton#Primary:pressed {{ background-color: #ea6a06; }}
QPushButton#Primary:disabled {{ background-color: #f6c79e; color: #ffffff; }}

QPushButton#Accent {{ background-color: #2563eb; color: #ffffff; border: none; font-weight: 700; }}
QPushButton#Accent:hover {{ background-color: #3b82f6; }}
QPushButton#Accent:pressed {{ background-color: #1d4ed8; }}

QPushButton#Ghost {{ background: transparent; border: 1px solid #d8dbe6; color: #4b5263; }}
QPushButton#Ghost:hover {{ background-color: #eef0f6; color: #1e2230; }}

QPushButton#Danger {{ background: transparent; border: 1px solid #f3c2cb; color: #dc2626; }}
QPushButton#Danger:hover {{ background-color: #fdeef1; border-color: #dc2626; }}
QPushButton#Danger:disabled {{ color: #aab0be; border-color: #e6e8f0; }}

QPushButton#NavItem {{
    text-align: left; background: transparent; border: none; border-radius: 10px;
    padding: 11px 14px; margin: 2px 12px; color: #4b5263; font-weight: 500;
}}
QPushButton#NavItem:hover {{ background-color: #eef0f6; color: #1e2230; }}
QPushButton#NavItem:checked {{ background-color: #e3edfd; color: #1d4ed8; font-weight: 700; }}

QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {{
    background-color: #ffffff; border: 1px solid #d8dbe6; border-radius: 9px; padding: 8px 11px;
    color: #1e2230; selection-background-color: #2563eb; selection-color: #ffffff;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QPlainTextEdit:focus {{ border-color: #2563eb; }}
QComboBox::drop-down {{ border: none; width: 26px; }}
QComboBox::down-arrow {{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #8a90a0; margin-right: 11px; }}
QComboBox QAbstractItemView {{
    background-color: #ffffff; border: 1px solid #d8dbe6; border-radius: 9px;
    selection-background-color: #e3edfd; selection-color: #1d4ed8; padding: 5px; outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 18px; border: none; background: #f0f1f6; }}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: #e2e5ee; }}
QSpinBox::up-arrow {{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 5px solid #8a90a0; }}
QSpinBox::down-arrow {{ border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #8a90a0; }}

QListWidget {{ background-color: #ffffff; border: 1px solid #e6e8f0; border-radius: 13px; padding: 6px; outline: none; }}
QListWidget::item {{ padding: 11px; border-radius: 9px; color: #3b4252; }}
QListWidget::item:hover {{ background-color: #eef0f6; }}
QListWidget::item:selected {{ background-color: #e3edfd; color: #1d4ed8; }}
QListWidget::item:alternate {{ background-color: #f7f8fc; }}

QTreeWidget, QTreeView {{
    background-color: #ffffff;
    alternate-background-color: #f4f6fb;
    border: 1px solid #e6e8f0; border-radius: 13px; padding: 4px; outline: none;
}}
QTreeWidget::item, QTreeView::item {{ padding: 6px 4px; color: #3b4252; border-radius: 6px; }}
QTreeWidget::item:hover, QTreeView::item:hover {{ background-color: #eef0f6; }}
QTreeWidget::item:selected, QTreeView::item:selected {{ background-color: #e3edfd; color: #1d4ed8; }}
QHeaderView::section {{
    background-color: #f0f1f6; color: #6b7280; padding: 7px 10px; border: none;
    border-bottom: 1px solid #e6e8f0; font-weight: 700;
}}

QProgressBar {{ background-color: #e6e8f0; border: none; border-radius: 6px; height: 10px; text-align: center; color: transparent; }}
QProgressBar::chunk {{ background-color: #2563eb; border-radius: 6px; }}

QGroupBox {{
    background-color: #ffffff; border: 1px solid #e6e8f0; border-radius: 15px;
    margin-top: 18px; padding: 18px 16px 14px 16px; font-weight: 700;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 16px; top: 2px; padding: 2px 9px; color: #1d4ed8; background-color: #f6f7fb; border-radius: 7px; }}

QTabWidget::pane {{ border: 1px solid #e6e8f0; border-radius: 13px; top: -1px; background: #ffffff; }}
QTabBar::tab {{
    background: transparent; color: #8a90a0; padding: 10px 18px; margin-right: 4px; border: none;
    border-top-left-radius: 10px; border-top-right-radius: 10px; font-weight: 600;
}}
QTabBar::tab:hover {{ color: #1e2230; background: #eef0f6; }}
QTabBar::tab:selected {{ color: #1d4ed8; background: #e3edfd; }}

QLabel#StatusOk {{ color: #16a34a; }}
QLabel#StatusErr {{ color: #dc2626; }}
QLabel#StatusWarn {{ color: #d97706; }}
QLabel#Hint {{ color: #8a90a0; font-size: 11px; }}
QLabel#H1 {{ font-size: 24px; font-weight: 800; color: #161a26; }}
QLabel#H2 {{ color: #8a90a0; font-size: 13px; }}

QCheckBox {{ padding: 5px; spacing: 9px; color: #3b4252; }}
QCheckBox::indicator {{ width: 18px; height: 18px; border: 1px solid #c2c7d4; border-radius: 5px; background-color: #ffffff; }}
QCheckBox::indicator:hover {{ border-color: #2563eb; }}
QCheckBox::indicator:checked {{ background-color: #2563eb; border-color: #2563eb; }}

QStatusBar {{ background-color: #ffffff; color: #8a90a0; border-top: 1px solid #e6e8f0; }}
QStatusBar::item {{ border: none; }}

QToolTip {{ background-color: #1e2230; color: #ffffff; border: none; border-radius: 7px; padding: 6px 10px; }}

QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 12px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: #d8dbe6; border-radius: 5px; min-height: 36px; }}
QScrollBar::handle:vertical:hover {{ background: #c2c7d4; }}
QScrollBar:horizontal {{ background: transparent; height: 12px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: #d8dbe6; border-radius: 5px; min-width: 36px; }}
QScrollBar::handle:horizontal:hover {{ background: #c2c7d4; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}
"""
