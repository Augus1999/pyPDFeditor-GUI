# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import sys
import json
import fitz
import subprocess as sp
from scripts import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QColorDialog


class Main(MainR):
    """
    main widow
    """
    def __init__(self):
        super(Main, self).__init__()
        content = setting_warning('settings\\main_settings.json')
        self.s_dir, self.o_dir = content["start dir"], content["save dir"]
        self.colour_r = content["colour"]["R"]
        self.colour_g = content["colour"]["G"]
        self.colour_b = content["colour"]["B"]
        self.ChildDialog = Setting()
        self.tab1.book_list = list()
        self.tab2.book_list = list()
        self.tab3.book_list = list()
        self.tab1.x, self.tab1.y = 0, 0
        self.tab2.x, self.tab2.y = 0, 0
        self.tab3.x, self.tab3.y = 0, 0
        self.tab1.col, self.tab1.crow = -1, -1
        self.tab2.col, self.tab2.crow = -1, -1
        self.tab3.col, self.tab3.crow = -1, -1
        self.tab1.w_col, self.tab1.w_row = 4, 1
        self.tab2.w_row, self.tab2.w_col = 2, 4
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab1.table.setRowCount(self.tab1.w_row)
        self.tab2.table.setRowCount(self.tab2.w_row)
        self.tab3.table.setRowCount(self.tab3.w_row)
        self.tab1.table.setColumnCount(self.tab1.w_col)
        self.tab2.table.setColumnCount(self.tab2.w_col)
        self.tab3.table.setColumnCount(self.tab3.w_col)
        for i in range(self.tab1.w_col):
            self.tab1.table.setColumnWidth(i, (895-15)//self.tab1.w_col)
        for i in range(self.tab1.w_row):
            self.tab1.table.setRowHeight(i, ((895-15)//self.tab1.w_col)*4//3)
        for i in range(self.tab2.w_col):
            self.tab2.table.setColumnWidth(i, (895-15)//self.tab2.w_col)
        for i in range(self.tab2.w_row):
            self.tab2.table.setRowHeight(i, ((895-15)//self.tab2.w_col)*4//3)
        self.tab3.table.setColumnWidth(0, 397)
        self.tab3.table.setRowHeight(0, 530)
        self.tab1.table.customContextMenuRequested.connect(self.gen1)
        self.tab2.table.customContextMenuRequested.connect(self.gen2)
        self.tab3.table.customContextMenuRequested.connect(self.gen3)
        self.tab1.button1.clicked.connect(self.add1)
        self.tab1.button2.clicked.connect(self.save1)
        self.tab1.button3.clicked.connect(self._set)
        self.tab2.button1.clicked.connect(self.add2)
        self.tab2.button2.clicked.connect(self.save2)
        self.tab2.button3.clicked.connect(self.clean)
        self.tab3.button1.clicked.connect(self.add3)
        self.tab3.button2.clicked.connect(self.save3)
        if float(self.colour_r) > 1:
            self.colour_r = str(float(self.colour_r)/255)
        if float(self.colour_g) > 1:
            self.colour_g = str(float(self.colour_g)/255)
        if float(self.colour_b) > 1:
            self.colour_b = str(float(self.colour_b)/255)

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
                sp.Popen('explorer ' + file_name.replace('/', '\\'), shell=True)

    def save2(self):
        if len(self.tab2.book_list) != 0:
            doc0 = fitz.open(self.tab2.book_list[0])
            for item in self.tab2.book_list[1:]:
                doc = fitz.open(item)
                doc0.insertPDF(doc)
                doc.close()
            file_name, ok = QFileDialog.getSaveFileName(None, "save",
                                                        self.o_dir + "new.pdf",
                                                        ".pdf")
            if ok:
                doc0.save(file_name.replace('/', '\\'))
                doc0.close()
                clean()
                sp.Popen('explorer ' + file_name.replace('/', '\\'), shell=True)

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
                security(self.tab3.book_list[0], file_name.replace('/', '\\'), watermark, 0,
                         (float(self.colour_r), float(self.colour_g), float(self.colour_b),),
                         font_size=font_size, opacity=opacity, owner_pass=o_password, user_pass=u_password)
                if self.tab3.check.isChecked():
                    sp.Popen('explorer '+file_name.replace('/', '\\'), shell=True)

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
        if _:
            if f_name.replace('/', '\\') not in self.tab1.book_list:
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
                b_l = pdf_split(f_name.replace('/', '\\'))
                if len(b_l) != 0:
                    self.tab2.book_list = b_l
                    book_len = len(self.tab2.book_list)
                    reset_table(book_len, self.tab2)
                    for item in self.tab2.book_list:
                        set_icon(item, self.tab2)
                else:
                    pass
            else:
                pass

    def add3(self):
        if len(self.tab3.book_list) == 0:
            add(self, self.tab3)

    def clean(self):
        clean(select=1)
        self.tab2.book_list = list()
        self.tab2.x, self.tab2.y = 0, 0
        self.tab2.col, self.tab2.crow = -1, -1
        self.tab2.table.clear()

    def get_data(self, par1, par2, par3):
        self.s_dir = par1
        self.o_dir = par2
        self.colour_r = par3[0]
        self.colour_g = par3[1]
        self.colour_b = par3[2]


class Setting(SettingR):
    """
    setting window
    """
    signal = QtCore.pyqtSignal(str, str, list)

    def __init__(self):
        super(Setting, self).__init__()
        content = setting_warning('settings\\main_settings.json')
        self.s_dir, self.o_dir = content["start dir"], content["save dir"]
        self.colour_r = content["colour"]["R"]
        self.colour_g = content["colour"]["G"]
        self.colour_b = content["colour"]["B"]
        self.line1.setText(self.s_dir)
        self.line2.setText(self.o_dir)
        self.line3.setText(self.colour_r)
        self.line4.setText(self.colour_g)
        self.line5.setText(self.colour_b)
        self.button1.clicked.connect(self.select1)
        self.button2.clicked.connect(self.select2)
        self.button3.clicked.connect(self.out)
        self.button4.clicked.connect(self.colour)

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
        if len(root) != 0:
            self.line1.setText(root.replace('/', '\\'))

    def select2(self):
        root = QtWidgets.QFileDialog.getExistingDirectory(None, "choose", self.o_dir)
        if len(root) != 0:
            self.line2.setText(root.replace('/', '\\'))

    def colour(self):
        _colour = QColorDialog.getColor()
        if _colour.isValid():
            self.line3.setText('%2.1f' % _colour.getRgbF()[0])
            self.line4.setText('%2.1f' % _colour.getRgbF()[1])
            self.line5.setText('%2.1f' % _colour.getRgbF()[2])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    _set = Setting()
    main.show()
    sys.exit(app.exec_())
