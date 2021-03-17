# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon
from .basics import MAX_WIDTH, MAX_HEIGHT
from PyQt5 import QtGui, QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import (QWidget, QTabWidget, QLabel, QTextEdit, QComboBox,
                             QLineEdit, QPushButton, QTableWidget, QCheckBox)


class MainR(QTabWidget):
    """
    main widow
    """
    def __init__(self):
        super(MainR, self).__init__()
        self.setFixedSize(MAX_WIDTH, MAX_HEIGHT)
        self.setWindowTitle('PDF Editor')
        self.setStyleSheet('''
        QTabBar::tab{
        border:none;
        border-bottom-color:#FFFFFF;
        border-top-right-radius:20px;
        border-bottom-right-radius:20px;
        min-width:40ex;
        padding:8px;
        font-size:20px;
        font-family:calibri;}
        QTabBar::tab:selected{
        background-color:#FFFFFF;
        border-top:1px solid #E5E5E5;
        border-right:1px solid #E5E5E5}
        ''')
        self.setWindowIcon(QIcon('ico\\pdf icon.ico'))
        self.setTabShape(QTabWidget.Rounded)
        self.setIconSize(QtCore.QSize(40, 40))
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab1_init()
        self.tab2_init()
        self.tab3_init()

    def tab1_init(self):
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.scroll_bar = QtWidgets.QScrollBar(self.tab1)
        self.tab1.scroll_bar.setStyleSheet(
            'QScrollBar:vertical{width:15px}'
            'QScrollBar::handle:vertical{background-color:#F1F1FF;'
            'border-radius:1px;min-height:45px}'
        )
        self.tab1.button1 = QPushButton(self.tab1)
        self.tab1.button2 = QPushButton(self.tab1)
        self.tab1.button3 = QPushButton(self.tab1)
        self.tab1.button4 = QPushButton(self.tab1)
        self.tab1.button5 = QPushButton(self.tab1)
        self.tab1.button1.setIcon(QIcon('ico\\new.png'))
        self.tab1.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab1.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab1.button4.setIcon(QIcon('ico\\clean.png'))
        self.tab1.button5.setIcon(QIcon('ico\\about.png'))
        self.tab1.button1.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab1.button2.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab1.button3.setStyleSheet('border-radius:10px')
        self.tab1.button4.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab1.button5.setStyleSheet('border-radius:10px')
        self.tab1.button1.setIconSize(QtCore.QSize(60, 60))
        self.tab1.button2.setIconSize(QtCore.QSize(60, 60))
        self.tab1.button3.setIconSize(QtCore.QSize(60, 60))
        self.tab1.button4.setIconSize(QtCore.QSize(60, 60))
        self.tab1.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab1.table.setGeometry(
            QtCore.QRect(0, 100, self.width()-5, self.height()-170)
        )
        self.tab1.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab1.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab1.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab1.button4.setGeometry(QtCore.QRect(400, 10, 80, 80))
        self.tab1.button5.setGeometry(
            QtCore.QRect(self.width()-80, 20, 50, 50)
        )
        self.tab1.button3.setToolTip('Settings')
        self.tab1.button5.setToolTip('about')
        self.tab1.table.setVerticalScrollBar(self.tab1.scroll_bar)
        self.tab1.table.setShowGrid(False)
        self.tab1.table.verticalHeader().setVisible(False)
        self.tab1.table.horizontalHeader().setVisible(False)
        self.tab1.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.tab1.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tab1.table.setStyleSheet(
            'QTableWidget{border:0px;background-color:#FFFFFF};'
        )
        self.tab1.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab1.setStyleSheet('background-color:#DAEAEF')

    def tab2_init(self):
        self.tab2.table = QTableWidget(self.tab2)
        self.tab2.scroll_bar = QtWidgets.QScrollBar(self.tab2)
        self.tab2.scroll_bar.setStyleSheet(
            'QScrollBar:vertical{width:15px;}'
            'QScrollBar::handle:vertical{background-color:#F1F1FF;'
            'border-radius:1px;min-height:45px}'
        )
        self.tab2.button1 = QPushButton(self.tab2)
        self.tab2.button2 = QPushButton(self.tab2)
        self.tab2.button3 = QPushButton(self.tab2)
        self.tab2.button4 = QPushButton(self.tab2)
        self.tab2.button5 = QPushButton(self.tab2)
        self.tab2.button1.setIcon(QIcon('ico\\new.png'))
        self.tab2.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab2.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab2.button4.setIcon(QIcon('ico\\clean.png'))
        self.tab2.button5.setIcon(QIcon('ico\\col1.png'))
        self.tab2.button1.setStyleSheet(
            'QPushButton{border-radius:10px;}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab2.button2.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab2.button3.setStyleSheet('border-radius:10px')
        self.tab2.button4.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:#9DBDC6}'
        )
        self.tab2.button5.setStyleSheet('border-radius:10px')
        self.tab2.button1.setIconSize(QtCore.QSize(60, 60))
        self.tab2.button2.setIconSize(QtCore.QSize(60, 60))
        self.tab2.button3.setIconSize(QtCore.QSize(60, 60))
        self.tab2.button4.setIconSize(QtCore.QSize(60, 60))
        self.tab2.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab2.table.setGeometry(
            QtCore.QRect(0, 100, self.width()-5, self.height()-170)
        )
        self.tab2.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab2.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab2.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab2.button4.setGeometry(QtCore.QRect(400, 10, 80, 80))
        self.tab2.button5.setGeometry(
            QtCore.QRect(self.width() - 80, 20, 50, 50)
        )
        self.tab2.button3.setToolTip('Settings')
        self.tab2.button5.setToolTip('dual columns')
        self.tab2.table.setShowGrid(False)
        self.tab2.table.setVerticalScrollBar(self.tab2.scroll_bar)
        self.tab2.table.verticalHeader().setVisible(False)
        self.tab2.table.horizontalHeader().setVisible(False)
        self.tab2.table.setStyleSheet(
            'QTableWidget{border:0px;background-color:#FFFFFF}'
        )
        self.tab2.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tab2.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.tab2.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tab2.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab2.setStyleSheet('background-color:#DAEAEF')

    def tab3_init(self):
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(
            QtCore.QRect(20, 100,
                         (self.height()-170)*3//4,
                         self.height()-170)
        )
        self.tab3.table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.tab3.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        self.tab3.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tab3.table.setColumnWidth(0, self.tab3.table.width())
        self.tab3.table.setRowHeight(0, self.tab3.table.height())
        self.tab3.table.setStyleSheet(
            'QTableWidget{border:0px;background-color:#DAEAEF}'
        )
        self.tab3.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab3.button1 = QPushButton(self.tab3)
        self.tab3.button2 = QPushButton(self.tab3)
        self.tab3.button3 = QPushButton(self.tab3)
        self.tab3.button4 = QPushButton(self.tab3)
        self.tab3.button1.setIcon(QIcon('ico\\new.png'))
        self.tab3.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab3.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab3.button4.setIcon(QIcon('ico\\palette.png'))
        self.tab3.button1.setStyleSheet(
            'QPushButton{border-radius:10px;}'
            'QPushButton:hover{background-color:rgba(10,10,10,30)}'
        )
        self.tab3.button2.setStyleSheet(
            'QPushButton{border-radius:10px}'
            'QPushButton:hover{background-color:rgba(10,10,10,20)}'
        )
        self.tab3.button3.setStyleSheet('border-radius:10px')
        self.tab3.button4.setStyleSheet(
            'QPushButton{border-radius:15px}'
            'QPushButton:hover{background-color:rgba(245,233,190,80)}'
        )
        self.tab3.scroll_bar = QtWidgets.QScrollBar(self.tab3)
        self.tab3.scroll_bar.setStyleSheet(
            'QScrollBar:vertical{width:15px;}'
            'QScrollBar::handle:vertical{background-color:#F1F1FF;'
            'border-radius:1px;min-height:45px}'
        )
        self.tab3.button1.setIconSize(QtCore.QSize(60, 60))
        self.tab3.button2.setIconSize(QtCore.QSize(60, 60))
        self.tab3.button3.setIconSize(QtCore.QSize(60, 60))
        self.tab3.button4.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button3.setToolTip('Settings')
        self.tab3.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab3.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab3.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab3.button4.setGeometry(QtCore.QRect(1042, 550, 40, 40))
        self.tab3.text = QTextEdit(self.tab3)
        self.tab3.line1 = QLineEdit(self.tab3)
        self.tab3.line2 = QLineEdit(self.tab3)
        self.tab3.line3 = QLineEdit(self.tab3)
        self.tab3.line4 = QLineEdit(self.tab3)
        self.tab3.label1 = QLabel(self.tab3)
        self.tab3.label2 = QLabel(self.tab3)
        self.tab3.label3 = QLabel(self.tab3)
        self.tab3.label4 = QLabel(self.tab3)
        self.tab3.label5 = QLabel(self.tab3)
        self.tab3.label6 = QLabel(self.tab3)
        self.tab3.label7 = QLabel(self.tab3)
        self.tab3.label8 = QLabel(self.tab3)
        self.tab3.text.setGeometry(QtCore.QRect(733, 360, 300, 120))
        self.tab3.line1.setGeometry(QtCore.QRect(733, 160, 300, 40))
        self.tab3.line2.setGeometry(QtCore.QRect(733, 240, 300, 40))
        self.tab3.line3.setGeometry(QtCore.QRect(952, 500, 40, 40))
        self.tab3.line4.setGeometry(QtCore.QRect(952, 550, 40, 40))
        self.tab3.line1.setPlaceholderText('user password here')
        self.tab3.line2.setPlaceholderText('owner password here')
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('40')
        self.tab3.text.setStyleSheet('font-size:14pt;border-radius:5px;'
                                     'background-color:rgba(245,233,190,80);'
                                     'color:#174c4f;font-family:calibri')
        self.tab3.line1.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#F1F2FF;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line2.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#F1F1FF;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line3.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#F1F3FF;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line4.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#F1F3FF;'
                                      'color:#382513;font-family:calibri')
        self.tab3.label1.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label2.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label3.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label4.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label5.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label6.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label7.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label8.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.text.setVerticalScrollBar(self.tab3.scroll_bar)
        self.tab3.label1.setGeometry(QtCore.QRect(733, 100, 300, 40))
        self.tab3.label2.setGeometry(QtCore.QRect(733, 300, 300, 40))
        self.tab3.label3.setGeometry(QtCore.QRect(992, 500, 40, 40))
        self.tab3.label4.setGeometry(QtCore.QRect(832, 500, 120, 40))
        self.tab3.label5.setGeometry(QtCore.QRect(880, 840, 160, 40))
        self.tab3.label6.setGeometry(QtCore.QRect(992, 550, 40, 40))
        self.tab3.label7.setGeometry(QtCore.QRect(850, 550, 100, 40))
        self.tab3.label8.setGeometry(QtCore.QRect(733, 600, 300, 40))
        self.tab3.label1.setText('.'*10+'password'+'.'*10)
        self.tab3.label2.setText('.' * 10 + 'watermark' + '.' * 10)
        self.tab3.label3.setText('pt')
        self.tab3.label4.setText('Font Size:')
        self.tab3.label5.setText('Open after saving')
        self.tab3.label6.setText('%')
        self.tab3.label7.setText('Opacity:')
        self.tab3.label8.setText('.'*50)
        self.tab3.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label6.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label7.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label8.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.check = QCheckBox(self.tab3)
        self.tab3.check.setChecked(True)
        self.tab3.check.setGeometry(QtCore.QRect(1050, 840, 40, 40))


