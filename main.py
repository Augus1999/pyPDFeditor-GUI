# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import json
import fitz
import subprocess as sp
from scripts import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QColorDialog


class Main(MainR):
    """
    main widow
    """
    def __init__(self):
        super(Main, self).__init__()
        content = setting_warning(
            os.getcwd()+'\\'+'settings\\main_settings.json',
            )
        self.colour_r = 0.1
        self.colour_g = 0.1
        self.colour_b = 0.1
        self.s_dir = content["start dir"]
        self.o_dir = content["save dir"]
        self.language = content["language"]
        self.ChildDialog = Setting()
        self.tab1.book_list = list()
        self.tab2.book_list = list()
        self.tab3.book_list = list()
        self.tab2.book_name = str()
        self.tab1.x, self.tab1.y = 0, 0
        self.tab2.x, self.tab2.y = 0, 0
        self.tab3.x, self.tab3.y = 0, 0
        self.tab1.col, self.tab1.crow = -1, -1
        self.tab2.col, self.tab2.crow = -1, -1
        self.tab3.col, self.tab3.crow = -1, -1
        self.tab1.w_col, self.tab1.w_row = COLUMN_COUNTER, 1
        self.tab2.w_row, self.tab2.w_col = 2, COLUMN_COUNTER
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab1.table.setRowCount(self.tab1.w_row)
        self.tab2.table.setRowCount(self.tab2.w_row)
        self.tab3.table.setRowCount(self.tab3.w_row)
        self.tab1.table.setColumnCount(self.tab1.w_col)
        self.tab2.table.setColumnCount(self.tab2.w_col)
        self.tab3.table.setColumnCount(self.tab3.w_col)
        tab1_width = (self.tab1.table.width()-15)//self.tab1.w_col
        tab2_width = (self.tab2.table.width()-15)//self.tab2.w_col
        for i in range(self.tab1.w_col):
            self.tab1.table.setColumnWidth(i, tab1_width)
        for i in range(self.tab1.w_row):
            self.tab1.table.setRowHeight(i, tab1_width*4//3)
        for i in range(self.tab2.w_col):
            self.tab2.table.setColumnWidth(i, tab2_width)
        for i in range(self.tab2.w_row):
            self.tab2.table.setRowHeight(i, tab2_width*4//3)
        self.tab3.table.setColumnWidth(0, self.tab3.table.width())
        self.tab3.table.setRowHeight(0, self.tab3.table.height())
        self.tab1.table.customContextMenuRequested.connect(self.gen1)
        self.tab2.table.customContextMenuRequested.connect(self.gen2)
        self.tab3.table.customContextMenuRequested.connect(self.gen3)
        self.tab1.button1.clicked.connect(self.add1)
        self.tab1.button2.clicked.connect(self.save1)
        self.tab1.button3.clicked.connect(self._set)
        self.tab1.button4.clicked.connect(self.clean1)
        self.tab2.button1.clicked.connect(self.add2)
        self.tab2.button2.clicked.connect(self.save2)
        self.tab2.button3.clicked.connect(self._set)
        self.tab2.button4.clicked.connect(self.clean2)
        self.tab3.button1.clicked.connect(self.add3)
        self.tab3.button2.clicked.connect(self.save3)
        self.tab3.button3.clicked.connect(self._set)
        self.tab3.button4.clicked.connect(self.get_colour)
        self._change()

    def _change(self):
        self.addTab(
            self.tab1,
            QIcon('ico\\tab1.png'),
            LANGUAGE[self.language][0],
        )
        self.addTab(
            self.tab2,
            QIcon('ico\\tab2.png'),
            LANGUAGE[self.language][1],
        )
        self.addTab(
            self.tab3,
            QIcon('ico\\tab3.png'),
            LANGUAGE[self.language][2],
        )

    def save1(self):
        if len(self.tab1.book_list) != 0:
            doc0 = fitz.open(self.tab1.book_list[0])
            for item in self.tab1.book_list[1:]:
                doc = fitz.open(item)
                doc0.insertPDF(doc)
                doc.close()
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                doc0.save(file_name.replace('/', '\\'))
                doc0.close()
                sp.Popen(
                    'explorer ' + file_name.replace('/', '\\'),
                    shell=True,
                    )

    def save2(self):
        if len(self.tab2.book_list) != 0:
            doc0 = fitz.open(self.tab2.book_name)
            doc0.select(self.tab2.book_list)
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                doc0.save(file_name.replace('/', '\\'))
                doc0.close()
                sp.Popen(
                    'explorer ' + file_name.replace('/', '\\'),
                    shell=True,
                    )

    def save3(self):
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
                security(
                    input_pdf=self.tab3.book_list[0],
                    output_pdf=file_name.replace('/', '\\'),
                    text=watermark,
                    rotate=0,
                    colour=(self.colour_r,
                            self.colour_g,
                            self.colour_b,),
                    font_size=font_size,
                    opacity=opacity,
                    owner_pass=o_password,
                    user_pass=u_password,
                    )
                if self.tab3.check.isChecked():
                    sp.Popen(
                        'explorer '+file_name.replace('/', '\\'),
                        shell=True,
                        )

    def _set(self):
        self.ChildDialog.show()
        self.ChildDialog.signal.connect(self.get_data)

    def gen1(self, pos):
        generate_menu(pos, self.tab1)

    def gen2(self, pos):
        generate_menu(pos, self.tab2, select=1, main=self)

    def gen3(self, pos):
        generate_menu(pos, self.tab3)

    def add1(self):
        f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                                self.s_dir, '(*.pdf)')
        if _ and (f_name.replace('/', '\\') not in self.tab1.book_list):
            self.tab1.book_list.append(f_name.replace('/', '\\'))
            book_len = len(self.tab1.book_list)
            reset_table(book_len, self.tab1)
            self.tab1.table.clear()
            self.tab1.x, self.tab1.y = 0, 0
            for item in self.tab1.book_list:
                if not set_icon(item, self.tab1):
                    self.tab1.book_list.remove(item)
                else:
                    pass
        else:
            pass

    def add2(self):
        if len(self.tab2.book_list) == 0:
            f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                                    self.s_dir, '(*.pdf)')
            if _:
                self.tab2.book_name = f_name.replace('/', '\\')
                b_l = pdf_split(self.tab2.book_name)
                if len(b_l) != 0:
                    self.tab2.book_list = b_l
                    book_len = len(self.tab2.book_list)
                    reset_table(book_len, self.tab2)
                    for item in self.tab2.book_list:
                        set_icon(self.tab2.book_name, self.tab2, item)
                else:
                    pass
            else:
                pass

    def add3(self):
        if len(self.tab3.book_list) == 0:
            add(self, self.tab3)

    def clean1(self):
        clean(self.tab1)

    def clean2(self):
        clean(self.tab2)

    def get_data(self, par1, par2, par3):
        self.s_dir = par1
        self.o_dir = par2
        self.language = par3
        self._change()

    def get_colour(self):
        _colour = QColorDialog.getColor()
        if _colour.isValid():
            self.colour_r = _colour.getRgbF()[0]
            self.colour_g = _colour.getRgbF()[1]
            self.colour_b = _colour.getRgbF()[2]
            self.tab3.text.setStyleSheet(
                'font-size:14pt;border-radius:5px;'
                'background-color:rgba(245,233,190,80);'
                'color:rgb({},{},{});font-family:calibri'.
                format(
                    self.colour_r*255,
                    self.colour_g*255,
                    self.colour_b*255,
                )
            )


