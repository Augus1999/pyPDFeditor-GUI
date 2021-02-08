# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import subprocess as sp
from PyQt5.QtGui import QIcon
from PyPDF2 import PdfFileMerger
from PyQt5 import QtGui, QtCore, QtWidgets
from scripts import (setting, setting_warning, recover, cover, add, set_icon,
                     generate_menu, add_encryption, create_watermark, pdf_split, reset_table)
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QLabel, QTextEdit,
                             QLineEdit, QPushButton, QTableWidget, QFileDialog, QCheckBox)


class Main(QTabWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.setFixedSize(900, 600)
        self.setWindowTitle('PDF Editor')
        self.setStyleSheet('background-color: #ffffff')
        self.setWindowIcon(QtGui.QIcon('.\\ico\\pdf.ico'))
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
        content = setting_warning('settings\\merger_settings.json')
        self.tab1.s_dir, self.tab1.o_dir = content["start dir"], content["save dir"]
        self.tab1.w_col, self.tab1.w_row = content["Column Counter"], content["Row Counter"]
        self.tab1.book_list = list()
        self.tab1.x, self.tab1.y = 0, 0
        self.tab1.col, self.tab1.crow = -1, -1
        self.tab1.open_program = content["open program"]
        self.tab1.table = QTableWidget(self.tab1)
        scroll_bar = QtWidgets.QScrollBar(self.tab1)
        scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                 'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                 'border-radius:1px}')
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
        # self.tab1.table.setShowGrid(False)
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
        cover(self.tab1)
        if os.path.exists('cache\\merger_cache.th'):
            recover('cache\\merger_cache.th', self.tab1)
        self.tab1.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab1.table.customContextMenuRequested.connect(self.gen1)
        button1.clicked.connect(self.add1)
        button2.clicked.connect(self.save1)
        button3.clicked.connect(self._set)

    def tab2_init(self):
        content = setting_warning('settings\\security_settings.json')
        self.tab2.s_dir, self.tab2.o_dir = content["start dir"], content["save dir"]
        self.tab2.book_list = list()
        self.tab2.x, self.tab2.y = 0, 0
        self.tab2.col, self.tab2.crow = -1, -1
        self.tab2.w_row, self.tab2.w_col = 2, 4
        self.tab2.table = QTableWidget(self.tab2)
        scroll_bar = QtWidgets.QScrollBar(self.tab2)
        scroll_bar.setStyleSheet('QScrollBar:vertical{width:15px;}'
                                 'QScrollBar::handle:vertical{background-color:#f1f1ff;'
                                 'border-radius:1px}')
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
        # self.tab1.table.setShowGrid(False)
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
        cover(self.tab2)
        self.tab2.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab2.table.customContextMenuRequested.connect(self.gen2)
        button1.clicked.connect(self.add2)
        button2.clicked.connect(self.save2)

    def tab3_init(self):
        content = setting_warning('settings\\security_settings.json')
        self.tab3.s_dir, self.tab3.o_dir = content["start dir"], content["save dir"]
        self.tab3.book_list = list()
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab3.x, self.tab3.y = 0, 0
        self.tab3.col, self.tab3.crow = -1, -1
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
        cover(self.tab3)
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
                                 'border-radius:1px}')
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
                                                        self.tab1.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                with open(file_name, 'wb') as g:
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
                                                        self.tab2.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                with open(file_name, 'wb') as g:
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
                                                        self.tab3.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                cache_file_name = 'cache\\'+file_name.split('/')[-1].replace('.pdf', '_cache.pdf')
                create_watermark(self.tab3.book_list[0], cache_file_name, watermark,
                                 0, (1, 0, 0), font_size=font_size, opacity=opacity)
                add_encryption(cache_file_name, file_name, u_password, o_password)
                os.remove(cache_file_name)
                if self.tab3.check.isChecked():
                    sp.Popen('explorer '+file_name.replace('/', '\\'), shell=True)

    def _set(self):
        # 点击设置按钮事件
        setting(set_file_name='settings\\merger_settings.json',
                cache_file_name='cache\\merger_cache.th',
                list_name=self.tab1.book_list,
                open_program=self.tab1.open_program, cache=True)

    def gen1(self, pos):
        generate_menu(pos, self.tab1)

    def gen2(self, pos):
        generate_menu(pos, self.tab2)

    def gen3(self, pos):
        generate_menu(pos, self.tab3)

    def add1(self):
        add(self.tab1)

    def add2(self):
        if len(self.tab2.book_list) == 0:
            f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                                    self.tab2.s_dir, '(*.pdf)')
            if _:
                self.tab2.book_list = pdf_split(f_name)
                book_len = len(self.tab2.book_list)
                reset_table(book_len, self.tab2)
                for item in self.tab2.book_list:
                    set_icon(item, self.tab2)
            else:
                pass

    def add3(self):
        if len(self.tab3.book_list) == 0:
            add(self.tab3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