class SettingR(QWidget):
    """
    setting window
    """

    def __init__(self):
        super(SettingR, self).__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle('Setting')
        self.setWindowIcon(QIcon('ico\\settings.png'))
        self.setStyleSheet('background-color: #FFFFFF')
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line3 = QLineEdit(self)
        self.line4 = QLineEdit(self)
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.button3 = QPushButton(self)
        self.button4 = QPushButton(self)
        self.button5 = QPushButton(self)
        self.combobox = QComboBox(self)
        self.button1.setText('view')
        self.button2.setText('view')
        self.button3.setText('confirm')
        self.button4.setText('view')
        self.button5.setText('view')
        self.label1.setText('START DIR')
        self.label2.setText('SAVE DIR')
        self.label3.setText('PDF.JS DIR')
        self.label4.setText('FONT FILE')
        self.combobox.addItem('English')
        self.combobox.addItem('中文')
        self.combobox.addItem('日本語')
        self.label1.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label2.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label3.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label4.setStyleSheet('font-size:9pt;font-family:calibri')
        self.combobox.setStyleSheet(
            'font-size:12pt;font-family:calibri;'
            'border-radius:2px;background-color:rgba(245,233,190,100)'
        )
        self.button1.setStyleSheet(
            'font-size:9t;background-color:rgba(255,255,255,0);'
            'color:#A77E5E;font-weight:bold;font-family:calibri'
        )
        self.button2.setStyleSheet(
            'font-size:9t;background-color:rgba(255,255,255,0);'
            'color:#A77E5E;font-weight:bold;font-family:calibri'
        )
        self.button3.setStyleSheet(
            'font-size:9t;background-color:rgba(255,255,255,80);'
            'color:#A77E5E;font-weight:bold;font-family:calibri'
        )
        self.button4.setStyleSheet(
            'font-size:9t;background-color:rgba(255,255,255,0);'
            'color:#A77E5E;font-weight:bold;font-family:calibri'
        )
        self.button5.setStyleSheet(
            'font-size:9t;background-color:rgba(255,255,255,0);'
            'color:#A77E5E;font-weight:bold;font-family:calibri'
        )
        self.line1.setStyleSheet(
            'font-size:12pt;border-radius:15px;;color:#363942;'
            'background-color:#F5DCE3;font-family:calibri'
        )
        self.line2.setStyleSheet(
            'font-size:12pt;border-radius:15px;color:#363942;'
            'background-color:#F5DCE3;font-family:calibri'
        )
        self.line3.setStyleSheet(
            'font-size:12pt;border-radius:15px;color:#363942;'
            'background-color:#F1F2FF;font-family:calibri'
        )
        self.line4.setStyleSheet(
            'font-size:12pt;border-radius:15px;color:#363942;'
            'background-color:#F3F2FF;font-family:calibri'
        )
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.line1.setGeometry(QtCore.QRect(160, 20, 400, 40))
        self.line2.setGeometry(QtCore.QRect(160, 80, 400, 40))
        self.line3.setGeometry(QtCore.QRect(160, 140, 400, 40))
        self.line4.setGeometry(QtCore.QRect(160, 200, 400, 40))
        self.label1.setGeometry(QtCore.QRect(40, 20, 100, 40))
        self.label2.setGeometry(QtCore.QRect(40, 80, 100, 40))
        self.label3.setGeometry(QtCore.QRect(40, 140, 100, 40))
        self.label4.setGeometry(QtCore.QRect(40, 200, 100, 40))
        self.button1.setGeometry(QtCore.QRect(510, 20, 50, 40))
        self.button2.setGeometry(QtCore.QRect(510, 80, 50, 40))
        self.button3.setGeometry(QtCore.QRect(510, 350, 80, 40))
        self.button4.setGeometry(QtCore.QRect(510, 140, 50, 40))
        self.button5.setGeometry(QtCore.QRect(510, 200, 50, 40))
        self.combobox.setGeometry(QtCore.QRect(370, 260, 180, 40))


