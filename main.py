# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import json
import fitz
from scripts import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QColorDialog,
)
# Attention: ignore all warnings in fitz.open(.)


class Main(MainR):
    """
    main widow
    """
    def __init__(self):
        super(Main, self).__init__()
        content = setting_warning(
            'settings\\main_settings.json',
            )
        if os.path.exists(
                'settings\\metadata.json',
        ):
            with open(
                'settings\\metadata.json',
                mode='r',
                encoding='utf-8',
            ) as m:
                metadata = json.load(m)
            self.Author = metadata["Author"]
        else:
            self.Author = None
        self.move(100, 20)
        self.colour_r = 0.1
        self.colour_g = 0.1
        self.colour_b = 0.1
        self.perm_int = 4028
        self.s_dir = content["start dir"]
        self.o_dir = content["save dir"]
        self.js_dir = content["pdf.js dir"]
        self.font_dir = content["font dir"]
        self.language = content["language"]
        self.SettingCD = Setting()
        self.PermMenuCD = PermMenu()
        self.Viewer = PDFViewR()
        self.About = AboutR()
        self.tab1.book_list = list()
        self.tab2.book_list = list()
        self.tab3.book_list = list()
        self.tab4.book_list = list()
        self.tab2.book_name = str()
        self.tab4.book_name = str()
        self.tab2.click_counts = 0
        self.tab4.metadata = None
        self.tab1.x, self.tab1.y = 0, 0
        self.tab2.x, self.tab2.y = 0, 0
        self.tab3.x, self.tab3.y = 0, 0
        self.tab4.x, self.tab4.y = 0, 0
        self.tab1.w_col, self.tab1.w_row = COLUMN_COUNTER, 1
        self.tab2.w_row, self.tab2.w_col = 2, COLUMN_COUNTER
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab4.w_row, self.tab4.w_col = 2, 1
        self.tab1.table.setRowCount(self.tab1.w_row)
        self.tab2.table.setRowCount(self.tab2.w_row)
        self.tab3.table.setRowCount(self.tab3.w_row)
        self.tab4.table.setRowCount(self.tab4.w_row)
        self.tab1.table.setColumnCount(self.tab1.w_col)
        self.tab2.table.setColumnCount(self.tab2.w_col)
        self.tab3.table.setColumnCount(self.tab3.w_col)
        self.tab4.table.setColumnCount(self.tab4.w_col)
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
        for i in range(self.tab4.w_row):
            self.tab4.table.setRowHeight(i, self.tab4.table.width()*4//3)
        self.tab3.table.setColumnWidth(0, self.tab3.table.width())
        self.tab3.table.setRowHeight(0, self.tab3.table.height())
        self.tab4.table.setColumnWidth(0, self.tab4.table.width())
        self.tab1.table.customContextMenuRequested.connect(self.gen1)
        self.tab2.table.customContextMenuRequested.connect(self.gen2)
        self.tab3.table.customContextMenuRequested.connect(self.gen3)
        self.tab1.button1.clicked.connect(self.add1)
        self.tab1.button2.clicked.connect(self.save1)
        self.tab1.button3.clicked.connect(self._set)
        self.tab1.button4.clicked.connect(self.clean1)
        self.tab1.button5.clicked.connect(self._about)
        self.tab2.button1.clicked.connect(self.add2)
        self.tab2.button2.clicked.connect(self.save2)
        self.tab2.button3.clicked.connect(self._set)
        self.tab2.button4.clicked.connect(self.clean2)
        self.tab2.button5.clicked.connect(self.table_flip)
        self.tab3.button1.clicked.connect(self.add3)
        self.tab3.button2.clicked.connect(self.save3)
        self.tab3.button3.clicked.connect(self._set)
        self.tab3.button4.clicked.connect(self.get_colour)
        self.tab3.button5.clicked.connect(self.preview)
        self.tab3.line3.returnPressed.connect(self.preview)
        self.tab3.line4.returnPressed.connect(self.preview)
        self.tab3.line5.returnPressed.connect(self.preview)
        self.tab3.check1.stateChanged.connect(self.enable_preview)
        self.tab3.check2.stateChanged.connect(self.enable_perm_set)
        self.tab4.button1.clicked.connect(self.add4)
        self.tab4.button2.clicked.connect(self.save4)
        set_language(self)

    def enable_preview(self):
        if self.tab3.check1.isChecked():
            self.tab3.text.textChanged.connect(self.preview)
        else:
            self.tab3.text.textChanged.disconnect(self.preview)

    def enable_perm_set(self):
        if self.tab3.check2.isChecked():
            self.tab3.button6.clicked.connect(self._perm_set)
        else:
            self.tab3.button6.clicked.disconnect(self._perm_set)
            self.perm_int = 4028

    def _about(self):
        self.About.show()

    def view(self,
             index=None,
             widget=None,
             f_name=None):
        pdf_js = 'file:///{}/web/viewer.html'.format(
            self.js_dir.replace("\\", "/")
        )  # important format
        if f_name is not None:
            self.Viewer.view(
                f_name,
                pdf_js,
            )
        else:
            self.Viewer.view(
                widget.book_list[index],
                pdf_js,
            )
        self.Viewer.show()

    def save1(self):
        if len(self.tab1.book_list) != 0:
            doc0 = fitz.open(self.tab1.book_list[0])
            if not self.tab1.book_list[0].endswith('.pdf'):
                pdf_bites0 = doc0.convert_to_pdf()
                doc0 = fitz.open('pdf', pdf_bites0)
            for item in self.tab1.book_list[1:]:
                doc = fitz.open(item)
                if not item.endswith('.pdf'):
                    pdf_bites = doc.convert_to_pdf()
                    doc = fitz.open('pdf', pdf_bites)
                doc0.insertPDF(doc)
                doc.close()
            set_metadata0(
                doc=doc0,
                author=self.Author,
            )
            file_name, ok = QFileDialog.getSaveFileName(
                None,
                "save",
                self.o_dir + "new.pdf",
                ".pdf",
            )
            if ok:
                doc0.save(
                    file_name.replace('/', '\\'),
                    garbage=1,
                )
                doc0.close()
                self.view(f_name=file_name)

    def save2(self):
        if len(self.tab2.book_list) != 0:
            doc0 = fitz.open(self.tab2.book_name)
            doc0.select(self.tab2.book_list)
            file_name, ok = QFileDialog.getSaveFileName(
                None,
                "save",
                self.o_dir + "new.pdf",
                ".pdf",
            )
            set_metadata0(
                doc=doc0,
                author=self.Author,
            )
            if ok:
                doc0.save(
                    file_name.replace('/', '\\'),
                    garbage=1,
                )
                doc0.close()
                self.view(f_name=file_name)

    def save3(self):
        u_password = self.tab3.line1.text()
        o_password = self.tab3.line2.text()
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text())/100
        if len(self.tab3.book_list) != 0:
            file_name, ok = QFileDialog.getSaveFileName(
                None,
                "save",
                self.o_dir + "new.pdf",
                ".pdf",
            )
            if ok:
                security(
                    input_pdf=self.tab3.book_list[0],
                    output_pdf=file_name.replace('/', '\\'),
                    text=watermark,
                    rotate=rotation,
                    colour=(self.colour_r,
                            self.colour_g,
                            self.colour_b,),
                    font_size=font_size,
                    opacity=opacity,
                    owner_pass=o_password,
                    user_pass=u_password,
                    font_file=self.font_dir,
                    perm=self.perm_int,
                )
                if self.tab3.check.isChecked():
                    self.view(f_name=file_name)

    def save4(self):
        title = self.tab4.line1.text()
        author = self.tab4.line2.text()
        subject = self.tab4.line3.text()
        keywords = self.tab4.line4.text()
        toc = plaintext2toc(self.tab4.text.toPlainText())
        if len(self.tab4.book_list) != 0:
            file_name, ok = QFileDialog.getSaveFileName(
                None,
                "save",
                self.o_dir + "new.pdf",
                ".pdf",
            )
            if ok:
                doc = fitz.open(self.tab4.book_name)
                metadata = set_metadata1(
                    self.tab4.metadata,
                    title=title,
                    author=author,
                    subject=subject,
                    keywords=keywords,
                )
                doc.set_toc(toc)
                doc.set_metadata(metadata)
                doc.save(
                    file_name.replace('/', '\\'),
                    garbage=1,
                )
                doc.close()

    def _set(self):
        self.SettingCD.show()
        self.SettingCD.signal.connect(self.get_data)

    def gen1(self, pos):
        generate_menu(pos, self.tab1, main=self)

    def gen2(self, pos):
        generate_menu(pos, self.tab2, select=1, main=self)

    def gen3(self, pos):
        generate_menu(pos, self.tab3, main=self)

    def add1(self):
        f_name, _ = QFileDialog.getOpenFileName(
            None,
            'Open files',
            self.s_dir,
            'PDF files (*.pdf);;images (*.png *.jpg *.jpeg *.bmp)',
        )
        if _ and (f_name.replace('/', '\\') not in self.tab1.book_list):
            self.tab1.book_list.append(
                f_name.replace('/', '\\'),
            )
            book_len = len(self.tab1.book_list)
            reset_table(book_len, self.tab1)
            self.tab1.table.clear()
            self.tab1.x, self.tab1.y = 0, 0
            for item in self.tab1.book_list:
                doc, state = open_pdf(item)
                if not state:
                    self.tab1.book_list.remove(item)
                else:
                    set_icon(doc, self.tab1)
                del doc
        else:
            pass

    def add2(self):
        if len(self.tab2.book_list) == 0:
            f_name, _ = QFileDialog.getOpenFileName(
                None,
                'Open files',
                self.s_dir,
                '(*.pdf)',
            )
            if _:
                self.tab2.book_name = f_name.replace(
                    '/',
                    '\\',
                )
                doc, state = open_pdf(self.tab2.book_name)
                if state:
                    b_l = pdf_split(doc)
                    self.tab2.book_list = b_l
                    book_len = len(self.tab2.book_list)
                    reset_table(book_len, self.tab2)
                    for item in self.tab2.book_list:
                        set_icon(
                            doc,
                            self.tab2,
                            _page=item,
                        )
                else:
                    self.tab2.book_name = str()
                del doc
            else:
                pass

    def add3(self):
        if len(self.tab3.book_list) == 0:
            add(self, self.tab3)

    def add4(self):
        f_name, _ = QFileDialog.getOpenFileName(
            None,
            'Open files',
            self.s_dir,
            '(*.pdf)',
        )
        if _:
            self.tab4.metadata = None
            self.tab4.table.clear()
            self.tab4.x, self.tab4.y = 0, 0
            self.tab4.book_name = f_name.replace(
                '/',
                '\\',
            )
            doc, state = open_pdf(self.tab4.book_name)
            if state:
                b_l = pdf_split(doc)
                self.tab4.book_list = b_l
                book_len = len(self.tab4.book_list)
                reset_table(book_len, self.tab4)
                for item in self.tab4.book_list:
                    set_icon(
                        doc,
                        self.tab4,
                        _page=item,
                    )
                self.tab4.metadata = doc.metadata
                plaintext = toc2plaintext(doc.get_toc())
                self.tab4.text.setPlainText(plaintext)
                self.tab4.line1.setText(self.tab4.metadata["title"])
                self.tab4.line2.setText(self.tab4.metadata["author"])
                self.tab4.line3.setText(self.tab4.metadata["subject"])
                self.tab4.line4.setText(self.tab4.metadata["keywords"])
                doc.close()
            else:
                self.tab4.book_name = str()
        else:
            pass

    def clean1(self):
        clean(self.tab1)

    def clean2(self):
        clean(self.tab2)

    def get_data(self,
                 par1,
                 par2,
                 par3,
                 par4,
                 par5):
        self.s_dir = par1
        self.o_dir = par2
        self.js_dir = par3
        self.font_dir = par4
        self.language = par5
        set_language(self)

    def get_perm_para(self,
                      par):
        self.perm_int = par

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
            if self.tab3.check1.isChecked():
                self.preview()

    def _perm_set(self):
        self.PermMenuCD.show()
        self.PermMenuCD.signal.connect(self.get_perm_para)

    def table_flip(self):
        doc = fitz.open(self.tab2.book_name)
        if self.tab2.click_counts % 2 == 0:
            self.tab2.button5.setToolTip('multi-columns')
            self.tab2.button5.setIcon(QIcon('ico\\col2.png'))
            self.tab2.w_col = 2
            self.tab2.table.clearContents()
            self.tab2.x, self.tab2.y = 0, 0
            book_len = len(self.tab2.book_list)
            reset_table(book_len, self.tab2)
            for item in self.tab2.book_list:
                set_icon(
                    doc,
                    self.tab2,
                    item,
                )
        if self.tab2.click_counts % 2 == 1:
            self.tab2.button5.setToolTip('dual columns')
            self.tab2.button5.setIcon(QIcon('ico\\col1.png'))
            self.tab2.w_col = COLUMN_COUNTER
            self.tab2.table.clearContents()
            self.tab2.x, self.tab2.y = 0, 0
            book_len = len(self.tab2.book_list)
            reset_table(book_len, self.tab2)
            for item in self.tab2.book_list:
                set_icon(
                    doc,
                    self.tab2,
                    item,
                )
        self.tab2.click_counts += 1

    def preview(self):
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text())/100
        if len(self.tab3.book_list) != 0 and watermark != '':
            doc = security(
                input_pdf=self.tab3.book_list[0],
                output_pdf=None,
                text=watermark,
                rotate=rotation,
                colour=(self.colour_r,
                        self.colour_g,
                        self.colour_b,),
                font_size=font_size,
                opacity=opacity,
                font_file=self.font_dir,
                save=False,
                select=0,
            )
            self.tab3.table.clearContents()
            self.tab3.x, self.tab3.y = 0, 0
            set_icon(doc, widget=self.tab3)
            doc.close()
            del doc


