# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget, QTabWidget, QLabel, QTextEdit,
                             QLineEdit, QPushButton, QTableWidget, QCheckBox)


class MainR(QTabWidget):
    """
    main widow
    """
    def __init__(self):
        super(MainR, self).__init__()
        self.setFixedSize(900, 600)
        self.setWindowTitle('PDF Editor')
        self.setStyleSheet('background-color: #ffffff')
        self.setWindowIcon(QtGui.QIcon('.\\ico\\pdf icon.ico'))
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab1_init()
        self.tab2_init()
        self.tab3_init()
        self.addTab(self.tab1, QIcon('ico\\icon1.png'), 'Merge PDF')
        self.addTab(self.tab2, QIcon('ico\\icon1.png'), 'Organise')
        self.addTab(self.tab3, QIcon('ico\\icon3.png'), 'Security')

    def tab1_init(self):
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.label = QLabel(self.tab1)
        self.tab1.scroll_bar = QtWidgets.QScrollBar(self.tab1)
        self.tab1.scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px}'
                                           'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                           'border-radius:1px;min-height:45px}')
        self.tab1.button1 = QPushButton(self.tab1)
        self.tab1.button2 = QPushButton(self.tab1)
        self.tab1.button3 = QPushButton(self.tab1)
        self.tab1.button1.setIcon(QIcon('ico\\new.png'))
        self.tab1.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab1.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab1.button1.setStyleSheet('QPushButton{border-radius:10px;}'
                                        'QPushButton:hover{background-color:#9dbdc6}')
        self.tab1.button2.setStyleSheet('QPushButton{border-radius:10px}'
                                        'QPushButton:hover{background-color:#9dbdc6}')
        self.tab1.button3.setStyleSheet('border-radius:10px')
        self.tab1.button1.setIconSize(QtCore.QSize(45, 45))
        self.tab1.button2.setIconSize(QtCore.QSize(45, 45))
        self.tab1.button3.setIconSize(QtCore.QSize(50, 50))
        self.tab1.table.setGeometry(QtCore.QRect(0, 76, 895, 480))
        self.tab1.label.setGeometry(QtCore.QRect(0, 0, 900, 76))
        self.tab1.button1.setGeometry(QtCore.QRect(10, 10, 56, 56))
        self.tab1.button2.setGeometry(QtCore.QRect(106, 10, 56, 56))
        self.tab1.button3.setGeometry(QtCore.QRect(824, 10, 56, 56))
        self.tab1.table.setVerticalScrollBar(self.tab1.scroll_bar)
        self.tab1.table.setShowGrid(False)
        self.tab1.table.verticalHeader().setVisible(False)
        self.tab1.table.horizontalHeader().setVisible(False)
        self.tab1.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab1.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tab1.table.setStyleSheet('QTableWidget{border:0px;background-color:#ffffff};')
        self.tab1.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab1.setStyleSheet('background-color:#daeaef')

    def tab2_init(self):
        self.tab2.table = QTableWidget(self.tab2)
        self.tab2.scroll_bar = QtWidgets.QScrollBar(self.tab2)
        self.tab2.scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                           'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                           'border-radius:1px;min-height:45px}')
        self.tab2.button1 = QPushButton(self.tab2)
        self.tab2.button2 = QPushButton(self.tab2)
        self.tab2.button3 = QPushButton(self.tab2)
        self.tab2.button1.setIcon(QIcon('ico\\new.png'))
        self.tab2.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab2.button3.setIcon(QIcon('ico\\clean.png'))
        self.tab2.button1.setStyleSheet('QPushButton{border-radius:10px;}'
                                        'QPushButton:hover{background-color:#9dbdc6}')
        self.tab2.button2.setStyleSheet('QPushButton{border-radius:10px}'
                                        'QPushButton:hover{background-color:#9dbdc6}')
        self.tab2.button3.setStyleSheet('QPushButton{border-radius:10px}'
                                        'QPushButton:hover{background-color:#9dbdc6}')
        self.tab2.button1.setIconSize(QtCore.QSize(45, 45))
        self.tab2.button2.setIconSize(QtCore.QSize(45, 45))
        self.tab2.button3.setIconSize(QtCore.QSize(30, 30))
        self.tab2.table.setGeometry(QtCore.QRect(0, 76, 895, 480))
        self.tab2.button1.setGeometry(QtCore.QRect(10, 10, 56, 56))
        self.tab2.button2.setGeometry(QtCore.QRect(106, 10, 56, 56))
        self.tab2.button3.setGeometry(QtCore.QRect(820, 20, 45, 45))
        self.tab2.table.setShowGrid(False)
        self.tab2.table.setVerticalScrollBar(self.tab2.scroll_bar)
        self.tab2.table.verticalHeader().setVisible(False)
        self.tab2.table.horizontalHeader().setVisible(False)
        self.tab2.table.setStyleSheet('QTableWidget{border:0px;background-color:#ffffff}')
        self.tab2.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tab2.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab2.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tab2.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab2.setStyleSheet('background-color:#daeaef')

    def tab3_init(self):
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(QtCore.QRect(20, 20, 397, 530))
        self.tab3.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab3.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab3.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tab3.table.setColumnWidth(0, 397)
        self.tab3.table.setRowHeight(0, 530)
        self.tab3.table.setStyleSheet('QTableWidget{border:0px;background-color:#daeaef}')
        self.tab3.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab3.button1 = QPushButton(self.tab3)
        self.tab3.button2 = QPushButton(self.tab3)
        self.tab3.button1.setIcon(QIcon('ico\\new.png'))
        self.tab3.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab3.button1.setStyleSheet('QPushButton{border-radius:10px;}'
                                        'QPushButton:hover{background-color:#f1f1ff}')
        self.tab3.button2.setStyleSheet('QPushButton{border-radius:10px}'
                                        'QPushButton:hover{background-color:#f1f1ff}')
        self.tab3.scroll_bar = QtWidgets.QScrollBar(self.tab3)
        self.tab3.scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                           'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                           'border-radius:1px;min-height:45px}')
        self.tab3.button1.setIconSize(QtCore.QSize(45, 45))
        self.tab3.button2.setIconSize(QtCore.QSize(45, 45))
        self.tab3.button1.setGeometry(QtCore.QRect(437, 494, 56, 56))
        self.tab3.button2.setGeometry(QtCore.QRect(533, 494, 56, 56))
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
        self.tab3.text.setGeometry(QtCore.QRect(533, 280, 300, 120))
        self.tab3.line1.setGeometry(QtCore.QRect(533, 80, 300, 40))
        self.tab3.line2.setGeometry(QtCore.QRect(533, 160, 300, 40))
        self.tab3.line3.setGeometry(QtCore.QRect(752, 420, 40, 40))
        self.tab3.line4.setGeometry(QtCore.QRect(752, 470, 40, 40))
        self.tab3.line1.setPlaceholderText('user password here')
        self.tab3.line2.setPlaceholderText('owner password here')
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('40')
        self.tab3.text.setStyleSheet('font-size:14pt;border-radius:5px;'
                                     'background-color:rgba(245,233,190,80);'
                                     'color:#174c4f;font-family:calibri')
        self.tab3.line1.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f2ff;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line2.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f1ff;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line3.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f3ff;'
                                      'color:#382513;font-family:calibri')
        self.tab3.line4.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f3ff;'
                                      'color:#382513;font-family:calibri')
        self.tab3.label1.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label2.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label3.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label4.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label5.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label6.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.label7.setStyleSheet('font-size:9pt;font-family:calibri')
        self.tab3.text.setVerticalScrollBar(self.tab3.scroll_bar)
        self.tab3.label1.setGeometry(QtCore.QRect(533, 20, 300, 40))
        self.tab3.label2.setGeometry(QtCore.QRect(533, 220, 300, 40))
        self.tab3.label3.setGeometry(QtCore.QRect(792, 420, 40, 40))
        self.tab3.label4.setGeometry(QtCore.QRect(632, 420, 120, 40))
        self.tab3.label5.setGeometry(QtCore.QRect(680, 510, 160, 40))
        self.tab3.label6.setGeometry(QtCore.QRect(792, 470, 40, 40))
        self.tab3.label7.setGeometry(QtCore.QRect(650, 470, 100, 40))
        self.tab3.label1.setText('.'*10+'password'+'.'*10)
        self.tab3.label2.setText('.' * 10 + 'watermark' + '.' * 10)
        self.tab3.label3.setText('pt')
        self.tab3.label4.setText('Font Size:')
        self.tab3.label5.setText('Open after saving')
        self.tab3.label6.setText('%')
        self.tab3.label7.setText('Opacity:')
        self.tab3.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label6.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label7.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.check = QCheckBox(self.tab3)
        self.tab3.check.setChecked(True)
        self.tab3.check.setGeometry(QtCore.QRect(850, 510, 40, 40))


