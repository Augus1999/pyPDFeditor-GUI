# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
TAB_STYLE = '''
        QTabBar::tab{{
        border:none;
        border-bottom-color:#FFFFFF;
        border-top-right-radius:20px;
        border-bottom-right-radius:20px;
        min-width:40ex;
        padding:8px;
        font-size:{}pt;
        font-family:{};}}
        QTabBar::tab:selected{{
        background-color:#FFFFFF;
        border-top:1px solid #E5E5E5;
        border-right:1px solid #E5E5E5}}
        '''
SCROLL_BAR_STYLE_V = '''
        QScrollBar:vertical{width:10px}
        QScrollBar::handle:vertical{
        background-color:#c3c3c3;
        border-radius:1px;
        min-height:45px}
        '''
SCROLL_BAR_STYLE_H = '''
        QScrollBar:horizontal{width:15px}
        QScrollBar::handle:horizontal{
        background-color:#c3c3c3;
        border-radius:1px;
        min-height:45px}
        '''
COMBO_BOX_STYLE = '''
        font-size:12pt;
        font-family:calibri;
        border-radius:2px;
        background-color:#daeaef;
        color:#3c3c3c
        '''
TEXTEDIT_STYlE = '''
        font-size:{}pt;
        border-radius:5px;
        background-color:#DAEAEF;
        color:#3c3c3c;
        font-family:calibri
        '''
LINE_EDIT_STYLE = '''
        font-size:12pt;
        border-radius:15px;
        background-color:#DAEAEF;
        color:#3c3c3c;
        font-family:calibri
        '''
BUTTON_STYLE1 = '''
        QPushButton{border-radius:10px}
        QPushButton:hover{background-color:#9DBDC6}
        '''
BUTTON_STYLE2 = '''
        QPushButton{border-radius:10px;}
        QPushButton:hover{background-color:rgba(10,10,10,30)}
        '''
BUTTON_STYLE3 = '''
        QPushButton{border-radius:15px}
        QPushButton:hover{background-color:rgba(245,233,190,80)}
        '''
BUTTON_STYLE4 = '''
        font-size:9t;
        background-color:rgba(255,255,255,0);
        color:#A77E5E;
        font-weight:bold;
        font-family:calibri
        '''
BUTTON_STYLE6 = 'border-radius:10px'
TABLE_STYLE1 = 'QTableWidget{border:0px;background-color:#FFFFFF}'
TABLE_STYLE2 = 'QTableWidget{border:0px;background-color:#daeaef}'
LABEL_STYLE1 = 'font-size:10pt;font-family:consolas;color:#3c3c3c'
LABEL_STYLE2 = 'font-size:10pt;font-family:calibri;color:#3c3c3c'
BGC_STYLE1 = 'background-color:#DAEAEF'
BGC_STYLE2 = 'background-color:#FFFFFF'
