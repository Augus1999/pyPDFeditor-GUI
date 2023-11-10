# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
wrap the whole application to one function
"""
import os
import json
import shutil
import getpass
import subprocess as sp
from pathlib import Path
from typing import Dict
import fitz
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QColorDialog
from .language import set_language, lag_s, lag_p
from .windows import (
    MainR,
    PermMenuR,
    BUTTON_STYLE,
    SettingR,
    FontDialogR,
)
from .functions import (
    setting_warning,
    toc2plaintext,
    plaintext2toc,
    set_metadata0,
    set_metadata1,
    generate_menu,
    reset_table,
    pdf_split,
    find_font,
    warning,
    open_pdf,
    set_icon,
    add_watermark,
    choose,
    clean,
    add,
    render_pdf_page,
    save,
    copy,
    read_from_font_cache,
    store_font_path,
)


user_home = os.path.expanduser("~")
app_home = os.path.join(user_home, ".pyPDFeditor-GUI")


class Main(MainR):
    """
    main window class

    all app functions are written here
    """

    def __init__(self, system: str, version: str):
        super().__init__(system, version)
        content = setting_warning(os.path.join(app_home, "settings.json"), self)
        self.Author = getpass.getuser()
        self.move(100, 20)
        self.colour_r = 0.24
        self.colour_g = 0.24
        self.colour_b = 0.24
        self.perm_int = 4028
        self.s_dir = content["start dir"]
        self.o_dir = content["save dir"]
        self.font_dir = content["font dir"]
        self.language = content["language"]
        self.dir_store_state = content["dir store"]
        self.FontDialogCD = None
        self.PermMenuCD = PermMenu()
        self.PermMenuCD.set_language(self.language)
        self.SettingCD = None
        self.tab1.book_list = []
        self.tab2.book_list = []
        self.tab3.book_list = []
        self.tab4.book_list = []
        self.tab2.book = None
        self.tab4.book = None
        self.tab4.metadata = None
        self.tab3.xy = (0, 0)
        self.tab1.w_col, self.tab1.w_row = 4, 1
        self.tab2.w_row, self.tab2.w_col = 2, 4
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab4.w_row, self.tab4.w_col = 2, 1
        self.tab1.table.customContextMenuRequested.connect(
            lambda pos: generate_menu(pos, self.tab1, select=2, main=self),
        )
        self.tab2.table.customContextMenuRequested.connect(
            lambda pos: generate_menu(pos, self.tab2, select=1, main=self),
        )
        self.tab3.table.customContextMenuRequested.connect(
            lambda pos: generate_menu(pos, self.tab3, main=self),
        )
        self.tab1.button1.clicked.connect(self.add1)
        self.tab1.button2.clicked.connect(self.save1)
        self.tab1.button3.clicked.connect(self._set)
        self.tab1.button4.clicked.connect(lambda: clean(self.tab1))
        self.tab2.button1.clicked.connect(self.add2)
        self.tab2.button2.clicked.connect(self.save2)
        self.tab2.button3.clicked.connect(self._set)
        self.tab2.button4.clicked.connect(lambda: clean(self.tab2))
        self.tab3.button1.clicked.connect(self.add3)
        self.tab3.button2.clicked.connect(self.save3)
        self.tab3.button3.clicked.connect(self._set)
        self.tab3.button4.clicked.connect(self.get_colour)
        self.tab3.button5.clicked.connect(self.preview)
        self.tab3.button7.clicked.connect(self.get_font)
        self.tab3.button8.clicked.connect(
            lambda: (
                clean(self.tab3),
                self.tab3.text.clear(),
                self.tab3.line1.clear(),
                self.tab3.line2.clear(),
            )
        )
        self.tab3.button9.clicked.connect(
            lambda: os.remove(
                os.path.join(app_home, "font_dir_cache.json"),
            )
            if os.path.exists(
                os.path.join(app_home, "font_dir_cache.json"),
            )
            else None
        )  # delete font dir cache
        self.tab3.line3.returnPressed.connect(self.preview)
        self.tab3.line4.returnPressed.connect(self.preview)
        self.tab3.line5.returnPressed.connect(self.preview)
        self.tab3.check1.stateChanged.connect(self.enable_preview)
        self.tab3.check2.stateChanged.connect(self.enable_perm_set)
        self.tab4.button1.clicked.connect(self.add4)
        self.tab4.button2.clicked.connect(self.save4)
        self.tab4.button3.clicked.connect(self._set)
        self.tab4.button4.clicked.connect(
            lambda: (
                clean(self.tab4),
                self.tab4.text.clear(),
                self.tab4.line1.clear(),
                self.tab4.line2.clear(),
                self.tab4.line3.clear(),
                self.tab4.line4.clear(),
                self.tab4.label0.clear(),
            )
        )
        self.tab4.table.Index.connect(lambda par: self.show_index(par, self.tab4))
        set_language(self)

    def closeEvent(self, event) -> None:
        """
        write settings to settings.json
        """
        _settings = {
            "start dir": self.s_dir,
            "save dir": self.o_dir,
            "dir store": self.dir_store_state,
            "font dir": self.font_dir,
            "language": self.language,
        }
        if not os.path.exists(app_home):
            os.makedirs(app_home)
        if os.path.exists(os.path.join(app_home, "settings.json")):
            with open(
                os.path.join(app_home, "settings.json"),
                mode="r",
                encoding="utf-8",
            ) as c:
                states = json.load(c)
            if states == _settings:
                return  # if no new settings do not write
        with open(
            os.path.join(app_home, "settings.json"), mode="w", encoding="utf-8"
        ) as f:  # write new settings
            json.dump(
                _settings,
                f,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )

    def enable_preview(self) -> None:
        """
        enable preview mode
        """
        if self.tab3.check1.isChecked():
            self.tab3.text.textChanged.connect(self.preview)
            self.preview()
        else:
            self.tab3.text.textChanged.disconnect(self.preview)

    def enable_perm_set(self) -> None:
        """
        enable set permissions
        """
        if self.tab3.check2.isChecked():
            self.perm_int = 2820
            self.tab3.button6.clicked.connect(self._perm_set)
            self.tab3.button6.setStyleSheet(
                BUTTON_STYLE % ("more.svg", "more_h.svg", "more_p.svg"),
            )
        else:
            self.tab3.button6.setStyleSheet(
                BUTTON_STYLE % ("more_d.svg", "more_d.svg", "more_d.svg"),
            )
            self.tab3.button6.clicked.disconnect()
            self.perm_int = 4028  # value of all permissions

    def view(self, index=None, widget=None, f_name=None) -> None:
        """
        open file outside the application

        :param index: index of the file in book_list (necessary if f_name is None)
        :param widget: widget (necessary if f_name is None)
        :param f_name: file name
        :return: None
        """
        cmds = {
            "Windows": "explorer",
            "Linux": "xdg-open",
            "Darwin": "open",  # use `preview` if not work
            "Java": 0,
        }
        cmd = cmds[self.__system__] if self.__system__ in cmds else 0
        if not cmd:
            print(f'platform "{self.__system__}" cannot be recognised')
            return
        if f_name is not None:
            sp.Popen([cmd, Path(f_name)])
        else:
            sp.Popen([cmd, Path(widget.book_list[index].name)])

    def save1(self) -> None:
        """
        tab1 save function
        """
        if len(self.tab1.book_list) != 0:
            doc0 = copy(self.tab1.book_list[0])
            for item in self.tab1.book_list[1:]:
                doc0.insert_pdf(item)
            set_metadata0(doc=doc0, author=self.Author)
            file_name, ok = save(self, ".pdf")
            if ok:
                try:
                    doc0.save(file_name, garbage=1)
                    self.view(f_name=file_name)
                except RuntimeError:
                    warning(self)
                except ValueError:
                    warning(self)
            doc0.close()
            del doc0

    def save2(self) -> None:
        """
        tab2 save function
        """
        if len(self.tab2.book_list) != 0:
            doc0 = copy(self.tab2.book)
            doc0.select(self.tab2.book_list)
            file_name, ok = save(self, ".pdf")
            set_metadata0(doc=doc0, author=self.Author)
            if ok:
                try:
                    doc0.save(file_name, garbage=1)
                    self.view(f_name=file_name)
                except RuntimeError:
                    warning(self)
                except ValueError:
                    warning(self)
            doc0.close()
            del doc0

    def save3(self) -> None:
        """
        tab3 save function
        """
        u_password = self.tab3.line1.text()
        o_password = self.tab3.line2.text()
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text()) / 100
        if len(self.tab3.book_list) != 0:
            file_name, ok = save(self, ".pdf")
            if ok:
                doc = copy(self.tab3.book_list[0])
                doc = add_watermark(
                    doc=doc,
                    text=watermark,
                    rotate=rotation,
                    colour=(self.colour_r, self.colour_g, self.colour_b),
                    font_size=font_size,
                    opacity=opacity,
                    font_file=self.font_dir,
                    position=self.tab3.xy,
                )
                set_metadata0(doc=doc, author=self.Author)
                try:
                    doc.save(
                        file_name,
                        garbage=1,
                        permissions=self.perm_int,
                        encryption=fitz.PDF_ENCRYPT_AES_256,
                        user_pw=u_password if u_password != "" else None,
                        owner_pw=o_password if o_password != "" else None,
                    )
                    if self.tab3.check.isChecked():
                        self.view(f_name=file_name)
                except RuntimeError:
                    warning(self)
                except ValueError:
                    warning(self)
                doc.close()
            del doc

    def save4(self) -> None:
        """
        tab4 save function
        """
        title = self.tab4.line1.text()
        author = self.tab4.line2.text()
        subject = self.tab4.line3.text()
        keywords = self.tab4.line4.text()
        toc = plaintext2toc(self.tab4.text.toPlainText())
        if len(self.tab4.book_list) != 0:
            doc = self.tab4.book
            metadata = set_metadata1(
                self.tab4.metadata,
                title=title,
                author=author,
                subject=subject,
                keywords=keywords,
            )
            doc.set_toc(toc)
            doc.xref_set_key(-1, "Info", "null")  # remove all original xref
            doc.set_metadata(metadata)
            if doc.can_save_incrementally():
                doc.saveIncr()
                del doc
                return
            file_name, ok = save(self, ".pdf")
            if ok:
                try:
                    doc.save(file_name, garbage=1)
                except RuntimeError:
                    warning(self)
                except ValueError:
                    warning(self)
            del doc
            return

    def _set(self) -> None:
        self.SettingCD = Setting(
            {
                "start dir": self.s_dir,
                "save dir": self.o_dir,
                "language": self.language,
                "dir store": self.dir_store_state,
            },
        )
        self.SettingCD.show()
        self.SettingCD.signal.connect(self.get_data)

    def get_perm_para(self, par) -> None:
        """
        obtain permission code
        """
        self.perm_int = par

    def add1(self) -> None:
        """
        tab1 add file function
        """
        f_name, _ = add(
            self,
            "PDF files (*.pdf);;"
            "images (*.png *.jpg *.jpeg *.bmp *.tiff *.svg);;"
            "ebooks (*.epub *.xps *.fb2 *.cbz)",
        )
        if _:
            doc, state = open_pdf(f_name, self)
            if state:
                self.tab1.book_list.append(doc)
            book_len = len(self.tab1.book_list)
            reset_table(book_len, self.tab1)
            self.tab1.table.clear()
            set_icon(widget=self.tab1)
            del doc, state
        return

    def add2(self) -> None:
        """
        tab2 add function
        """
        if len(self.tab2.book_list) == 0:
            f_name, _ = add(self, "(*.pdf);;ebooks (*.epub *.xps *.fb2 *.cbz)")
            if _:
                doc, state = open_pdf(f_name, self)
                if state:
                    self.tab2.book = doc
                    b_l = pdf_split(doc)
                    self.tab2.book_list = b_l
                    book_len = len(self.tab2.book_list)
                    reset_table(book_len, self.tab2)
                    set_icon(widget=self.tab2)
                else:
                    self.tab2.book = None
                del doc, state
            return

    def add3(self) -> None:
        """
        tab3 add function
        """
        if len(self.tab3.book_list) == 0:
            f_name, _ = add(self, "(*.pdf)")
            if _:
                doc, state = open_pdf(f_name, self)
                if state:
                    self.tab3.book_list.append(doc)
                    reset_table(1, self.tab3)
                    set_icon(widget=self.tab3)
                else:
                    pass
                del doc, state
            return

    def add4(self) -> None:
        """
        tab4 add function
        """
        f_name, _ = add(self, "(*.pdf)")
        if _:
            self.tab4.metadata = None
            self.tab4.table.clear()
            doc, state = open_pdf(f_name, self)
            if state:
                self.tab4.book = doc
                b_l = pdf_split(doc)
                self.tab4.book_list = b_l
                book_len = len(self.tab4.book_list)
                reset_table(book_len, self.tab4)
                set_icon(widget=self.tab4, _scaled=0.9)
                self.tab4.metadata = doc.metadata
                plaintext = toc2plaintext(doc.get_toc())
                self.tab4.text.setPlainText(plaintext)
                self.tab4.line1.setText(self.tab4.metadata["title"])
                self.tab4.line2.setText(self.tab4.metadata["author"])
                self.tab4.line3.setText(self.tab4.metadata["subject"])
                self.tab4.line4.setText(self.tab4.metadata["keywords"])
            else:
                self.tab4.book = None
            del doc, state
        return

    def get_data(self, par1, par2, par3, par5) -> None:
        """
        obtain settings from setting window
        """
        self.s_dir = par1
        self.o_dir = par2
        self.dir_store_state = par3
        self.language = par5
        i = self.currentIndex()
        set_language(self)
        self.setCurrentIndex(i)

    def get_font_dir(self, par) -> None:
        """
        obtain font file directory from font window
        """
        self.font_dir = par
        if self.tab3.check1.isChecked():
            self.preview()

    def get_colour(self) -> None:
        """
        obtain colour data from colour dialog
        """
        _colour = QColorDialog.getColor(
            initial=QColor(
                int(255 * self.colour_r),
                int(255 * self.colour_g),
                int(255 * self.colour_b),
                int(255 * float(self.tab3.line4.text()) / 100),
            ),
            options=QColorDialog.ColorDialogOption(
                QColorDialog.ShowAlphaChannel,
            ),
            parent=self,
            title="Select Colour",
        )
        if _colour.isValid():
            self.colour_r = _colour.getRgbF()[0]
            self.colour_g = _colour.getRgbF()[1]
            self.colour_b = _colour.getRgbF()[2]
            self.tab3.line4.setText(f"{100 * _colour.getRgbF()[3]:.0f}")
            if self.tab3.check1.isChecked():
                self.preview()
        del _colour

    def get_font(self) -> None:
        """
        open font window
        """
        if os.path.exists(os.path.join(app_home, "font_dir_cache.json")):
            name_dict, file_dict = read_from_font_cache(
                os.path.join(app_home, "font_dir_cache.json"),
            )
        else:
            font_paths = QtCore.QStandardPaths.standardLocations(
                QtCore.QStandardPaths.FontsLocation,
            )
            name_dict, file_dict = find_font(font_paths)
            store_font_path(name_dict, os.path.join(app_home, "font_dir_cache.json"))
        self.FontDialogCD = FontDialog(
            self.font_dir,
            name_dict,
            file_dict,
        )
        self.FontDialogCD.show()
        self.FontDialogCD.signal.connect(self.get_font_dir)

    def _perm_set(self) -> None:
        self.PermMenuCD.set_language(self.language)
        self.PermMenuCD.show()
        self.PermMenuCD.signal.connect(self.get_perm_para)

    def preview(self) -> None:
        """
        preview watermark effects
        """
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text()) / 100
        if len(self.tab3.book_list) != 0:
            doc = fitz.Document()
            doc.insert_pdf(self.tab3.book_list[0], 0, 0)
            doc = add_watermark(
                doc=doc,
                text=watermark,
                rotate=rotation,
                colour=(self.colour_r, self.colour_g, self.colour_b),
                font_size=font_size,
                opacity=opacity,
                font_file=self.font_dir,
                position=self.tab3.xy,
            )
            self.tab3.table.clearContents()
            set_icon(widget=self.tab3, doc=doc)
            doc.close()
            del doc

    @staticmethod
    def show_index(par, widget):
        """
        show recent clicked page number
        """
        index = par[0] * widget.w_col + par[1]  # get position
        if len(widget.book_list) != 0:
            widget.label0.setText(f"📖 page {index + 1}")


class Setting(SettingR):
    """
    setting window
    """

    signal = QtCore.pyqtSignal(
        str,
        str,
        bool,
        str,
    )

    def __init__(self, set_dict: dict):
        super().__init__()
        self.s_dir = set_dict["start dir"]
        self.o_dir = set_dict["save dir"]
        self.language = set_dict["language"]
        self.dir_store_state = set_dict["dir store"]
        self.check.setChecked(self.dir_store_state)
        self.combobox.setCurrentText(self.language)
        self._enable_select()
        self.check.stateChanged.connect(self._enable_select)
        self.combobox.currentTextChanged.connect(
            lambda: lag_s(self, self.combobox.currentText()),
        )
        self.line1.setText(self.s_dir)
        self.line2.setText(self.o_dir)
        lag_s(self, self.combobox.currentText())

    def _enable_select(self):
        if self.check.isChecked():
            self.button1.setStyleSheet(
                BUTTON_STYLE % ("folder_d.svg", "folder_d.svg", "folder_d.svg"),
            )
            self.button2.setStyleSheet(
                BUTTON_STYLE % ("folder_d.svg", "folder_d.svg", "folder_d.svg"),
            )
            try:
                self.button1.clicked.disconnect()
                self.button2.clicked.disconnect()
            except TypeError:
                pass
            self.line1.setReadOnly(True)
            self.line2.setReadOnly(True)
        else:
            self.button1.setStyleSheet(
                BUTTON_STYLE % ("folder.svg", "folder_h.svg", "folder_p.svg"),
            )
            self.button2.setStyleSheet(
                BUTTON_STYLE % ("folder.svg", "folder_h.svg", "folder_p.svg"),
            )
            self.button1.clicked.connect(lambda: choose(self.line1, self.s_dir))
            self.button2.clicked.connect(lambda: choose(self.line2, self.o_dir))
            self.line1.setReadOnly(False)
            self.line2.setReadOnly(False)

    def closeEvent(self, event) -> None:
        """
        re-write closeEvent
        """
        self.signal.emit(
            self.line1.text(),
            self.line2.text(),
            self.check.isChecked(),
            self.combobox.currentText(),
        )
        self.close()
        del self


class PermMenu(PermMenuR):
    """
    permission setting menu window
    """

    signal = QtCore.pyqtSignal(int)

    def set_language(self, language: str) -> None:
        """
        set language
        """
        lag_p(self, language)

    def closeEvent(self, event) -> None:
        """
        close event
        """
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
        del self


class FontDialog(FontDialogR):
    """
    font menu window
    """

    signal = QtCore.pyqtSignal(str)

    def __init__(
        self, font_dir: str, name_dict: Dict[str, str], file_dict: Dict[str, str]
    ):
        super().__init__()
        self.name_dict = name_dict
        for item in name_dict:
            self.combobox.addItem(item)
        try:
            current_font = file_dict[font_dir]
            self.combobox.setCurrentText(current_font)
        except KeyError:
            pass
        self.change_text_font()
        self.combobox.currentTextChanged.connect(self.change_text_font)

    def change_text_font(self) -> None:
        """
        display the font
        """
        doc = fitz.Document()
        fitz.utils.new_page(doc, -1, 380, 220)
        r1 = fitz.Rect(10, 10, 370, 210)
        page = doc.load_page(0)
        shape = fitz.utils.Shape(page)
        shape.draw_rect(r1)
        shape.finish()
        shape.insert_textbox(
            r1,
            "Hello\nこんにちは\n你好\n3.14159",
            color=(0.24, 0.24, 0.24),
            align=1,
            fontsize=25,
            fontfile=self.name_dict[self.combobox.currentText()],
            fontname="ext_0",
        )
        shape.commit()
        cover = render_pdf_page(page)
        self.label.setPixmap(QPixmap(cover))
        doc.close()
        fitz.TOOLS.store_shrink(100)  # delete MuPDF cache
        del cover, shape, page, r1, doc

    def closeEvent(self, event) -> None:
        """
        close event
        """
        self.signal.emit(self.name_dict[self.combobox.currentText()])
        self.close()
        del self


def reset() -> None:
    """
    remove all settings, caches and icons
    """
    setting_path = os.path.join(app_home, "settings.json")
    cache_path = os.path.join(app_home, "font_dir_cache.json")
    if os.path.exists(setting_path):
        os.remove(setting_path)
    if os.path.exists(cache_path):
        os.remove(cache_path)
    print("reset finished")


def remove() -> None:
    """
    remove the whole application
    """
    c = input("Are you sure to remove the whole application? n/Y" "\n>>>")
    if c.lower() == "y":
        sp.call("pip uninstall pypdfeditor-gui", shell=True)
        if os.path.exists(app_home):
            shutil.rmtree(app_home)
        print("process finished")