class SettingR(QWidget):
    """
    setting window
    """
    signal = QtCore.pyqtSignal(str, str, list)

    def __init__(self):
        super(SettingR, self).__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle('Setting')
        self.setWindowIcon(QtGui.QIcon('.\\ico\\settings.png'))
        self.setStyleSheet('background-color: #ffffff')
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line3 = QLineEdit(self)
        self.line4 = QLineEdit(self)
        self.line5 = QLineEdit(self)
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.button3 = QPushButton(self)
        self.button1.setText('view')
        self.button2.setText('view')
        self.button3.setText('confirm')
        self.label1.setText('START DIR')
        self.label2.setText('SAVE DIR')
        self.label3.setText('R')
        self.label4.setText('G')
        self.label5.setText('B')
        self.label6.setText('.'*10+'watermark colour'+'.'*10)
        self.label1.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label2.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label3.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label4.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label5.setStyleSheet('font-size:9pt;font-family:calibri')
        self.label6.setStyleSheet('font-size:9pt;font-family:calibri')
        self.button1.setStyleSheet('font-size:9t;background-color:rgba(255,255,255,0);'
                                   'color:#a77e5e;font-weight:bold;font-family:calibri')
        self.button2.setStyleSheet('font-size:9t;background-color:rgba(255,255,255,0);'
                                   'color:#a77e5e;font-weight:bold;font-family:calibri')
        self.button3.setStyleSheet('font-size:9t;background-color:rgba(255,255,255,80);'
                                   'color:#a77e5e;font-weight:bold;font-family:calibri')
        self.line1.setStyleSheet('font-size:12pt;border-radius:15px;;color:#363942;'
                                 'background-color:#f5dce3;font-family:calibri')
        self.line2.setStyleSheet('font-size:12pt;border-radius:15px;color:#363942;'
                                 'background-color:#f1f2ff;font-family:calibri')
        self.line3.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:rgba(236,190,139,70);'
                                 'font-family:calibri;color:#363942')
        self.line4.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:rgba(236,190,139,70);'
                                 'font-family:calibri;color:#363942')
        self.line5.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:rgba(236,190,139,70);'
                                 'font-family:calibri;color:#363942')
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.label6.setAlignment(QtCore.Qt.AlignCenter)
        self.line1.setGeometry(QtCore.QRect(160, 20, 400, 40))
        self.line2.setGeometry(QtCore.QRect(160, 80, 400, 40))
        self.line3.setGeometry(QtCore.QRect(160, 200, 40, 40))
        self.line4.setGeometry(QtCore.QRect(230, 200, 40, 40))
        self.line5.setGeometry(QtCore.QRect(300, 200, 40, 40))
        self.label1.setGeometry(QtCore.QRect(40, 20, 100, 40))
        self.label2.setGeometry(QtCore.QRect(40, 80, 100, 40))
        self.label3.setGeometry(QtCore.QRect(140, 200, 10, 40))
        self.label4.setGeometry(QtCore.QRect(210, 200, 10, 40))
        self.label5.setGeometry(QtCore.QRect(280, 200, 10, 40))
        self.label6.setGeometry(QtCore.QRect(0, 140, 600, 40))
        self.button1.setGeometry(QtCore.QRect(510, 20, 50, 40))
        self.button2.setGeometry(QtCore.QRect(510, 80, 50, 40))
        self.button3.setGeometry(QtCore.QRect(510, 350, 80, 40))
