# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
all style sheets
"""
from .icons import icon_path

icon_path_ = str(icon_path).replace("\\", "/")

MAIN_COLOUR = "#6272a4"  # main colour of the theme
COMP_COLOUR = "#b7cbc9"  # complementary colour of MAIN_COLOUR
COMP_COLOUR_2 = "#ca8fc0"
LIGHT_COLOUR = "#f8f8f2"  # #f8f8f2
DARK_COLOUR = "#4f5c84"
TEXT_COLOUR = "#1b124b"
TAB_STYLE = f"""
        QTabBar::tab{{
        border-left:4px solid {MAIN_COLOUR};
        padding:3ex;
        margin:0px}}
        QTabBar::tab:selected{{
        border-left:4px solid {COMP_COLOUR};
        background-color:{DARK_COLOUR}}}
        QTabBar::tab:hover{{
        border-left:4px solid {COMP_COLOUR_2};
        background-color:{COMP_COLOUR_2}}}
        QToolTip{{
        border:none;
        color:{TEXT_COLOUR};
        background-color:{LIGHT_COLOUR};
        font-size:9pt;
        font-family:Verdana,Microsoft YaHei UI,PingFang SC}}
        QTabWidget{{
        border:none;
        border-radius:5px;
        background-color:{MAIN_COLOUR}}}
        """
COMBO_BOX_STYLE = f"""
        QComboBox{{
        font-size:11pt;
        font-family:Verdana,Microsoft YaHei UI,PingFang SC;
        border-radius:5px;
        background-color:{MAIN_COLOUR};
        color:{LIGHT_COLOUR}}}
        QComboBox:hover{{
        border:none}}
        QComboBox::drop-down{{
        subcontrol-origin:padding;
        subcontrol-position:top right;
        width:25px; 
        border-left-width:3px;
        border-left-color:{MAIN_COLOUR};
        border-left-style:solid;
        border-top-right-radius:3px;
        border-bottom-right-radius:3px;	
        background-image:url({icon_path_}/chevron_down.svg);
        background-position:center;
        background-repeat:no-repeat}}
        QScrollBar:vertical{{
        background-color:{LIGHT_COLOUR};
        border:none;
        width:10px}}
        QScrollBar::handle:vertical{{
        background-color:{MAIN_COLOUR};
        border-radius:3px;
        min-height:45px}}
        """
TEXTEDIT_STYlE = f"""
        QTextEdit{{font-size:11pt;
        border-top-left-radius:5px;
        border-top-right-radius:5px;
        border-bottom-left-radius:0px;
        border-bottom-right-radius:0px;
        background-color:{MAIN_COLOUR};
        color:{LIGHT_COLOUR};
        font-family:Verdana,Microsoft YaHei UI,PingFang SC}}
        QScrollBar:vertical{{
        border:none;
        border-top-right-radius:4px;
        border-bottom-right-radius:0px;
        background-color:{MAIN_COLOUR};
        margin:0 0 0 0;
        width:8px}}
        QScrollBar::handle:vertical{{
        background-color:{COMP_COLOUR};
        border-radius:4px;
        min-height:45px}}
        QScrollBar:horizontal{{
        border:none;
        border-radius:0px;
        background-color:{MAIN_COLOUR};
        margin:0 0 0 0;
        width:5px}}
        QScrollBar::handle:horizontal{{
        background-color:{MAIN_COLOUR};
        border-radius:4px;
        min-width:45px}}
        """
LINE_EDIT_STYLE = f"""
        QLineEdit{{
        border:none;
        font-size:10pt;
        border-radius:10px;
        background-color:{MAIN_COLOUR};
        color:{LIGHT_COLOUR};
        font-family:Verdana,Microsoft YaHei UI,PingFang SC}}
        QLineEdit:focus{{
        border:2px solid {COMP_COLOUR}}}
        """
BUTTON_STYLE = f"""
        QPushButton{{
        border-radius:0px;
        background-color:transparent;
        image:url({icon_path_}/%s)}}
        QPushButton:hover{{
        image:url({icon_path_}/%s)}}
        QPushButton:pressed{{
        image:url({icon_path_}/%s)}}
        """
BUTTON_STYLE0 = f"""
        QPushButton{{
        border-radius:10px;
        background-color:transparent;
        image:url({icon_path_}/%s)}}
        QPushButton:hover{{
        background-color:#e2e2dd}}
        """
BUTTON_STYLE1 = f"""
        QPushButton{{
        border-radius:10px;
        background-color:transparent;
        image:url({icon_path_}/%s)}}
        QPushButton:hover{{
        background-color:#f25355;
        image:url({icon_path_}/%s)}}
        """
TABLE_STYLE1 = f"""
        QTableWidget{{
        border:none;
        background-color:transparent}}
        QTableWidget::item:selected{{
        background-color:transparent}}
        QScrollBar:vertical{{
        border:none;
        width:5px;
        background-color:{LIGHT_COLOUR}}}
        QScrollBar::handle:vertical{{
        background-color:#939393;
        border-radius:2px;
        min-height:45px}}
        """
TABLE_STYLE2 = f"""
        QTableWidget{{
        border-radius:10px;
        border:none;
        background-color:#adb6e0}}
        QTableWidget::item:selected{{
        background-color:#adb6e0}}
        QScrollBar:vertical{{
        background-color:{LIGHT_COLOUR};
        border:none;
        border-radius:1px;
        margin:21 0 21 0;
        width:5px}}
        QScrollBar::handle:vertical{{
        background-color:#939393;
        border-radius:2px;
        min-height:45px}}
        """
LABEL_STYLE = f"""
        QLabel{{
        border:none;
        border-radius:10px;
        font-size:8pt;
        font-family:Verdana,Microsoft YaHei UI,PingFang SC;
        color:{TEXT_COLOUR};
        background-color:transparent}}
        """
BGC_STYLE = f"""
        QWidget{{
        border:none;
        border-radius:0px;
        background-color:%s}}
        QToolTip{{
        border:none;
        color:{TEXT_COLOUR};
        background-color:{LIGHT_COLOUR};
        font-size:9pt;
        font-family:Verdana,Microsoft YaHei UI,PingFang SC}}
        """
SWITCH_STYLE = f"""
        SwitchBtn:on{{
        background-color:{MAIN_COLOUR};
        color:{LIGHT_COLOUR}}}
        SwitchBtn:off{{
        background-color:#e2e2dd;
        color:#8d90a4}}
        """
SCROLL_AREA_STYlE = f"""
        QScrollArea{{
        border:none;
        background-color:transparent}}
        QScrollBar:horizontal{{
        border:none;
        background:{MAIN_COLOUR};
        height:8px;
        margin:0px 21px 0 21px;
        border-radius:0px}}
        QScrollBar::handle:horizontal{{
        background:{COMP_COLOUR};
        min-width:25px;
        border-radius:0px}}
        QScrollBar::add-line:horizontal{{
        border:none;
        background:{MAIN_COLOUR};
        width:20px;
        border-top-right-radius:4px;
        border-bottom-right-radius:4px;
        subcontrol-position:right;
        subcontrol-origin:margin}}
        QScrollBar::sub-line:horizontal{{
        border:none;
        background:{MAIN_COLOUR};
        width:20px;
        border-top-left-radius:4px;
        border-bottom-left-radius:4px;
        subcontrol-position:left;
        subcontrol-origin:margin}}
        QScrollBar::up-arrow:horizontal,QScrollBar::down-arrow:horizontal{{
        background:none}}
        QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{{
        background:none}}
        QScrollBar:vertical{{
        border:none;
        background-color:{MAIN_COLOUR};
        width:8px;
        margin:21px 0 21px 0;
        border-radius:0px}}
        QScrollBar::handle:vertical{{
        background:{COMP_COLOUR};
        min-height:25px;
        border-radius:0px}}
        QScrollBar::add-line:vertical{{
        border:none;
        background:{MAIN_COLOUR};
        height:20px;
        border-bottom-left-radius:4px;
        border-bottom-right-radius:4px;
        subcontrol-position:bottom;
        subcontrol-origin:margin}}
        QScrollBar::sub-line:vertical{{
        border:none;
        background:{MAIN_COLOUR};
        height:20px;
        border-top-left-radius:4px;
        border-top-right-radius:4px;
        subcontrol-position:top;
        subcontrol-origin:margin}}
        QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{{
        background:none}}
        QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{{
        background:none}}
        """
