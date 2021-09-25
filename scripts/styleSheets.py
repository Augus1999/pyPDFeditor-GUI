# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
TAB_STYLE = '''
        QTabBar::tab{
        border:none;
        padding:3ex;
        margin:0px}
        QTabBar::tab:selected{
        border-left:4px solid #b7cbc9;
        background-color:#4f5c84}
        QTabBar::tab:hover{
        border:none;
        background-color:#ca8fc0}
        QToolTip{
        border:none;
        color:#3c3c3c;
        background-color:#ffffff;
        font-size:9pt;
        font-family:Verdana,Microsoft YaHei UI}
        QTabWidget{
        background-color:#6272a4}
        '''
COMBO_BOX_STYLE = '''
        QComboBox{font-size:11pt;
        font-family:Verdana,Microsoft YaHei UI;
        border-radius:5px;
        background-color:#6272a4;
        color:#f8f8f2}
        QComboBox:hover{
        border:none}
        QComboBox::drop-down{
        subcontrol-origin:padding;
        subcontrol-position:top right;
        width:25px; 
        border-left-width:3px;
        border-left-color:#6272a4;
        border-left-style:solid;
        border-top-right-radius:3px;
        border-bottom-right-radius:3px;	
        background-image:url(./ico/chevron_down.svg);
        background-position:center;
        background-repeat:no-reperat}
        QScrollBar:vertical{width:10px}
        QScrollBar::handle:vertical{
        background-color:#c3c3c3;
        border-radius:1px;
        min-height:45px}
        '''
TEXTEDIT_STYlE = '''
        QTextEdit{font-size:11pt;
        border-radius:5px;
        background-color:#6272a4;
        color:#f8f8f2;
        font-family:Verdana,Microsoft YaHei UI}
        QScrollBar:vertical{width:5px}
        QScrollBar::handle:vertical{
        background-color:#939393;
        border-radius:1px;
        min-height:45px}
        QScrollBar:horizontal{width:10px}
        QScrollBar::handle:horizontal{
        background-color:#daeaef;
        border-radius:1px;
        min-height:45px}
        '''
LINE_EDIT_STYLE = '''
        QLineEdit{font-size:10pt;
        border-radius:10px;
        background-color:#6272a4;
        color:#f8f8f2;
        font-family:Verdana,Microsoft YaHei UI}
        QLineEdit:focus{
        border:2px solid #b7cbc9}
        '''
BUTTON_STYLE = '''
        QPushButton{{
        border-radius:0px;
        background-color:rgba(255,255,255,0);
        image:url(./ico/{})}}
        QPushButton:hover{{
        image:url(./ico/{})}}
        QPushButton:pressed{{
        image:url(./ico/{})}}
        '''
BUTTON_STYLE0 = '''
        QPushButton{{
        border-radius:10px;
        background-color:rgba(255,255,255,0);
        image:url(./ico/{})}}
        QPushButton:hover{{
        background-color:#e2e2dd}}
        '''
BUTTON_STYLE1 = '''
        QPushButton{{
        border-radius:10px;
        background-color:rgba(255,255,255,0);
        image:url(./ico/{})}}
        QPushButton:hover{{
        background-color:#f25355;
        image:url(./ico/{})}}
        '''
TABLE_STYLE1 = '''
        QTableWidget{
        border:none;
        background-color:#f8f8f2}
        QTableWidget::item:selected{
        background-color:#f8f8f2}
        QHeaderView::section{
        padding:0px;
        border:none;
        color:#1b124b;
        background-color:#ffffff}
        QScrollBar:vertical{width:5px}
        QScrollBar::handle:vertical{
        background-color:#939393;
        border-radius:1px;
        min-height:45px}
        '''
TABLE_STYLE2 = '''
        QTableWidget{
        border-radius:5px;
        border:none;
        background-color:#adb6e0}
        QTableWidget::item:selected{
        background-color:#daeaef}
        QHeaderView::section{
        padding:0px;
        border:none;
        color:#1b124b;
        background-color:#ffffff}
        QScrollBar:vertical{width:5px}
        QScrollBar::handle:vertical{
        background-color:#939393;
        border-radius:1px;
        min-height:45px}
        '''
LABEL_STYLE = '''
        font-size:8pt;
        font-family:Verdana,Microsoft YaHei UI;
        color:#1b124b;
        background-color:rgba(255,255,255,0)
        '''
BGC_STYLE = '''
        QWidget{background-color:#f8f8f2}
        QToolTip{
        border:none;
        color:#3c3c3c;
        background-color:#ffffff;
        font-size:9pt;
        font-family:Verdana,Microsoft YaHei UI}
        '''
SWITCH_STYLE = '''
        SwitchBtn:on{
        background-color:#6272a4;
        color:#f8f8f2}
        SwitchBtn:off{
        background-color:#e2e2dd;
        color:#8d90a4}
        '''
WELCOME_PAGE = 'ico/bkg.svg'
