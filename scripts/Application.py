# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import sys
import json
import fitz
import getpass
import subprocess as sp
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QColorDialog, QTabWidget
from .language import set_language, lag_s, lag_p
from .windows import (MainR, PermMenuR, BUTTON_STYLE,
                      SettingR, FontDialogR,)
from .functions import (setting_warning, toc2plaintext, plaintext2toc,
                        set_metadata0, set_metadata1, generate_menu,
                        reset_table, pdf_split, find_font, _warning,
                        open_pdf, set_icon, add_watermark, choose, clean,
                        add, render_pdf_page, save, copy,)


class Main(MainR):
    """
    main widow
    """
    def __init__(self, system: str, version: str):
        super(Main, self).__init__()
        self.__system__ = system
        self.__version__ = version
        content = setting_warning(
            'settings\\settings.json',
            self,
            )
        self.BORDER_WIDTH = 8
        self.monitor_info = None
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
        self.tab1.book_list = list()
        self.tab2.book_list = list()
        self.tab3.book_list = list()
        self.tab4.book_list = list()
        self.tab2.book = None
        self.tab4.book = None
        self.tab4.metadata = None
        self.tab1.w_col, self.tab1.w_row = 4, 1
        self.tab2.w_row, self.tab2.w_col = 2, 4
        self.tab3.w_row, self.tab3.w_col = 1, 1
        self.tab4.w_row, self.tab4.w_col = 2, 1
        self.tab1.table.customContextMenuRequested.connect(
            lambda pos: generate_menu(pos, self.tab1, main=self),
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
        self.tab3.button8.clicked.connect(lambda: (
            clean(self.tab3),
            self.tab3.text.clear(),
            self.tab3.line1.clear(),
            self.tab3.line2.clear(),
        ))
        self.tab3.line3.returnPressed.connect(self.preview)
        self.tab3.line4.returnPressed.connect(self.preview)
        self.tab3.line5.returnPressed.connect(self.preview)
        self.tab3.check1.stateChanged.connect(self.enable_preview)
        self.tab3.check2.stateChanged.connect(self.enable_perm_set)
        self.tab4.button1.clicked.connect(self.add4)
        self.tab4.button2.clicked.connect(self.save4)
        self.tab4.button3.clicked.connect(self._set)
        self.tab4.button4.clicked.connect(lambda: (
            clean(self.tab4),
            self.tab4.text.clear(),
            self.tab4.line1.clear(),
            self.tab4.line2.clear(),
            self.tab4.line3.clear(),
            self.tab4.line4.clear(),
            self.tab4.label0.clear(),
        ))
        self.tab4.table.Index.connect(lambda par: self.showIndex(par, self.tab4))
        self.btn_min_0.clicked.connect(self.showMinimized)
        self.btn_min_1.clicked.connect(self.showMinimized)
        self.btn_min_2.clicked.connect(self.showMinimized)
        self.btn_min_3.clicked.connect(self.showMinimized)
        self.btn_min_4.clicked.connect(self.showMinimized)
        self.btn_max_0.clicked.connect(self.windowChange)
        self.btn_max_1.clicked.connect(self.windowChange)
        self.btn_max_2.clicked.connect(self.windowChange)
        self.btn_max_3.clicked.connect(self.windowChange)
        self.btn_max_4.clicked.connect(self.windowChange)
        self.btn_ext_0.clicked.connect(self.close)
        self.btn_ext_1.clicked.connect(self.close)
        self.btn_ext_2.clicked.connect(self.close)
        self.btn_ext_3.clicked.connect(self.close)
        self.btn_ext_4.clicked.connect(self.close)
        self.customise_status_bar(self.__system__)  # important! call this method first!!!
        if self.__system__ == 'Windows':
            from .window_effect import WindowEffect
            self.windowEffect = WindowEffect()
            self._status_bar_pos = [QtCore.QPoint(x, y) for x in range(int(self.width()))
                                    for y in range(int(self.size2 * 2))]
            self.windowEffect.addWindowAnimation(int(self.winId()))
            self.windowEffect.addShadowEffect(int(self.winId()))
        else:
            # close all unwanted buttons
            self.btn_min_0.close(), self.btn_max_0.close(), self.btn_ext_0.close()
            self.btn_min_1.close(), self.btn_max_1.close(), self.btn_ext_1.close()
            self.btn_min_2.close(), self.btn_max_2.close(), self.btn_ext_2.close()
            self.btn_min_3.close(), self.btn_max_3.close(), self.btn_ext_3.close()
            self.btn_min_4.close(), self.btn_max_4.close(), self.btn_ext_4.close()
        self.tab0.label_v.setText(f'version {self.__version__}')
        set_language(self)

    # -------well, why do the following ugly codes exist?-------
    # -------they are used to re-enable, correctly, the window animations under Windows platform-------
    def mousePressEvent(self, event) -> None:
        if self.__system__ == 'Windows':
            if event.pos() in self._status_bar_pos:
                self.windowEffect.move_window(int(self.winId()))
        else:
            QTabWidget.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event) -> None:
        if self.__system__ == 'Windows':
            if event.button() == QtCore.Qt.LeftButton and event.pos() in self._status_bar_pos:
                self.windowChange()
        else:
            QTabWidget.mouseDoubleClickEvent(self, event)

    def nativeEvent(self, event_type, message) -> any:
        if self.__system__ == 'Windows':
            import win32api
            import win32con
            import win32gui
            from ctypes import cast, POINTER
            from ctypes.wintypes import MSG
            from .window_effect import NCCalcSizePARAMS, MINMAXINFO
            msg = MSG.from_address(message.__int__())

            def __isWindowMaximized(h_wnd) -> bool:
                """ whether is maximised """
                window_placement = win32gui.GetWindowPlacement(h_wnd)
                if not window_placement:
                    return False
                return window_placement[1] == win32con.SW_MAXIMIZE

            def __monitorNCCALCSIZE(_self, _msg: MSG) -> any:
                _monitor = win32api.MonitorFromWindow(_msg.hWnd)
                if _monitor is None and not self.monitor_info:
                    return _monitor
                elif _monitor is not None:
                    _self.monitor_info = win32api.GetMonitorInfo(_monitor)
                # resize window
                params = cast(_msg.lParam, POINTER(NCCalcSizePARAMS)).contents
                params.rgrc[0].left = _self.monitor_info['Work'][0]
                params.rgrc[0].top = _self.monitor_info['Work'][1]
                params.rgrc[0].right = _self.monitor_info['Work'][2]
                params.rgrc[0].bottom = _self.monitor_info['Work'][3]

            if msg.message == win32con.WM_NCHITTEST:
                x_pos = (win32api.LOWORD(msg.lParam)-self.frameGeometry().x()) % 65536
                y_pos = win32api.HIWORD(msg.lParam)-self.frameGeometry().y()
                w, h = self.width(), self.height()
                lx = x_pos < self.BORDER_WIDTH
                rx = x_pos + 9 > w - self.BORDER_WIDTH
                ty = y_pos < self.BORDER_WIDTH
                by = y_pos > h - self.BORDER_WIDTH
                if lx and ty:
                    return True, win32con.HTTOPLEFT
                elif rx and by:
                    return True, win32con.HTBOTTOMRIGHT
                elif rx and ty:
                    return True, win32con.HTTOPRIGHT
                elif lx and by:
                    return True, win32con.HTBOTTOMLEFT
                elif ty:
                    return True, win32con.HTTOP
                elif by:
                    return True, win32con.HTBOTTOM
                elif lx:
                    return True, win32con.HTLEFT
                elif rx:
                    return True, win32con.HTRIGHT
            elif msg.message == win32con.WM_NCCALCSIZE:
                if __isWindowMaximized(msg.hWnd):
                    __monitorNCCALCSIZE(self, msg)
                return True, 0
            elif msg.message == win32con.WM_GETMINMAXINFO:
                if __isWindowMaximized(msg.hWnd):
                    window_rect = win32gui.GetWindowRect(msg.hWnd)
                    if not window_rect:
                        return False, 0
                    # obtain monitor api
                    monitor = win32api.MonitorFromRect(window_rect)
                    if not monitor:
                        return False, 0
                    # obtain monitor information
                    monitor_info = win32api.GetMonitorInfo(monitor)
                    monitor_rect = monitor_info['Monitor']
                    work_area = monitor_info['Work']
                    # transform lParam into MINMAXINFO pointer
                    info = cast(msg.lParam, POINTER(MINMAXINFO)).contents
                    # resize window
                    info.ptMaxSize.x = work_area[2] - work_area[0]
                    info.ptMaxSize.y = work_area[3] - work_area[1]
                    info.ptMaxTrackSize.x = info.ptMaxSize.x
                    info.ptMaxTrackSize.y = info.ptMaxSize.y
                    info.ptMaxPosition.x = abs(window_rect[0] - monitor_rect[0])
                    info.ptMaxPosition.y = abs(window_rect[1] - monitor_rect[1])
                    return True, 1
        return QTabWidget.nativeEvent(self, event_type, message)
    # -------here ends the ugly code-------

    def closeEvent(self, event) -> None:
        """
        close all child windows and write settings to settings.json
        """
        _settings = {
            "start dir": self.s_dir,
            "save dir": self.o_dir,
            "dir store": self.dir_store_state,
            "font dir": self.font_dir,
            "language": self.language
        }
        with open(
                'settings/settings.json',
                mode='w',
                encoding='utf-8',
        ) as f:
            json.dump(
                _settings,
                f,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        sys.exit(0)

    def resizeEvent(self, event) -> None:
        self.widget3.resize(self.width() * 0.9, self.height() * 0.9)
        self.widget4.resize(self.width() * 0.9, self.height() * 0.9)
        QTabWidget.resizeEvent(self, event)

    def enable_preview(self) -> None:
        if self.tab3.check1.isChecked():
            self.tab3.text.textChanged.connect(self.preview)
            self.preview()
        else:
            self.tab3.text.textChanged.disconnect(self.preview)

    def enable_perm_set(self) -> None:
        if self.tab3.check2.isChecked():
            self.perm_int = 2820
            self.tab3.button6.clicked.connect(self._perm_set)
            self.tab3.button6.setStyleSheet(BUTTON_STYLE.format('more.svg', 'more_h.svg', 'more_p.svg'))
        else:
            self.tab3.button6.setStyleSheet(BUTTON_STYLE.format('more_d.svg', 'more_d.svg', 'more_d.svg'))
            self.tab3.button6.clicked.disconnect()
            self.perm_int = 4028

    @staticmethod
    def _view(index=None,
              widget=None,
              f_name=None) -> None:
        if f_name is not None:
            sp.Popen('explorer ' + f_name)
        else:
            sp.Popen('explorer '+widget.book_list[index].name)

    def save1(self) -> None:
        if len(self.tab1.book_list) != 0:
            doc0 = copy(self.tab1.book_list[0])
            for item in self.tab1.book_list[1:]:
                doc0.insert_pdf(item)
            set_metadata0(doc=doc0, author=self.Author)
            file_name, ok = save(self, '.pdf')
            if ok:
                try:
                    doc0.save(file_name, garbage=1)
                    self._view(f_name=file_name)
                except RuntimeError:
                    _warning(self)
                except ValueError:
                    _warning(self)
            doc0.close()
            del doc0

    def save2(self) -> None:
        if len(self.tab2.book_list) != 0:
            doc0 = copy(self.tab2.book)
            doc0.select(self.tab2.book_list)
            file_name, ok = save(self, '.pdf')
            set_metadata0(doc=doc0, author=self.Author)
            if ok:
                try:
                    doc0.save(file_name, garbage=1)
                    self._view(f_name=file_name)
                except RuntimeError:
                    _warning(self)
                except ValueError:
                    _warning(self)
            doc0.close()
            del doc0

    def save3(self) -> None:
        u_password = self.tab3.line1.text()
        o_password = self.tab3.line2.text()
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text())/100
        if len(self.tab3.book_list) != 0:
            file_name, ok = save(self, '.pdf')
            if ok:
                doc = copy(self.tab3.book_list[0])
                doc = add_watermark(
                    doc=doc,
                    text=watermark,
                    rotate=rotation,
                    colour=(self.colour_r,
                            self.colour_g,
                            self.colour_b),
                    font_size=font_size,
                    opacity=opacity,
                    font_file=self.font_dir,
                )
                try:
                    doc.save(
                        file_name,
                        garbage=1,
                        permissions=self.perm_int,
                        encryption=fitz.PDF_ENCRYPT_AES_256,
                        user_pw=u_password,
                        owner_pw=o_password,
                    )
                    if self.tab3.check.isChecked():
                        self._view(f_name=file_name)
                except RuntimeError:
                    _warning(self)
                except ValueError:
                    _warning(self)
                doc.close()
            del doc

    def save4(self) -> None:
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
            doc.set_metadata(metadata)
            if doc.can_save_incrementally():
                doc.saveIncr()
                del doc
            else:
                file_name, ok = save(self, '.pdf')
                if ok:
                    try:
                        doc.save(file_name, garbage=1)
                    except RuntimeError:
                        _warning(self)
                    except ValueError:
                        _warning(self)
                del doc

    def _set(self) -> None:
        self.SettingCD = Setting(
            {
                "start dir": self.s_dir,
                "save dir": self.o_dir,
                "language": self.language,
                "dir store": self.dir_store_state
            },
        )
        self.SettingCD.show()
        self.SettingCD.signal.connect(self.get_data)

    def get_perm_para(self,
                      par) -> None:
        self.perm_int = par

    def add1(self) -> None:
        f_name, _ = add(
            self,
            'PDF files (*.pdf);;'
            'images (*.png *.jpg *.jpeg *.bmp *.tiff *.svg);;'
            'ebooks (*.epub *.xps *.fb2 *.cbz)',
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
        else:
            pass

    def add2(self) -> None:
        if len(self.tab2.book_list) == 0:
            f_name, _ = add(self, '(*.pdf);;ebooks (*.epub *.xps *.fb2 *.cbz)')
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
            else:
                pass

    def add3(self) -> None:
        if len(self.tab3.book_list) == 0:
            f_name, _ = add(self, '(*.pdf)')
            if _:
                doc, state = open_pdf(f_name, self)
                if state:
                    self.tab3.book_list.append(doc)
                    reset_table(1, self.tab3)
                    set_icon(widget=self.tab3)
                else:
                    pass
                del doc, state
            else:
                pass

    def add4(self) -> None:
        f_name, _ = add(self, '(*.pdf)')
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
                set_icon(widget=self.tab4, _scaled=0.9, _scaled_=1)
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
        else:
            pass

    def get_data(self,
                 par1,
                 par2,
                 par3,
                 par5) -> None:
        self.s_dir = par1
        self.o_dir = par2
        self.dir_store_state = par3
        self.language = par5
        i = self.currentIndex()
        set_language(self)
        self.setCurrentIndex(i)

    def get_font_dir(self,
                     par) -> None:
        self.font_dir = par
        if self.tab3.check1.isChecked():
            self.preview()

    def get_colour(self) -> None:
        _colour = QColorDialog.getColor(
            initial=QColor(
                int(255*self.colour_r),
                int(255*self.colour_g),
                int(255*self.colour_b),
                int(255*float(self.tab3.line4.text())/100)),
            options=QColorDialog.ColorDialogOption(
                QColorDialog.ShowAlphaChannel,
            ),
            title='Select Colour',
        )
        if _colour.isValid():
            self.colour_r = _colour.getRgbF()[0]
            self.colour_g = _colour.getRgbF()[1]
            self.colour_b = _colour.getRgbF()[2]
            self.tab3.line4.setText('%.f' % (100*_colour.getRgbF()[3]))
            if self.tab3.check1.isChecked():
                self.preview()
        del _colour

    def get_font(self) -> None:
        font_paths = QtCore.QStandardPaths.standardLocations(
            QtCore.QStandardPaths.FontsLocation,
        )
        name_dict, file_dict = find_font(font_paths)
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
        rotation = int(self.tab3.line5.text())
        font_size = int(self.tab3.line3.text())
        watermark = self.tab3.text.toPlainText()
        opacity = int(self.tab3.line4.text())/100
        if len(self.tab3.book_list) != 0:
            doc = copy(self.tab3.book_list[0])
            doc = add_watermark(
                doc=doc,
                text=watermark,
                rotate=rotation,
                colour=(self.colour_r,
                        self.colour_g,
                        self.colour_b),
                font_size=font_size,
                opacity=opacity,
                font_file=self.font_dir,
                select=0,
            )
            self.tab3.table.clearContents()
            set_icon(widget=self.tab3, doc=doc)
            doc.close()
            del doc

    @staticmethod
    def showIndex(par, widget):
        index = par[0] * widget.w_col + par[1]  # get position
        if len(widget.book_list) != 0:
            widget.label0.setText(f'page {index+1}')


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
        super(Setting, self).__init__()
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
            self.button1.setStyleSheet(BUTTON_STYLE.format('folder_d.svg', 'folder_d.svg', 'folder_d.svg'))
            self.button2.setStyleSheet(BUTTON_STYLE.format('folder_d.svg', 'folder_d.svg', 'folder_d.svg'))
            try:
                self.button1.clicked.disconnect()
                self.button2.clicked.disconnect()
            except TypeError:
                pass
            self.line1.setReadOnly(True)
            self.line2.setReadOnly(True)
        else:
            self.button1.setStyleSheet(BUTTON_STYLE.format('folder.svg', 'folder_h.svg', 'folder_p.svg'))
            self.button2.setStyleSheet(BUTTON_STYLE.format('folder.svg', 'folder_h.svg', 'folder_p.svg'))
            self.button1.clicked.connect(lambda: choose(self.line1, self.s_dir))
            self.button2.clicked.connect(lambda: choose(self.line2, self.o_dir))
            self.line1.setReadOnly(False)
            self.line2.setReadOnly(False)

    def closeEvent(self, event) -> None:
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

    def __init__(self):
        super(PermMenu, self).__init__()

    def set_language(self, language: str) -> None:
        lag_p(self, language)

    def closeEvent(self, event) -> None:
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
    signal = QtCore.pyqtSignal(str)

    def __init__(self,
                 font_dir: str,
                 name_dict: dict,
                 file_dict: dict):
        super(FontDialog, self).__init__()
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
        doc = fitz.Document()
        fitz.utils.new_page(doc, -1, 380, 220)
        r1 = fitz.Rect(10, 10, 370, 210)
        page = doc.load_page(0)
        shape = fitz.utils.Shape(page)
        shape.draw_rect(r1)
        shape.finish()
        shape.insertTextbox(
            r1,
            'Hello\nこんにちは\n你好\n3.14159',
            color=(0.24, 0.24, 0.24),
            align=1,
            fontsize=25,
            fontfile=self.name_dict[self.combobox.currentText()],
            fontname='ext_0',
        )
        shape.commit()
        cover = render_pdf_page(page)
        self.label.setPixmap(
            QPixmap(cover).scaled(
                380,
                220,
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation,
            ),
        )
        doc.close()
        del cover, shape, page, r1, doc

    def closeEvent(self, event) -> None:
        self.signal.emit(self.name_dict[self.combobox.currentText()])
        self.close()
        del self


def __main__(system: str,
             version: str,
             debug: bool = True) -> None:
    """
    main function

    :param debug: whether display mupdf errors or not
    :return: None
    """
    fitz.TOOLS.mupdf_display_errors(debug)
    arg = sys.argv
    app = QApplication(arg)
    main = Main(system, version)
    main.show()
    sys.exit(app.exec_())
