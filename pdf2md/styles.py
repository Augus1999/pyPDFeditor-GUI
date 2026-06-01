# -*- coding: utf-8 -*-
"""Modern stylesheets for pdf2md."""

DARK = """
* { font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", sans-serif; font-size: 13px; }
QMainWindow, QWidget { background-color: #1b1d23; color: #e6e9ef; }

QFrame#Sidebar { background-color: #15171c; border-right: 1px solid #2a2d35; }
QLabel#Logo { color: #7aa2f7; font-size: 18px; font-weight: 700; padding: 14px; }
QLabel#Subtitle { color: #8a909c; padding-left: 14px; padding-bottom: 14px; font-size: 11px; }
QLabel#SectionLabel { color: #8a909c; font-size: 11px; font-weight: 600; padding: 14px 14px 4px 14px; text-transform: uppercase; letter-spacing: 0.5px; }

QPushButton {
    background-color: #2a2d35;
    color: #e6e9ef;
    border: 1px solid #353944;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 500;
}
QPushButton:hover { background-color: #353944; border-color: #4a4f5c; }
QPushButton:pressed { background-color: #1f222a; }
QPushButton:disabled { color: #555a66; background-color: #22252c; }

QPushButton#Primary {
    background-color: #7aa2f7;
    color: #15171c;
    border: none;
    font-weight: 600;
}
QPushButton#Primary:hover { background-color: #93b3f8; }
QPushButton#Primary:disabled { background-color: #3a4258; color: #8a909c; }

QPushButton#Accent {
    background-color: #9ece6a;
    color: #15171c;
    border: none;
    font-weight: 600;
}
QPushButton#Accent:hover { background-color: #b1d97e; }

QPushButton#NavItem {
    text-align: left;
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    margin: 1px 8px;
    color: #c0c6d2;
}
QPushButton#NavItem:hover { background-color: #22252c; }
QPushButton#NavItem:checked { background-color: #2a3148; color: #7aa2f7; }

QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {
    background-color: #22252c;
    border: 1px solid #353944;
    border-radius: 6px;
    padding: 6px 8px;
    color: #e6e9ef;
    selection-background-color: #7aa2f7;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus { border-color: #7aa2f7; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView { background-color: #22252c; border: 1px solid #353944; selection-background-color: #2a3148; }

QListWidget {
    background-color: #1b1d23;
    border: 1px solid #2a2d35;
    border-radius: 8px;
    padding: 4px;
}
QListWidget::item { padding: 8px; border-radius: 6px; }
QListWidget::item:hover { background-color: #22252c; }
QListWidget::item:selected { background-color: #2a3148; color: #7aa2f7; }

QProgressBar {
    background-color: #22252c;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk { background-color: #7aa2f7; border-radius: 4px; }

QGroupBox {
    border: 1px solid #2a2d35;
    border-radius: 10px;
    margin-top: 16px;
    padding: 14px;
    font-weight: 600;
}
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; color: #8a909c; }

QLabel#StatusOk { color: #9ece6a; }
QLabel#StatusErr { color: #f7768e; }
QLabel#StatusWarn { color: #e0af68; }

QCheckBox { padding: 4px; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid #4a4f5c;
    border-radius: 4px;
    background-color: #22252c;
}
QCheckBox::indicator:checked { background-color: #7aa2f7; border-color: #7aa2f7; }

QStatusBar { background-color: #15171c; color: #8a909c; border-top: 1px solid #2a2d35; }

QScrollBar:vertical { background: #1b1d23; width: 10px; }
QScrollBar::handle:vertical { background: #353944; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #4a4f5c; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }
"""

LIGHT = """
* { font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", sans-serif; font-size: 13px; }
QMainWindow, QWidget { background-color: #f7f8fb; color: #1f2430; }

QFrame#Sidebar { background-color: #ffffff; border-right: 1px solid #e3e6ec; }
QLabel#Logo { color: #3b6dd6; font-size: 18px; font-weight: 700; padding: 14px; }
QLabel#Subtitle { color: #6b7280; padding-left: 14px; padding-bottom: 14px; font-size: 11px; }
QLabel#SectionLabel { color: #6b7280; font-size: 11px; font-weight: 600; padding: 14px 14px 4px 14px; text-transform: uppercase; letter-spacing: 0.5px; }

QPushButton {
    background-color: #ffffff;
    color: #1f2430;
    border: 1px solid #d6dae3;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 500;
}
QPushButton:hover { background-color: #f0f2f7; border-color: #b5bcc9; }
QPushButton:pressed { background-color: #e3e6ec; }

QPushButton#Primary {
    background-color: #3b6dd6;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#Primary:hover { background-color: #4f7ee0; }

QPushButton#Accent {
    background-color: #2eb872;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#Accent:hover { background-color: #43c684; }

QPushButton#NavItem {
    text-align: left;
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    margin: 1px 8px;
    color: #4b5563;
}
QPushButton#NavItem:hover { background-color: #f0f2f7; }
QPushButton#NavItem:checked { background-color: #e6edfc; color: #3b6dd6; }

QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #d6dae3;
    border-radius: 6px;
    padding: 6px 8px;
    color: #1f2430;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus { border-color: #3b6dd6; }

QListWidget { background-color: #ffffff; border: 1px solid #e3e6ec; border-radius: 8px; padding: 4px; }
QListWidget::item { padding: 8px; border-radius: 6px; }
QListWidget::item:selected { background-color: #e6edfc; color: #3b6dd6; }

QProgressBar { background-color: #e3e6ec; border: none; border-radius: 4px; height: 8px; }
QProgressBar::chunk { background-color: #3b6dd6; border-radius: 4px; }

QGroupBox {
    border: 1px solid #e3e6ec;
    border-radius: 10px;
    margin-top: 16px;
    padding: 14px;
    font-weight: 600;
}
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; color: #6b7280; }

QStatusBar { background-color: #ffffff; color: #6b7280; border-top: 1px solid #e3e6ec; }
"""