class Setting(SettingR):
    """
    setting window
    """
    signal = QtCore.pyqtSignal(
        str,
        str,
        str,
        str,
        str,
    )

    def __init__(self):
        super(Setting, self).__init__()
        content = setting_warning(
            'settings\\main_settings.json',
            )
        self.s_dir = content["start dir"]
        self.o_dir = content["save dir"]
        self.js_dir = content["pdf.js dir"]
        self.font_dir = content["font dir"]
        self.language = content["language"]
        self.line1.setText(self.s_dir)
        self.line2.setText(self.o_dir)
        self.line3.setText(self.js_dir)
        self.line4.setText(self.font_dir)
        self.combobox.setCurrentText(self.language)
        self.button1.clicked.connect(self.select1)
        self.button2.clicked.connect(self.select2)
        self.button4.clicked.connect(self.select3)
        self.button5.clicked.connect(self.select4)
        self.button3.clicked.connect(self.out)

    def out(self):
        self.signal.emit(
            self.line1.text(),
            self.line2.text(),
            self.line3.text(),
            self.line4.text(),
            self.combobox.currentText(),
        )
        _settings = {
            "start dir": self.line1.text(),
            "save dir": self.line2.text(),
            "pdf.js dir": self.line3.text(),
            "font dir": self.line4.text(),
            "language": self.combobox.currentText()
        }
        with open(
                'settings\\main_settings.json',
                'w',
                encoding='utf-8',
        ) as f:
            json.dump(
                _settings,
                f,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        self.close()

    def select1(self):
        choose(self.line1, self.s_dir)

    def select2(self):
        choose(self.line2, self.o_dir)

    def select3(self):
        choose(self.line3, os.getcwd())

    def select4(self):
        file_name, ok = QFileDialog.getOpenFileName(
            None,
            'Open files',
            'C:\\Windows\\Fonts',
            '',
        )
        if ok:
            self.line4.setText(
                file_name.replace('/', '\\'),
            )


class PermMenu(PermMenuR):
    """
    permission setting menu window
    """
    signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super(PermMenu, self).__init__()
        self.button.clicked.connect(self.out)

    def out(self):
        perm_int = 0
        if self.check1.isChecked():
            perm_int += fitz.PDF_PERM_PRINT
        if self.check2.isChecked():
            perm_int += fitz.PDF_PERM_MODIFY
        if self.check3.isChecked():
            perm_int += fitz.PDF_PERM_COPY
        if self.check4.isChecked():
            perm_int += fitz.PDF_PERM_ANNOTATE
        if self.check5.isChecked():
            perm_int += fitz.PDF_PERM_FORM
        if self.check6.isChecked():
            perm_int += fitz.PDF_PERM_ACCESSIBILITY
        if self.check7.isChecked():
            perm_int += fitz.PDF_PERM_ASSEMBLE
        if self.check8.isChecked():
            perm_int += fitz.PDF_PERM_PRINT_HQ
        self.signal.emit(perm_int)
        self.close()


if __name__ == '__main__':
    # 8964
    arg = sys.argv
    if arg[0] != 'main.py':
        os.chdir(
            os.path.dirname(
                arg[0],
            ),
        )
    app = QApplication(arg)
    main = Main()
    _set = Setting()
    _view = PDFViewR()
    _about = AboutR()
    if len(arg) == 1:
        main.show()
    if len(arg) == 2:
        main.Viewer.resize(1200, 800)
        main.view(f_name=arg[1])
    sys.exit(app.exec_())
    # **************** 8 9 6 4 ****************
