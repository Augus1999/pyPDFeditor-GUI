# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5 import (
    QtWidgets,
    QtGui,
)
from .styleSheets import TAB_STYLE
from .basics import (
    FONT_F,
    TAB_L,
)


def set_language(widget: QtWidgets.QWidget):
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
