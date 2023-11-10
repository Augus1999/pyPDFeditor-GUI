# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
core of pyPDFeditor-GUI
"""
import os
import sys
import platform
import fitz
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from .application import reset, remove, Main, app_home

if not os.path.exists(app_home):
    os.makedirs(app_home)

__system__ = platform.system()
__author__ = "Nianze A. TAO (Omozawa SUENO)"
__version__ = "2.2.7"
__all__ = ["main", "reset", "remove"]


def main(
    system: str = __system__, version: str = __version__, debug: bool = False
) -> None:
    """
    main function

    :param system: system name
    :param version: version name
    :param debug: whether display mupdf errors or not
    :return: None
    """
    a = QApplication([])
    s = a.desktop().screenGeometry()
    screen_w, screen_h = s.width(), s.height()  # get screen info
    del s, a  # delete QApplication object so that it won't affect the following codes
    if screen_w > 1920 and screen_h > 1080:
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    fitz.TOOLS.mupdf_display_errors(debug)
    app = QApplication(sys.argv)
    main_app = Main(system, version)
    main_app.show()
    sys.exit(app.exec())


# --------------完成！2021年八月十日に--------------
