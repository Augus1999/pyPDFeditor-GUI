# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import json
import subprocess as sp
from PyQt5.QtGui import QIcon
from PyPDF2 import PdfFileMerger
from PyQt5 import QtGui, QtCore, QtWidgets
from scripts import *
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QLabel, QTextEdit,
                             QLineEdit, QPushButton, QTableWidget, QFileDialog, QCheckBox)


class Main(QTabWidget):
    def __init__(self):
        super(Main, self).__init__()
        content = setting_warning('settings\\main_settings.json')
        self.s_dir, self.o_dir = content["start dir"], content["save dir"]
        self.colour_r = content["colour"]["R"]
        self.colour_g = content["colour"]["G"]
        self.colour_b = content["colour"]["B"]
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
        self.ChildDialog = Setting()

    def tab1_init(self):
        self.tab1.book_list = list()
        self.tab1.x, self.tab1.y = 0, 0
        self.tab1.col, self.tab1.crow = -1, -1
        self.tab1.w_col, self.tab1.w_row = 4, 2
        self.tab1.table = QTableWidget(self.tab1)
        scroll_bar = QtWidgets.QScrollBar(self.tab1)
        scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px}'
                                 'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                 'border-radius:1px;min-height:45px}')
        button1 = QPushButton(self.tab1)
        button2 = QPushButton(self.tab1)
        button3 = QPushButton(self.tab1)
        button1.setIcon(QIcon('ico\\new.png'))
        button2.setIcon(QIcon('ico\\disk.png'))
        button3.setIcon(QIcon('ico\\settings.png'))
        button1.setStyleSheet('QPushButton{border-radius:10px;}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        button2.setStyleSheet('QPushButton{border-radius:10px}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        button3.setStyleSheet('border-radius:10px')
        button1.setIconSize(QtCore.QSize(45, 45))
        button2.setIconSize(QtCore.QSize(45, 45))
        button3.setIconSize(QtCore.QSize(50, 50))
        self.tab1.table.setGeometry(QtCore.QRect(10, 76, 875, 480))
        button1.setGeometry(QtCore.QRect(10, 10, 56, 56))
        button2.setGeometry(QtCore.QRect(106, 10, 56, 56))
        button3.setGeometry(QtCore.QRect(824, 10, 56, 56))
        self.tab1.table.setRowCount(self.tab1.w_row)
        self.tab1.table.setColumnCount(self.tab1.w_col)
        self.tab1.table.setVerticalScrollBar(scroll_bar)
        self.tab1.table.verticalHeader().setVisible(False)
        self.tab1.table.horizontalHeader().setVisible(False)
        self.tab1.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tab1.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab1.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(self.tab1.w_col):
            self.tab1.table.setColumnWidth(i, (875-16)//self.tab1.w_col)
        for i in range(self.tab1.w_row):
            self.tab1.table.setRowHeight(i, ((875-15)//self.tab1.w_col)*4//3)
        cover(words='PDF file', widget=self.tab1)
        self.tab1.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab1.table.customContextMenuRequested.connect(self.gen1)
        button1.clicked.connect(self.add1)
        button2.clicked.connect(self.save1)
        button3.clicked.connect(self._set)

    def tab2_init(self):
        self.tab2.book_list = list()
        self.tab2.x, self.tab2.y = 0, 0
        self.tab2.col, self.tab2.crow = -1, -1
        self.tab2.w_row, self.tab2.w_col = 2, 4
        self.tab2.table = QTableWidget(self.tab2)
        scroll_bar = QtWidgets.QScrollBar(self.tab2)
        scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                 'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                 'border-radius:1px;min-height:45px}')
        button1 = QPushButton(self.tab2)
        button2 = QPushButton(self.tab2)
        button1.setIcon(QIcon('ico\\new.png'))
        button2.setIcon(QIcon('ico\\disk.png'))
        button1.setStyleSheet('QPushButton{border-radius:10px;}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        button2.setStyleSheet('QPushButton{border-radius:10px}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        button1.setIconSize(QtCore.QSize(45, 45))
        button2.setIconSize(QtCore.QSize(45, 45))
        self.tab2.table.setGeometry(QtCore.QRect(10, 76, 875, 480))
        button1.setGeometry(QtCore.QRect(10, 10, 56, 56))
        button2.setGeometry(QtCore.QRect(106, 10, 56, 56))
        self.tab2.table.setRowCount(self.tab2.w_row)
        self.tab2.table.setColumnCount(self.tab2.w_col)
        self.tab2.table.setVerticalScrollBar(scroll_bar)
        self.tab2.table.verticalHeader().setVisible(False)
        self.tab2.table.horizontalHeader().setVisible(False)
        self.tab2.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tab2.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab2.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(self.tab2.w_col):
            self.tab2.table.setColumnWidth(i, (875-16)//self.tab2.w_col)
        for i in range(self.tab2.w_row):
            self.tab2.table.setRowHeight(i, ((875-15)//self.tab2.w_col)*4//3)
        cover(words='page', widget=self.tab2)
        self.tab2.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab2.table.customContextMenuRequested.connect(self.gen2)
        button1.clicked.connect(self.add2)
        button2.clicked.connect(self.save2)

    def tab3_init(self):
        self.tab3.book_list = list()
        self.tab3.x, self.tab3.y = 0, 0
        self.tab3.col, self.tab3.crow = -1, -1
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.setRowCount(self.tab3.w_row)
        self.tab3.table.setColumnCount(self.tab3.w_col)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(QtCore.QRect(20, 20, 397, 530))
        self.tab3.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab3.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab3.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tab3.table.setColumnWidth(0, 397)
        self.tab3.table.setRowHeight(0, 530)
        cover(words='PDF file', widget=self.tab3)
        self.tab3.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab3.table.customContextMenuRequested.connect(self.gen3)
        button1 = QPushButton(self.tab3)
        button2 = QPushButton(self.tab3)
        button1.setIcon(QIcon('ico\\new.png'))
        button2.setIcon(QIcon('ico\\disk.png'))
        button1.setStyleSheet('QPushButton{border-radius:10px;}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        button2.setStyleSheet('QPushButton{border-radius:10px}'
                              'QPushButton:hover{background-color:#f1f1ff}')
        scroll_bar = QtWidgets.QScrollBar(self.tab3)
        scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                 'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                 'border-radius:1px;min-height:45px}')
        button1.setIconSize(QtCore.QSize(45, 45))
        button2.setIconSize(QtCore.QSize(45, 45))
        button1.setGeometry(QtCore.QRect(437, 494, 56, 56))
        button2.setGeometry(QtCore.QRect(533, 494, 56, 56))
        self.tab3.text = QTextEdit(self.tab3)
        self.tab3.line1 = QLineEdit(self.tab3)
        self.tab3.line2 = QLineEdit(self.tab3)
        self.tab3.line3 = QLineEdit(self.tab3)
        self.tab3.line4 = QLineEdit(self.tab3)
        label1 = QLabel(self.tab3)
        label2 = QLabel(self.tab3)
        label3 = QLabel(self.tab3)
        label4 = QLabel(self.tab3)
        label5 = QLabel(self.tab3)
        label6 = QLabel(self.tab3)
        label7 = QLabel(self.tab3)
        self.tab3.text.setGeometry(QtCore.QRect(533, 280, 300, 120))
        self.tab3.line1.setGeometry(QtCore.QRect(533, 80, 300, 40))
        self.tab3.line2.setGeometry(QtCore.QRect(533, 160, 300, 40))
        self.tab3.line3.setGeometry(QtCore.QRect(752, 420, 40, 40))
        self.tab3.line4.setGeometry(QtCore.QRect(752, 470, 40, 40))
        self.tab3.line1.setPlaceholderText('user password here')
        self.tab3.line2.setPlaceholderText('owner password here')
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('50')
        self.tab3.line1.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f2ff')
        self.tab3.line2.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f1ff')
        self.tab3.line3.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f3ff')
        self.tab3.line4.setStyleSheet('font-size:12pt;border-radius:15px;'
                                      'background-color:#f1f3ff')
        label1.setStyleSheet('font-size:9pt')
        label2.setStyleSheet('font-size:9pt')
        label3.setStyleSheet('font-size:9pt')
        label4.setStyleSheet('font-size:9pt')
        label5.setStyleSheet('font-size:9pt')
        label6.setStyleSheet('font-size:9pt')
        label7.setStyleSheet('font-size:9pt')
        self.tab3.text.setVerticalScrollBar(scroll_bar)
        label1.setGeometry(QtCore.QRect(533, 20, 300, 40))
        label2.setGeometry(QtCore.QRect(533, 220, 300, 40))
        label3.setGeometry(QtCore.QRect(792, 420, 40, 40))
        label4.setGeometry(QtCore.QRect(632, 420, 120, 40))
        label5.setGeometry(QtCore.QRect(680, 510, 160, 40))
        label6.setGeometry(QtCore.QRect(792, 470, 40, 40))
        label7.setGeometry(QtCore.QRect(650, 470, 100, 40))
        label1.setText('.'*10+'password'+'.'*10)
        label2.setText('.' * 10 + 'watermark' + '.' * 10)
        label3.setText('pt')
        label4.setText('Font Size:')
        label5.setText('Open after saving')
        label6.setText('%')
        label7.setText('Opacity:')
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label2.setAlignment(QtCore.Qt.AlignCenter)
        label3.setAlignment(QtCore.Qt.AlignCenter)
        label4.setAlignment(QtCore.Qt.AlignCenter)
        label5.setAlignment(QtCore.Qt.AlignCenter)
        label6.setAlignment(QtCore.Qt.AlignCenter)
        label7.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.check = QCheckBox(self.tab3)
        self.tab3.check.setChecked(True)
        self.tab3.check.setGeometry(QtCore.QRect(850, 510, 40, 40))
        button1.clicked.connect(self.add3)
        button2.clicked.connect(self.save3)

    def save1(self):
        # 点击保存按钮事件
        merger = PdfFileMerger()
        if len(self.tab1.book_list) != 0:
            for item in self.tab1.book_list:
                _input = open(item, 'rb')
                merger.append(_input)
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                with open(file_name.replace('/', '\\'), 'wb') as g:
                    merger.write(g)
                sp.Popen('explorer ' + file_name.replace('/', '\\'), shell=True)

    def save2(self):
        # 点击保存按钮事件
        merger = PdfFileMerger()
        if len(self.tab2.book_list) != 0:
            for item in self.tab2.book_list:
                _input = open(item, 'rb')
                merger.append(_input)
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                with open(file_name.replace('/', '\\'), 'wb') as g:
                    merger.write(g)
                sp.Popen('explorer ' + file_name.replace('/', '\\'), shell=True)

    def save3(self):
        # 点击保存按钮事件
        u_password = self.tab3.line1.text()
        o_password = self.tab3.line2.text()
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text())/100
        if len(self.tab3.book_list) != 0:
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                cache_file_name = 'cache\\'+file_name.split('/')[-1].replace('.pdf', '_cache.pdf')
                create_watermark(self.tab3.book_list[0], cache_file_name, watermark, 0,
                                 (float(self.colour_r), float(self.colour_g), float(self.colour_b),),
                                 font_size=font_size, opacity=opacity)
                add_encryption(cache_file_name, file_name.replace('/', '\\'), u_password, o_password)
                os.remove(cache_file_name)
                if self.tab3.check.isChecked():
                    sp.Popen('explorer '+file_name.replace('/', '\\'), shell=True)

    def _set(self):
        # 点击设置按钮事件
        self.ChildDialog.show()
        self.ChildDialog.signal.connect(self.get_data)

    def gen1(self, pos):
        generate_menu(pos, self.tab1)

    def gen2(self, pos):
        generate_menu(pos, self.tab2)

    def gen3(self, pos):
        generate_menu(pos, self.tab3)

    def add1(self):
        f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                                self.s_dir, '(*.pdf)')
        if _:
            if f_name not in self.tab1.book_list:
                self.tab1.book_list.append(f_name.replace('/', '\\'))
                book_len = len(self.tab1.book_list)
                reset_table(book_len, self.tab1)
                self.tab1.table.clear()
                self.tab1.x, self.tab1.y = 0, 0
            for item in self.tab1.book_list:
                set_icon(item, self.tab1)
        else:
            pass

    def add2(self):
        if len(self.tab2.book_list) == 0:
            f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                                    self.s_dir, '(*.pdf)')
            if _:
                self.tab2.book_list = pdf_split(f_name.replace('/', '\\'))
                book_len = len(self.tab2.book_list)
                reset_table(book_len, self.tab2)
                for item in self.tab2.book_list:
                    set_icon(item, self.tab2)
            else:
                pass

    def add3(self):
        if len(self.tab3.book_list) == 0:
            add(self, self.tab3)

    def get_data(self, par1, par2, par3):
        self.s_dir = par1
        self.o_dir = par2
        self.colour_r = par3[0]
        self.colour_g = par3[1]
        self.colour_b = par3[2]


class Setting(QWidget):
    signal = QtCore.pyqtSignal(str, str, list)

    def __init__(self):
        super(Setting, self).__init__()
        content = setting_warning('settings\\main_settings.json')
        self.s_dir, self.o_dir = content["start dir"], content["save dir"]
        self.colour_r = content["colour"]["R"]
        self.colour_g = content["colour"]["G"]
        self.colour_b = content["colour"]["B"]
        self.setFixedSize(600, 400)
        self.setWindowTitle('Setting')
        self.setWindowIcon(QtGui.QIcon(':\\ico\\settings.png'))
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
        self.line1.setText(self.s_dir)
        self.line2.setText(self.o_dir)
        self.line3.setText(self.colour_r)
        self.line4.setText(self.colour_g)
        self.line5.setText(self.colour_b)
        self.button1.setText('view')
        self.button2.setText('view')
        self.button3.setText('confirm')
        self.label1.setText('Start Root')
        self.label2.setText('Save Root')
        self.label3.setText('R')
        self.label4.setText('G')
        self.label5.setText('B')
        self.label6.setText('.'*10+'watermark colour'+'.'*10)
        self.label1.setStyleSheet('font-size:9pt')
        self.label2.setStyleSheet('font-size:9pt')
        self.label3.setStyleSheet('font-size:9pt')
        self.label4.setStyleSheet('font-size:9pt')
        self.label5.setStyleSheet('font-size:9pt')
        self.label6.setStyleSheet('font-size:9pt')
        self.line1.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:#f1f2ff')
        self.line2.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:#f1f2ff')
        self.line3.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:#f1f2ff')
        self.line4.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:#f1f2ff')
        self.line5.setStyleSheet('font-size:12pt;border-radius:15px;'
                                 'background-color:#f1f2ff')
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
        self.button1.clicked.connect(self.select1)
        self.button2.clicked.connect(self.select2)
        self.button3.clicked.connect(self.out)

    def out(self):
        self.signal.emit(self.line1.text(), self.line2.text(),
                         [self.line3.text(), self.line4.text(), self.line5.text()])
        _settings = {
            "start dir": self.line1.text(),
            "save dir": self.line2.text(),
            "colour": {"R": self.line3.text(), "G": self.line4.text(), "B": self.line5.text()}
        }
        with open('settings\\main_settings.json', 'w', encoding='utf-8') as f:
            json.dump(_settings, f)
        self.close()

    def select1(self):
        root = QtWidgets.QFileDialog.getExistingDirectory(None, "choose", self.s_dir)
        self.line1.setText(root.replace('/', '\\'))

    def select2(self):
        root = QtWidgets.QFileDialog.getExistingDirectory(None, "choose", self.s_dir)
        self.line2.setText(root.replace('/', '\\'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    _set = Setting()
    main.show()
    sys.exit(app.exec_())