class PDFViewR(QtWebEngineWidgets.QWebEngineView):
    """
    PDF viewer window
    """
    def __init__(self):
        super(PDFViewR, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('PDF viewer')
        self.setWindowIcon(QIcon('ico\\pdf icon.ico'))

    def view(self, pdf_address, pdf_js_address):
        self.load(QtCore.QUrl.fromUserInput(
            '%s?file=%s' % (pdf_js_address, pdf_address))
        )


class AboutR(QWidget):
    """
    about window
    """
    def __init__(self):
        super(AboutR, self).__init__()
        self.setFixedSize(500, 350)
        self.setWindowTitle('About')
        self.setWindowIcon(QIcon('ico\\about.png'))
        self.setStyleSheet('background-color:#FFFFFF')
        self.label = QLabel(self)
        self.label.setText(
            "<p>Author: Nianze A. Tao</p>"
            "<p>MIT licence</p>"
            "<p>Github page:</p>"
            "<a href='https://github.com/Augus1999/pyPDFeditor-GUI'>"
            "<small>https://github.com/Augus1999/pyPDFeditor-GUI</small></a>"
        )
        self.label.setStyleSheet('font-size:12pt;font-family:calibri')
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setGeometry(
            QtCore.QRect(20, 20, self.width()-40, self.height()-20)
        )
        self.label.setOpenExternalLinks(True)
