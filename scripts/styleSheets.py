# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
TAB_STYLE = '''
        QTabBar::tab{
        border-left:4px solid #6272a4;
        padding:3ex;
        margin:0px}
        QTabBar::tab:selected{
        border-left:4px solid #b7cbc9;
        background-color:#4f5c84}
        QTabBar::tab:hover{
        border-left:4px solid #ca8fc0;
        background-color:#ca8fc0}
        QToolTip{
        border:none;
        color:#3c3c3c;
        background-color:#ffffff;
        font-size:9pt;
        font-family:Verdana,Microsoft YaHei UI}
        QTabWidget{
        border:none;
        border-radius:0px;
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
        QScrollBar:vertical{
        background-color:#ffffff;
        border:none;
        width:10px}
        QScrollBar::handle:vertical{
        background-color:#6272a4;
        border-radius:3px;
        min-height:45px}
        '''
TEXTEDIT_STYlE = '''
        QTextEdit{font-size:11pt;
        border-radius:5px;
        background-color:#6272a4;
        color:#f8f8f2;
        font-family:Verdana,Microsoft YaHei UI}
        QScrollBar:vertical{
        border:none;
        border-top-right-radius:4px;
        border-bottom-right-radius:0px;
        background-color:#6272a4;
        margin:0 0 0 0;
        width:8px}
        QScrollBar::handle:vertical{
        background-color:#b7cbc9;
        border-radius:4px;
        min-height:45px}
        QScrollBar:horizontal{
        border:none;
        border-bottom-left-radius:4px;
        border-bottom-right-radius:0px;
        background-color:#6272a4;
        margin:0 0 0 0;
        width:5px}
        QScrollBar::handle:horizontal{
        background-color:#6272a4;
        border-radius:4px;
        min-width:45px}
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
        QScrollBar:vertical{
        border:none;
        width:5px;
        background-color:#f7f7f1}
        QScrollBar::handle:vertical{
        background-color:#939393;
        border-radius:2px;
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
        QScrollBar:vertical{
        background-color:#f8f8f2;
        border:none;
        border-radius:0px;
        margin:0 0 0 0;
        width:5px}
        QScrollBar::handle:vertical{
        background-color:#939393;
        border-radius:2px;
        min-height:45px}
        '''
LABEL_STYLE = '''
        QLabel{
        border:none;
        border-radius:10px;
        font-size:8pt;
        font-family:Verdana,Microsoft YaHei UI;
        color:#1b124b;
        background-color:rgba(255,255,255,0)}
        '''
BGC_STYLE = '''
        QWidget{
        border:none;
        border-radius:0px;
        background-color:#f8f8f2}
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
SCROLL_AREA_STYlE = '''
        QScrollArea{
        border:none;
        background-color:rgba(255,255,255,0)}
        QScrollBar:horizontal{
        border:none;
        background:#6272a4;
        height:8px;
        margin:0px 21px 0 21px;
        border-radius:0px}
        QScrollBar::handle:horizontal{
        background:#b7cbc9;
        min-width:25px;
        border-radius:0px}
        QScrollBar::add-line:horizontal{
        border:none;
        background:#6272a4;
        width:20px;
        border-top-right-radius:4px;
        border-bottom-right-radius:4px;
        subcontrol-position:right;
        subcontrol-origin:margin}
        QScrollBar::sub-line:horizontal{
        border:none;
        background:#6272a4;
        width:20px;
        border-top-left-radius:4px;
        border-bottom-left-radius:4px;
        subcontrol-position:left;
        subcontrol-origin:margin}
        QScrollBar::up-arrow:horizontal,QScrollBar::down-arrow:horizontal{
        background:none}
        QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{
        background:none}
        QScrollBar:vertical{
        border:none;
        background-color:#6272a4;
        width:8px;
        margin:21px 0 21px 0;
        border-radius:0px}
        QScrollBar::handle:vertical{	
        background:#b7cbc9;
        min-height:25px;
        border-radius:0px}
        QScrollBar::add-line:vertical{
        border:none;
        background:#6272a4;
        height:20px;
        border-bottom-left-radius:4px;
        border-bottom-right-radius:4px;
        subcontrol-position:bottom;
        subcontrol-origin:margin}
        QScrollBar::sub-line:vertical{
        border:none;
        background:#6272a4;
        height:20px;
        border-top-left-radius:4px;
        border-top-right-radius:4px;
        subcontrol-position:top;
        subcontrol-origin:margin}
        QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{
        background:none}
        QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
        background:none}
        '''
WELCOME_PAGE = 'ico/bkg.svg'
