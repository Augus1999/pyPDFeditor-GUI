# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5 import (
    QtWidgets,
    QtGui,
)
from .styleSheets import TAB_STYLE

TAB_L = {
    "English": ['Merge PDF', 'Organise', 'Security', 'Metadata'],
    "中文": ['合并文檔', '分割頁面', '檔案保護', '元數據'],
    "日本語": ['ファイル結合', 'ページオルガナイズ', '電子透かし', 'メタデータ']
}
FONT_F = {
    "English": [10, 'calibri'],  # calibri
    "中文": [9, 'Microsoft YaHei'],  # Microsoft YaHei
    "日本語": [9, 'Microsoft YaHei']  # Microsoft YaHei
}


def set_language(widget: QtWidgets.QWidget) -> None:
    """
    set language

    :param widget: QWidget -> self
    :return: None
    """
    widget.addTab(
        widget.tab1,
        QtGui.QIcon('ico\\merge.svg'),
        TAB_L[widget.language][0],
    )
    widget.addTab(
        widget.tab2,
        QtGui.QIcon('ico\\edit.svg'),
        TAB_L[widget.language][1],
    )
    widget.addTab(
        widget.tab3,
        QtGui.QIcon('ico\\lock.svg'),
        TAB_L[widget.language][2],
    )
    widget.addTab(
        widget.tab4,
        QtGui.QIcon('ico\\metadata.svg'),
        TAB_L[widget.language][3],
    )
    widget.setStyleSheet(
        TAB_STYLE.format(
            FONT_F[widget.language][0],
            FONT_F[widget.language][1],
        ),
    )
