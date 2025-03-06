# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
core of pyPDFeditor-GUI
"""
import os
import sys
import platform
import pymupdf
from PyQt6.QtWidgets import QApplication
from .application import reset, remove, Main, app_home

if not os.path.exists(app_home):
    os.makedirs(app_home)

__system__ = platform.system()
__author__ = "Nianze A. TAO (Omozawa SUENO)"
__version__ = "3.0.9"
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
    if system == "Windows":
        os.environ["QT_FONT_DPI"] = "96"
    pymupdf.TOOLS.mupdf_display_errors(debug)
    app = QApplication(sys.argv)
    main_app = Main(system, version)
    main_app.show()
    sys.exit(app.exec())


# --------------完成！2021年八月十日に--------------