class Setting(SettingR):
    """
    setting window
    """
    signal = QtCore.pyqtSignal(str, str, str)

    def __init__(self):
        super(Setting, self).__init__()
        content = setting_warning(
            os.getcwd()+'\\{}'.format('settings\\main_settings.json'),
            )
        self.s_dir = content["start dir"]
        self.o_dir = content["save dir"]
        self.language = content["language"]
        self.line1.setText(self.s_dir)
        self.line2.setText(self.o_dir)
        self.button1.clicked.connect(self.select1)
        self.button2.clicked.connect(self.select2)
        self.button3.clicked.connect(self.out)

    def out(self):
        self.signal.emit(self.line1.text(),
                         self.line2.text(),
                         self.combobox.currentText(),)
        _settings = {
            "start dir": self.line1.text(),
            "save dir": self.line2.text(),
            "language": self.combobox.currentText()
        }
        with open('settings\\main_settings.json', 'w', encoding='utf-8') as f:
            json.dump(_settings, f)
        self.close()

    def select1(self):
        root = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "choose",
            self.s_dir,
            )
        if len(root) != 0:
            self.line1.setText(root.replace('/', '\\'))

    def select2(self):
        root = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "choose",
            self.o_dir,
            )
        if len(root) != 0:
            self.line2.setText(root.replace('/', '\\'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    _set = Setting()
    main.show()
    sys.exit(app.exec_())
