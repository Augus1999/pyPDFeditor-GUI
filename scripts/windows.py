# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
application window forms
"""
from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QColor, QFont, QPixmap, QTransform
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QWidget, QGridLayout, QTabWidget, QLabel, QTextEdit, QScrollArea,
                             QComboBox, QLineEdit, QPushButton, QTableWidget, QApplication)
from .styleSheets import *  # change here if thee want to change theme!
from .functions import shadow


class SwitchBtn(QWidget):
    """
    switch button
    """
    stateChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checked = False
        self.bgColorOff = QColor("#e2e2dd")
        self.bgColorOn = QColor("#6272a4")
        self.sliderColorOff = QColor("#8d90a4")
        self.sliderColorOn = QColor("#f8f8f2")
        self.textColorOff = QColor("#8d90a4")
        self.textColorOn = QColor("#f8f8f2")
        self.textOff = "OFF"
        self.textOn = "ON"
        self.space = 6
        self.rectRadius = 5
        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.setFont(QFont("calibri", 11))

    def setStyleSheet(self, style_sheet: str) -> None:
        """
        define set-style-sheet behaviour
        """
        style_sheet = style_sheet.replace(' ', '').replace('\n', '').replace('\t', '')
        li = style_sheet.split('}')
        for i in li:
            if 'SwitchBtn:on' in i:
                lines = i.split('{')
                line1 = lines[1]
                styles = line1.split(';')
                for style in styles:
                    if 'background-color:' in style:
                        self.bgColorOn = QColor(style[17:])
                    if 'color:' in style and 'background-color:' not in style:
                        self.sliderColorOn = QColor(style[6:])
                        self.textColorOn = QColor(style[6:])
            if 'SwitchBtn:off' in i:
                lines = i.split('{')
                line1 = lines[1]
                styles = line1.split(';')
                for style in styles:
                    if 'background-color:' in style:
                        self.bgColorOff = QColor(style[17:])
                    if 'color:' in style and 'background-color:' not in style:
                        self.sliderColorOff = QColor(style[6:])
                        self.textColorOff = QColor(style[6:])

    def update_value(self) -> None:
        """
        update positions values
        """
        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        self.update()

    def mousePressEvent(self, event) -> None:
        """
        mousePressEvent
        """
        self.checked = not self.checked
        self.stateChanged.emit(self.checked)
        self.step = self.width() / 50
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def setChecked(self, on: bool) -> None:
        """
        set-checked
        """
        self.step = self.width() / 50
        if on:
            self.checked = True
            self.endX = self.width() - self.height()
        else:
            self.checked = False
            self.endX = 0
        self.timer.start(5)

    def isChecked(self) -> bool:
        """
        is-checked
        """
        return self.checked

    def paintEvent(self, event) -> None:
        """
        paintEvent
        """
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_bg(painter)
        self.draw_text(painter)
        self.draw_slider(painter)
        painter.end()

    def draw_text(self, painter) -> None:
        """
        draw text
        """
        painter.save()
        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(
                0,
                0,
                int(self.width() / 2 + self.space * 2),
                self.height(),
                QtCore.Qt.AlignCenter,
                self.textOn,
            )
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(
                int(self.width() / 2),
                0,
                int(self.width() / 2 - self.space),
                self.height(),
                QtCore.Qt.AlignCenter,
                self.textOff,
            )
        painter.restore()

    def draw_bg(self, painter) -> None:
        """
        draw background
        """
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)
        rect = QtCore.QRect(0, 0, self.width(), self.height())
        radius = rect.height() / 2
        circle_width = rect.height()
        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(
            QtCore.QRectF(
                rect.left(),
                rect.top(),
                circle_width,
                circle_width,
            ),
            90,
            180,
        )
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(
            QtCore.QRectF(
                rect.width() - rect.height(),
                rect.top(),
                circle_width,
                circle_width,
            ),
            270,
            180,
        )
        path.lineTo(radius, rect.top())
        painter.drawPath(path)
        painter.restore()

    def draw_slider(self, painter) -> None:
        """
        draw slider
        """
        painter.save()
        painter.setPen(QtCore.Qt.NoPen)
        if self.checked:
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setBrush(self.sliderColorOff)
        rect = QtCore.QRect(0, 0, self.width(), self.height())
        slider_width = rect.height() - self.space * 2
        slider_rect = QtCore.QRect(
            int(self.startX + self.space),
            self.space,
            slider_width,
            slider_width,
        )
        painter.drawEllipse(slider_rect)
        painter.restore()


class TableWidget(QTableWidget):
    """
    a wrapper to QTableWidget
    """
    Index = QtCore.pyqtSignal(tuple)

    def mousePressEvent(self, event) -> None:
        """
        re-write mousePressEvent
        """
        QTableWidget.mousePressEvent(self, event)
        if event.button() == QtCore.Qt.LeftButton:
            row_num = col_num = int()
            for i in self.selectionModel().selection().indexes():
                row_num = i.row()
                col_num = i.column()
            self.Index.emit((row_num, col_num))


class MainR(QTabWidget):
    """
    main window
    all window functions that define the appearance and behaviours are written here
    """
    def __init__(self, system: str, version: str, system_style: bool):
        super().__init__()
        self.__system__ = system
        self.__version__ = version
        self.system_style = system_style
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.88  # 950
        width = height*1.36  # 1290
        self.size1 = height * 0.04
        self.size2 = height * 0.03
        self.resize(width, height)
        self.setMinimumSize(0.47 * width, 0.45 * height)
        self.setWindowTitle('PDF Editor')
        self.setWindowIcon(QIcon('ico\\pdf icon.svg'))
        self.setTabShape(QTabWidget.Rounded)
        self.setTabPosition(QTabWidget.West)
        self.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.setStyleSheet(TAB_STYLE)
        self.tab0 = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.widget3 = QWidget()
        self.widget4 = QWidget()
        self.widget3.setStyleSheet(BGC_STYLE % 'transparent')
        self.widget4.setStyleSheet(BGC_STYLE % 'transparent')
        self.tab0_init()
        self.tab1_init()
        self.tab2_init()
        self.tab3_init()
        self.tab4_init()
        matrix = QTransform()
        matrix.rotate(90)
        self.addTab(
            self.tab0,
            QIcon(QPixmap('ico\\home.svg').transformed(matrix, QtCore.Qt.SmoothTransformation)),
            ''
        )
        self.addTab(
            self.tab1,
            QIcon(QPixmap('ico\\merge.svg').transformed(matrix, QtCore.Qt.SmoothTransformation)),
            '',
        )
        self.addTab(
            self.tab2,
            QIcon(QPixmap('ico\\edit.svg').transformed(matrix, QtCore.Qt.SmoothTransformation)),
            '',
        )
        self.addTab(
            self.tab3,
            QIcon(QPixmap('ico\\lock.svg').transformed(matrix, QtCore.Qt.SmoothTransformation)),
            '',
        )
        self.addTab(
            self.tab4,
            QIcon(QPixmap('ico\\metadata.svg').transformed(matrix, QtCore.Qt.SmoothTransformation)),
            '',
        )
        if self.__system__ == 'Windows':
            self.monitor_info = None
            self.btn_min_0 = QPushButton(self.tab0)
            self.btn_max_0 = QPushButton(self.tab0)
            self.btn_ext_0 = QPushButton(self.tab0)
            self.btn_min_1 = QPushButton(self.tab1)
            self.btn_max_1 = QPushButton(self.tab1)
            self.btn_ext_1 = QPushButton(self.tab1)
            self.btn_min_2 = QPushButton(self.tab2)
            self.btn_max_2 = QPushButton(self.tab2)
            self.btn_ext_2 = QPushButton(self.tab2)
            self.btn_min_3 = QPushButton(self.tab3)
            self.btn_max_3 = QPushButton(self.tab3)
            self.btn_ext_3 = QPushButton(self.tab3)
            self.btn_min_4 = QPushButton(self.tab4)
            self.btn_max_4 = QPushButton(self.tab4)
            self.btn_ext_4 = QPushButton(self.tab4)
            self.btn_min_0.setFixedSize(self.size2 * 2, self.size2)
            self.btn_max_0.setFixedSize(self.size2 * 2, self.size2)
            self.btn_ext_0.setFixedSize(self.size2 * 2, self.size2)
            self.btn_min_1.setFixedSize(self.size2 * 2, self.size2)
            self.btn_max_1.setFixedSize(self.size2 * 2, self.size2)
            self.btn_ext_1.setFixedSize(self.size2 * 2, self.size2)
            self.btn_min_2.setFixedSize(self.size2 * 2, self.size2)
            self.btn_max_2.setFixedSize(self.size2 * 2, self.size2)
            self.btn_ext_2.setFixedSize(self.size2 * 2, self.size2)
            self.btn_min_3.setFixedSize(self.size2 * 2, self.size2)
            self.btn_max_3.setFixedSize(self.size2 * 2, self.size2)
            self.btn_ext_3.setFixedSize(self.size2 * 2, self.size2)
            self.btn_min_4.setFixedSize(self.size2 * 2, self.size2)
            self.btn_max_4.setFixedSize(self.size2 * 2, self.size2)
            self.btn_ext_4.setFixedSize(self.size2 * 2, self.size2)
            self.btn_min_0.setStyleSheet(BUTTON_STYLE0.format('minimize.svg'))
            self.btn_max_0.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
            self.btn_ext_0.setStyleSheet(BUTTON_STYLE1.format('dismiss.svg', 'dismiss_h.svg'))
            self.btn_min_1.setStyleSheet(BUTTON_STYLE0.format('minimize.svg'))
            self.btn_max_1.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
            self.btn_ext_1.setStyleSheet(BUTTON_STYLE1.format('dismiss.svg', 'dismiss_h.svg'))
            self.btn_min_2.setStyleSheet(BUTTON_STYLE0.format('minimize.svg'))
            self.btn_max_2.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
            self.btn_ext_2.setStyleSheet(BUTTON_STYLE1.format('dismiss.svg', 'dismiss_h.svg'))
            self.btn_min_3.setStyleSheet(BUTTON_STYLE0.format('minimize.svg'))
            self.btn_max_3.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
            self.btn_ext_3.setStyleSheet(BUTTON_STYLE1.format('dismiss.svg', 'dismiss_h.svg'))
            self.btn_min_4.setStyleSheet(BUTTON_STYLE0.format('minimize.svg'))
            self.btn_max_4.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
            self.btn_ext_4.setStyleSheet(BUTTON_STYLE1.format('dismiss.svg', 'dismiss_h.svg'))
            self.btn_max_0.setObjectName('max0')
            self.btn_max_1.setObjectName('max1')
            self.btn_max_2.setObjectName('max2')
            self.btn_max_3.setObjectName('max3')
            self.btn_max_4.setObjectName('max4')
            self.tab0.grid.addWidget(self.btn_min_0, 0, 18)
            self.tab0.grid.addWidget(self.btn_max_0, 0, 19)
            self.tab0.grid.addWidget(self.btn_ext_0, 0, 20)
            self.tab1.grid.addWidget(self.btn_min_1, 0, 18)
            self.tab1.grid.addWidget(self.btn_max_1, 0, 19)
            self.tab1.grid.addWidget(self.btn_ext_1, 0, 20)
            self.tab1.grid.addWidget(self.tab1.button3, 0, 17)
            self.tab2.grid.addWidget(self.btn_min_2, 0, 18)
            self.tab2.grid.addWidget(self.btn_max_2, 0, 19)
            self.tab2.grid.addWidget(self.btn_ext_2, 0, 20)
            self.tab2.grid.addWidget(self.tab2.button3, 0, 17)
            self.tab3.grid.addWidget(self.btn_min_3, 0, 18)
            self.tab3.grid.addWidget(self.btn_max_3, 0, 19)
            self.tab3.grid.addWidget(self.btn_ext_3, 0, 20)
            self.tab3.grid.addWidget(self.tab3.button3, 0, 17)
            self.tab4.grid.addWidget(self.btn_min_4, 0, 18)
            self.tab4.grid.addWidget(self.btn_max_4, 0, 19)
            self.tab4.grid.addWidget(self.btn_ext_4, 0, 20)
            self.tab4.grid.addWidget(self.tab4.button3, 0, 17)
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
            from .window_effect import WindowEffect
            self.windowEffect = WindowEffect()
            self._status_bar_pos = [QtCore.QPoint(x, y) for x in range(int(self.width()))
                                    for y in range(int(self.size2 * 2))]
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # important! call this method first!
            self.setAttribute(QtCore.Qt.WA_StyledBackground)
            self.windowEffect.addWindowAnimation(int(self.winId()))
            if self.system_style:
                self.windowEffect.addShadowEffect(int(self.winId()))
                self.tab0.setStyleSheet(BGC_STYLE % '#ffffff')
                self.tab1.setStyleSheet(BGC_STYLE % '#ffffff')
                self.tab2.setStyleSheet(BGC_STYLE % '#ffffff')
                self.tab3.setStyleSheet(BGC_STYLE % '#ffffff')
                self.tab4.setStyleSheet(BGC_STYLE % '#ffffff')
                return
        else:
            self.tab1.grid.addWidget(self.tab1.button3, 0, 20)
            self.tab2.grid.addWidget(self.tab2.button3, 0, 20)
            self.tab3.grid.addWidget(self.tab3.button3, 0, 20)
            self.tab4.grid.addWidget(self.tab4.button3, 0, 20)
        self.tab0.setStyleSheet(BGC_STYLE % LIGHT_COLOUR)
        self.tab1.setStyleSheet(BGC_STYLE % LIGHT_COLOUR)
        self.tab2.setStyleSheet(BGC_STYLE % LIGHT_COLOUR)
        self.tab3.setStyleSheet(BGC_STYLE % LIGHT_COLOUR)
        self.tab4.setStyleSheet(BGC_STYLE % LIGHT_COLOUR)
        return

    def close(self) -> None:
        """
        re-write close
        """
        QTabWidget.close(self)

    def paintEvent(self, event) -> None:
        """
        re-write paintEvent
        """
        super().paintEvent(event)
        if self.__system__ != "Windows" or not self.system_style:
            QTabWidget.paintEvent(self, event)
            return None
        painter = QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QColor(MAIN_COLOUR))
        painter.drawRect(QtCore.QRect(0, 0, self.width()-2, self.height()-2))
        painter.setBrush(QColor('#ffffff'))
        painter.drawRect(QtCore.QRect(0, self.height()-2, self.width(), 2))
        painter.drawRect(QtCore.QRect(self.width()-2, 0, 2, self.height()))

    # -------well, why do the following ugly codes exist?-------
    # -------they are used to re-enable the window animations under Windows platform-------
    def mousePressEvent(self, event) -> None:
        """
        re-write mousePressEvent
        """
        if self.__system__ == 'Windows':
            if event.pos() in self._status_bar_pos:
                self.windowEffect.move_window(int(self.winId()))
        else:
            QTabWidget.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event) -> None:
        """
        re-write mouseDoubleClickEvent
        """
        if self.__system__ == 'Windows':
            if event.button() == QtCore.Qt.LeftButton and event.pos() in self._status_bar_pos:
                self.windowChange()
        else:
            QTabWidget.mouseDoubleClickEvent(self, event)

    def nativeEvent(self, event_type, message) -> (bool, int):
        """
        re-write nativeEvent
        """
        if self.__system__ == 'Windows':
            import win32api
            import win32con
            import win32gui
            from ctypes import cast, POINTER
            from ctypes.wintypes import MSG
            from .window_effect import NCCalcSizePARAMS
            msg = MSG.from_address(message.__int__())
            i = self.currentIndex()

            def __monitorNCCALCSIZE(_self, _msg: MSG) -> None:
                _monitor = win32api.MonitorFromWindow(_msg.hWnd)
                if _monitor is None and not _self.monitor_info:
                    return None
                if _monitor is not None:
                    _self.monitor_info = win32api.GetMonitorInfo(_monitor)
                # resize window
                params = cast(_msg.lParam, POINTER(NCCalcSizePARAMS)).contents
                params.rgrc[0].left = _self.monitor_info['Work'][0]
                params.rgrc[0].top = _self.monitor_info['Work'][1]
                params.rgrc[0].right = _self.monitor_info['Work'][2]
                params.rgrc[0].bottom = _self.monitor_info['Work'][3]
                return None

            def __isWindowMaximized(_self, h_wnd: MSG.hWnd) -> bool:
                window_placement = win32gui.GetWindowPlacement(h_wnd)
                if not window_placement:
                    return False
                return window_placement[1] == win32con.SW_MAXIMIZE

            if msg.message == win32con.WM_NCHITTEST:
                x_pos = win32api.GetCursorPos()[0]-self.frameGeometry().x()
                y_pos = win32api.GetCursorPos()[1]-self.frameGeometry().y()
                max_btn_x_pos = x_pos - self.size2 * 2
                lx = x_pos < 5
                rx = x_pos > self.width() - 5
                ty = y_pos < 5
                by = y_pos > self.height() - 5
                btn = self.findChildren(QPushButton, f'max{i}')[0]
                x_l, x_r = btn.x(), btn.x() + btn.width()
                y_t, y_b = btn.y(), btn.y() + btn.height()
                if x_l < max_btn_x_pos < x_r and y_t < y_pos < y_b and self.system_style:
                    return True, win32con.HTMAXBUTTON
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
            if msg.message == win32con.WM_NCCALCSIZE:
                if __isWindowMaximized(self, msg.hWnd):
                    __monitorNCCALCSIZE(self, msg)
                    self.btn_max_0.setStyleSheet(BUTTON_STYLE0.format('slide_multiple.svg'))
                    self.btn_max_1.setStyleSheet(BUTTON_STYLE0.format('slide_multiple.svg'))
                    self.btn_max_2.setStyleSheet(BUTTON_STYLE0.format('slide_multiple.svg'))
                    self.btn_max_3.setStyleSheet(BUTTON_STYLE0.format('slide_multiple.svg'))
                    self.btn_max_4.setStyleSheet(BUTTON_STYLE0.format('slide_multiple.svg'))
                else:
                    self.btn_max_0.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
                    self.btn_max_1.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
                    self.btn_max_2.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
                    self.btn_max_3.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
                    self.btn_max_4.setStyleSheet(BUTTON_STYLE0.format('maximize.svg'))
                return True, 0
        return QTabWidget.nativeEvent(self, event_type, message)
    # -------here ends the ugly code-------

    def resizeEvent(self, event) -> None:
        """
        re-write resizeEvent
        """
        super().resizeEvent(event)
        self.widget3.resize(self.width() * 0.9, self.height() * 0.9)
        self.widget4.resize(self.width() * 0.9, self.height() * 0.9)
        if self.__system__ == 'Windows':
            self._status_bar_pos = [QtCore.QPoint(x, y) for x in range(int(self.width()))
                                    for y in range(int(self.size2 * 2))]

    def windowChange(self) -> None:
        """
        maximise or normalise the window
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def tab0_init(self) -> None:
        """
        initialise tab0
        """
        self.tab0.grid = QGridLayout(self.tab0)
        label = QLabel(self.tab0)
        label.setStyleSheet(f'image:url(./{WELCOME_PAGE});border-radius:15px')
        shadow(label, QColor(0, 0, 0, 90), 10)
        label_w = QLabel(self.tab0)
        label_w.setStyleSheet(LABEL_STYLE)
        label_w.setText(
            "<a href='https://github.com/Augus1999/pyPDFeditor-GUI' style='color:#a3b5b3'>"
            "<small>https://github.com/Augus1999/pyPDFeditor-GUI</small></a>",
        )
        label_w.setOpenExternalLinks(True)
        self.tab0.label_v = QLabel(self.tab0)
        self.tab0.label_v.setStyleSheet(LABEL_STYLE)
        self.tab0.label_v.setText(f'version {self.__version__}')
        self.tab0.grid.addWidget(label, 1, 0, 30, 21)
        self.tab0.grid.addWidget(self.tab0.label_v, 31, 0, 1, 5, QtCore.Qt.AlignBottom)
        self.tab0.grid.addWidget(label_w, 31, 17, 1, 4, QtCore.Qt.AlignBottom)

    def tab1_init(self) -> None:
        """
        initialise tab1
        """
        self.tab1.grid = QGridLayout(self.tab1)
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.button1 = QPushButton(self.tab1)
        self.tab1.button2 = QPushButton(self.tab1)
        self.tab1.button3 = QPushButton(self.tab1)
        self.tab1.button4 = QPushButton(self.tab1)
        self.tab1.button1.setStyleSheet(
            BUTTON_STYLE.format('Add.svg', 'Add_h.svg', 'Add_p.svg'),
        )
        self.tab1.button2.setStyleSheet(
            BUTTON_STYLE.format('down.svg', 'down_h.svg', 'down_p.svg'),
        )
        self.tab1.button3.setStyleSheet(
            BUTTON_STYLE.format('settings.svg', 'settings_h.svg', 'settings_p.svg'),
        )
        self.tab1.button4.setStyleSheet(
            BUTTON_STYLE.format('delete.svg', 'delete_h.svg', 'delete_p.svg'),
        )
        self.tab1.button1.setFixedSize(self.size2 * 2, self.size2)
        self.tab1.button2.setFixedSize(self.size2 * 2, self.size2)
        self.tab1.button3.setFixedSize(self.size2 * 2, self.size2)
        self.tab1.button4.setFixedSize(self.size2 * 2, self.size2)
        self.tab1.table.setShowGrid(False)
        self.tab1.table.verticalHeader().setVisible(False)
        self.tab1.table.horizontalHeader().setVisible(False)
        self.tab1.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab1.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab1.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab1.table.setStyleSheet(TABLE_STYLE1)
        self.tab1.table.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu,
        )
        self.tab1.grid.addWidget(self.tab1.button1, 0, 0)
        self.tab1.grid.addWidget(self.tab1.button2, 0, 1)
        self.tab1.grid.addWidget(self.tab1.button4, 0, 2)
        self.tab1.grid.addWidget(self.tab1.table, 1, 0, 10, 21)

    def tab2_init(self) -> None:
        """
        initialise tab2
        """
        self.tab2.grid = QGridLayout(self.tab2)
        self.tab2.table = QTableWidget(self.tab2)
        self.tab2.button1 = QPushButton(self.tab2)
        self.tab2.button2 = QPushButton(self.tab2)
        self.tab2.button3 = QPushButton(self.tab2)
        self.tab2.button4 = QPushButton(self.tab2)
        self.tab2.button1.setStyleSheet(
            BUTTON_STYLE.format('Add.svg', 'Add_h.svg', 'Add_p.svg'),
        )
        self.tab2.button2.setStyleSheet(
            BUTTON_STYLE.format('down.svg', 'down_h.svg', 'down_p.svg'),
        )
        self.tab2.button3.setStyleSheet(
            BUTTON_STYLE.format('settings.svg', 'settings_h.svg', 'settings_p.svg'),
        )
        self.tab2.button4.setStyleSheet(
            BUTTON_STYLE.format('delete.svg', 'delete_h.svg', 'delete_p.svg'),
        )
        self.tab2.button1.setFixedSize(self.size2 * 2, self.size2)
        self.tab2.button2.setFixedSize(self.size2 * 2, self.size2)
        self.tab2.button3.setFixedSize(self.size2 * 2, self.size2)
        self.tab2.button4.setFixedSize(self.size2 * 2, self.size2)
        self.tab2.table.setShowGrid(False)
        self.tab2.table.verticalHeader().setVisible(False)
        self.tab2.table.horizontalHeader().setVisible(False)
        self.tab2.table.setStyleSheet(TABLE_STYLE1)
        self.tab2.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab2.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab2.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab2.table.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu,
        )
        self.tab2.grid.addWidget(self.tab2.button1, 0, 0)
        self.tab2.grid.addWidget(self.tab2.button2, 0, 1)
        self.tab2.grid.addWidget(self.tab2.button4, 0, 2)
        self.tab2.grid.addWidget(self.tab2.table, 1, 0, 10, 21)

    def tab3_init(self) -> None:
        """
        initialise tab3
        """
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(SCROLL_AREA_STYlE)
        self.widget3.setMinimumSize(self.width()*0.8, self.height()*0.8)
        layout = QGridLayout(self.widget3)
        scroll_area.setWidget(self.widget3)
        self.tab3.grid = QGridLayout(self.tab3)
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab3.table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab3.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab3.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab3.table.setStyleSheet(TABLE_STYLE2)
        self.tab3.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tab3.button1 = QPushButton(self.tab3)
        self.tab3.button2 = QPushButton(self.tab3)
        self.tab3.button3 = QPushButton(self.tab3)
        self.tab3.button4 = QPushButton(self.tab3)
        self.tab3.button5 = QPushButton(self.tab3)
        self.tab3.button6 = QPushButton(self.tab3)
        self.tab3.button7 = QPushButton(self.tab3)
        self.tab3.button8 = QPushButton(self.tab3)
        self.tab3.button1.setStyleSheet(
            BUTTON_STYLE.format('Add.svg', 'Add_h.svg', 'Add_p.svg'),
        )
        self.tab3.button2.setStyleSheet(
            BUTTON_STYLE.format('down.svg', 'down_h.svg', 'down_p.svg'),
        )
        self.tab3.button3.setStyleSheet(
            BUTTON_STYLE.format('settings.svg', 'settings_h.svg', 'settings_p.svg'),
        )
        self.tab3.button4.setStyleSheet(
            BUTTON_STYLE.format('color.svg', 'color_h.svg', 'color_p.svg'),
        )
        self.tab3.button5.setStyleSheet(
            BUTTON_STYLE.format('view.svg', 'view_h.svg', 'view_p.svg'),
        )
        self.tab3.button6.setStyleSheet(
            BUTTON_STYLE.format('more_d.svg', 'more_d.svg', 'more_d.svg'),
        )
        self.tab3.button7.setStyleSheet(
            BUTTON_STYLE.format('font.svg', 'font_h.svg', 'font_p.svg'),
        )
        self.tab3.button8.setStyleSheet(
            BUTTON_STYLE.format('delete.svg', 'delete_h.svg', 'delete_p.svg'),
        )
        self.tab3.table.setFixedSize(self.size2 * 20, self.size2 * 27)
        self.tab3.button1.setFixedSize(self.size2 * 2, self.size2)
        self.tab3.button2.setFixedSize(self.size2 * 2, self.size2)
        self.tab3.button3.setFixedSize(self.size2 * 2, self.size2)
        self.tab3.button4.setFixedSize(self.size2, self.size2)
        self.tab3.button5.setFixedSize(self.size2, self.size2)
        self.tab3.button6.setFixedSize(self.size2, self.size2)
        self.tab3.button7.setFixedSize(self.size2, self.size2)
        self.tab3.button8.setFixedSize(self.size2 * 2, self.size2)
        self.tab3.text = QTextEdit(self.tab3)
        self.tab3.line1 = QLineEdit(self.tab3)
        self.tab3.line2 = QLineEdit(self.tab3)
        self.tab3.line3 = QLineEdit(self.tab3)
        self.tab3.line4 = QLineEdit(self.tab3)
        self.tab3.line5 = QLineEdit(self.tab3)
        self.tab3.label1 = QLabel(self.tab3)
        self.tab3.label2 = QLabel(self.tab3)
        self.tab3.label3 = QLabel(self.tab3)
        self.tab3.label4 = QLabel(self.tab3)
        self.tab3.label5 = QLabel(self.tab3)
        self.tab3.label6 = QLabel(self.tab3)
        self.tab3.label7 = QLabel(self.tab3)
        self.tab3.label8 = QLabel(self.tab3)
        self.tab3.label9 = QLabel(self.tab3)
        self.tab3.label10 = QLabel(self.tab3)
        self.tab3.label11 = QLabel(self.tab3)
        self.tab3.label12 = QLabel(self.tab3)
        self.tab3.text.setFixedWidth(self.size2 * 10)
        self.tab3.line1.setFixedSize(self.size2 * 10, self.size1)
        self.tab3.line2.setFixedSize(self.size2 * 10, self.size1)
        self.tab3.line3.setFixedSize(self.size1, self.size1)
        self.tab3.line4.setFixedSize(self.size1, self.size1)
        self.tab3.line5.setFixedSize(self.size1, self.size1)
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('40')
        self.tab3.line5.setText(' 0')
        self.tab3.text.setStyleSheet(TEXTEDIT_STYlE)
        self.tab3.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line3.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line4.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line5.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.label1.setStyleSheet(LABEL_STYLE)
        self.tab3.label2.setStyleSheet(LABEL_STYLE)
        self.tab3.label3.setStyleSheet(LABEL_STYLE)
        self.tab3.label4.setStyleSheet(LABEL_STYLE)
        self.tab3.label5.setStyleSheet(LABEL_STYLE)
        self.tab3.label6.setStyleSheet(LABEL_STYLE)
        self.tab3.label7.setStyleSheet(LABEL_STYLE)
        self.tab3.label8.setStyleSheet(LABEL_STYLE)
        self.tab3.label9.setStyleSheet(LABEL_STYLE)
        self.tab3.label10.setStyleSheet(LABEL_STYLE)
        self.tab3.label11.setStyleSheet(LABEL_STYLE)
        self.tab3.label12.setStyleSheet(LABEL_STYLE)
        self.tab3.label3.setFixedSize(self.size1, self.size1)
        self.tab3.label6.setFixedSize(self.size1, self.size1)
        self.tab3.label10.setFixedSize(self.size1, self.size1)
        self.tab3.label3.setText('pt')
        self.tab3.label6.setText('%')
        self.tab3.label8.setText('* '*20)
        self.tab3.label10.setText('°')
        self.tab3.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label6.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label7.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label8.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label9.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label10.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label11.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.label12.setAlignment(QtCore.Qt.AlignCenter)
        self.tab3.check = SwitchBtn(self.tab3)
        self.tab3.check1 = SwitchBtn(self.tab3)
        self.tab3.check2 = SwitchBtn(self.tab3)
        self.tab3.check.setFixedSize(self.size1 * 2.1, self.size2)
        self.tab3.check1.setFixedSize(self.size1 * 2.1, self.size2)
        self.tab3.check2.setFixedSize(self.size1 * 2.1, self.size2)
        self.tab3.check.setChecked(True)
        self.tab3.check1.setChecked(False)
        self.tab3.check2.setChecked(False)
        self.tab3.check.setStyleSheet(SWITCH_STYLE)
        self.tab3.check1.setStyleSheet(SWITCH_STYLE)
        self.tab3.check2.setStyleSheet(SWITCH_STYLE)
        self.tab3.grid.addWidget(self.tab3.button1, 0, 0)
        self.tab3.grid.addWidget(self.tab3.button2, 0, 1)
        self.tab3.grid.addWidget(self.tab3.button8, 0, 2)
        self.tab3.grid.addWidget(scroll_area, 1, 0, 20, 21)
        layout.addWidget(self.tab3.table, 0, 0, 14, 10, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label1, 0, 14, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.line1, 1, 14, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.line2, 2, 14, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label2, 3, 14, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.text, 4, 14, 2, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label4, 6, 14, 1, 2, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.label7, 7, 14, 1, 2, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.label9, 8, 14, 1, 2, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.line3, 6, 16, 1, 1, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.line4, 7, 16, 1, 1, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.line5, 8, 16, 1, 1, QtCore.Qt.AlignRight)
        layout.addWidget(self.tab3.label3, 6, 17, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.label6, 7, 17, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.label10, 8, 17, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.button7, 6, 18, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.button4, 7, 18, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.button5, 8, 18, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(self.tab3.label8, 9, 14, 1, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label12, 10, 14, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label11, 11, 14, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.label5, 12, 14, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.check2, 10, 16, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.check1, 11, 16, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.check, 12, 16, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab3.button6, 10, 18, 1, 1, QtCore.Qt.AlignLeft)

    def tab4_init(self) -> None:
        """
        initialise tab4
        """
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(SCROLL_AREA_STYlE)
        self.widget4.setMinimumSize(self.width() * 0.8, self.height() * 0.8)
        layout = QGridLayout(self.widget4)
        scroll_area.setWidget(self.widget4)
        self.tab4.grid = QGridLayout(self.tab4)
        self.tab4.button1 = QPushButton(self.tab4)
        self.tab4.button2 = QPushButton(self.tab4)
        self.tab4.button3 = QPushButton(self.tab4)
        self.tab4.button4 = QPushButton(self.tab4)
        self.tab4.button1.setStyleSheet(
            BUTTON_STYLE.format('Add.svg', 'Add_h.svg', 'Add_p.svg'),
        )
        self.tab4.button2.setStyleSheet(
            BUTTON_STYLE.format('down.svg', 'down_h.svg', 'down_p.svg'),
        )
        self.tab4.button3.setStyleSheet(
            BUTTON_STYLE.format('settings.svg', 'settings_h.svg', 'settings_p.svg'),
        )
        self.tab4.button4.setStyleSheet(
            BUTTON_STYLE.format('delete.svg', 'delete_h.svg', 'delete_p.svg'),
        )
        self.tab4.button1.setFixedSize(self.size2 * 2, self.size2)
        self.tab4.button2.setFixedSize(self.size2 * 2, self.size2)
        self.tab4.button3.setFixedSize(self.size2 * 2, self.size2)
        self.tab4.button4.setFixedSize(self.size2 * 2, self.size2)
        self.tab4.table = TableWidget(self.tab4)
        self.tab4.table.setShowGrid(False)
        self.tab4.table.verticalHeader().setVisible(False)
        self.tab4.table.horizontalHeader().setVisible(False)
        self.tab4.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab4.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab4.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab4.table.setStyleSheet(TABLE_STYLE2)
        self.tab4.text = QTextEdit(self.tab4)
        self.tab4.text.setStyleSheet(TEXTEDIT_STYlE)
        self.tab4.text.setLineWrapColumnOrWidth(2000)
        self.tab4.text.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.tab4.label0 = QLabel(self.tab4)
        self.tab4.label1 = QLabel(self.tab4)
        self.tab4.label2 = QLabel(self.tab4)
        self.tab4.label3 = QLabel(self.tab4)
        self.tab4.label4 = QLabel(self.tab4)
        self.tab4.label5 = QLabel(self.tab4)
        self.tab4.label0.setStyleSheet(LABEL_STYLE)
        self.tab4.label1.setStyleSheet(LABEL_STYLE)
        self.tab4.label2.setStyleSheet(LABEL_STYLE)
        self.tab4.label3.setStyleSheet(LABEL_STYLE)
        self.tab4.label4.setStyleSheet(LABEL_STYLE)
        self.tab4.label5.setStyleSheet(LABEL_STYLE)
        self.tab4.label1.setPixmap(
            QPixmap('ico\\book2.svg').scaled(
                self.height()*0.2,
                self.height()*0.2,
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation,
            ),
        )
        self.tab4.line1 = QLineEdit(self.tab4)
        self.tab4.line2 = QLineEdit(self.tab4)
        self.tab4.line3 = QLineEdit(self.tab4)
        self.tab4.line4 = QLineEdit(self.tab4)
        self.tab4.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line3.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line4.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line1.setFixedSize(self.size2 * 12, self.size1)
        self.tab4.line2.setFixedSize(self.size2 * 12, self.size1)
        self.tab4.line3.setFixedSize(self.size2 * 12, self.size1)
        self.tab4.line4.setFixedSize(self.size2 * 12, self.size1)
        self.tab4.text.setFixedSize(self.size2 * 12, self.height() * 0.47)
        self.tab4.line1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line4.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.grid.addWidget(self.tab4.button1, 0, 0)
        self.tab4.grid.addWidget(self.tab4.button2, 0, 1)
        self.tab4.grid.addWidget(self.tab4.button4, 0, 2)
        self.tab4.grid.addWidget(scroll_area, 1, 0, 20, 21)
        layout.addWidget(self.tab4.text, 4, 0, 8, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.table, 0, 7, 20, 7)
        layout.addWidget(self.tab4.label1, 1, 0, 3, 5, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.label2, 1, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.label3, 3, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.label4, 5, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.label5, 7, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.line1, 2, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.line2, 4, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.line3, 6, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.line4, 8, 14, 1, 7, QtCore.Qt.AlignCenter)
        layout.addWidget(self.tab4.label0, 19, 0, 1, 3, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)


class SettingR(QWidget):
    """
    setting window
    """
    def __init__(self):
        super().__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.26  # 280
        width = height*2.14  # 600
        fixed_h = width*2//30
        grid = QGridLayout(self)
        self.setFixedSize(width, height)
        self.setWindowTitle('Setting')
        self.setWindowIcon(
            QIcon('ico\\settings.svg'),
        )
        self.setStyleSheet('background-color:#ffffff')
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.check = SwitchBtn(self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.combobox = QComboBox(self)
        self.combobox.addItem('English')
        self.combobox.addItem('中文')
        self.combobox.addItem('日本語')
        self.label1.setStyleSheet(LABEL_STYLE)
        self.label2.setStyleSheet(LABEL_STYLE)
        self.label3.setStyleSheet(LABEL_STYLE)
        self.check.setStyleSheet(SWITCH_STYLE)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.label1.setAlignment(QtCore.Qt.AlignVCenter)
        self.label2.setAlignment(QtCore.Qt.AlignVCenter)
        self.label3.setAlignment(QtCore.Qt.AlignVCenter)
        self.check.setFixedSize(fixed_h * 2, fixed_h * 0.75)
        self.line1.setFixedSize(fixed_h * 10, fixed_h)
        self.line2.setFixedSize(fixed_h * 10, fixed_h)
        self.button1.setFixedSize(fixed_h * 0.7, fixed_h * 0.7)
        self.button2.setFixedSize(fixed_h * 0.7, fixed_h * 0.7)
        self.combobox.setFixedSize(fixed_h*17/4, fixed_h)
        grid.addWidget(self.label1, 0, 0, 1, 5, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label2, 1, 0, 1, 5, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label3, 2, 0, 1, 7, QtCore.Qt.AlignLeft)
        grid.addWidget(self.combobox, 3, 0)
        grid.addWidget(self.line1, 0, 5, 1, 10)
        grid.addWidget(self.line2, 1, 5, 1, 10)
        grid.addWidget(self.button1, 0, 14, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.button2, 1, 14, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.check, 2, 13, 1, 2, QtCore.Qt.AlignHCenter)
        self.setWindowOpacity(0.92)


class PermMenuR(QWidget):
    """
    permission setting menu window
    """
    def __init__(self):
        super().__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.37  # 400
        width = height*1.2  # 480
        x = height/5
        y = width/16
        grid = QGridLayout(self)
        self.setFixedSize(width, height)
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('ico\\lock.svg'))
        self.setStyleSheet('background-color:#ffffff')
        self.check1 = SwitchBtn(self)
        self.check2 = SwitchBtn(self)
        self.check3 = SwitchBtn(self)
        self.check4 = SwitchBtn(self)
        self.check5 = SwitchBtn(self)
        self.check6 = SwitchBtn(self)
        self.check7 = SwitchBtn(self)
        self.check8 = SwitchBtn(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)
        self.check1.setFixedSize(x, y)
        self.check2.setFixedSize(x, y)
        self.check3.setFixedSize(x, y)
        self.check4.setFixedSize(x, y)
        self.check5.setFixedSize(x, y)
        self.check6.setFixedSize(x, y)
        self.check7.setFixedSize(x, y)
        self.check8.setFixedSize(x, y)
        grid.addWidget(self.label1, 0, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label2, 1, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label3, 2, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label4, 3, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label5, 4, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label6, 5, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label7, 6, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label8, 7, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.check1, 0, 1)
        grid.addWidget(self.check2, 1, 1)
        grid.addWidget(self.check3, 2, 1)
        grid.addWidget(self.check4, 3, 1)
        grid.addWidget(self.check5, 4, 1)
        grid.addWidget(self.check6, 5, 1)
        grid.addWidget(self.check7, 6, 1)
        grid.addWidget(self.check8, 7, 1)
        self.label1.setStyleSheet(LABEL_STYLE)
        self.label2.setStyleSheet(LABEL_STYLE)
        self.label3.setStyleSheet(LABEL_STYLE)
        self.label4.setStyleSheet(LABEL_STYLE)
        self.label5.setStyleSheet(LABEL_STYLE)
        self.label6.setStyleSheet(LABEL_STYLE)
        self.label7.setStyleSheet(LABEL_STYLE)
        self.label8.setStyleSheet(LABEL_STYLE)
        self.check1.setStyleSheet(SWITCH_STYLE)
        self.check2.setStyleSheet(SWITCH_STYLE)
        self.check3.setStyleSheet(SWITCH_STYLE)
        self.check4.setStyleSheet(SWITCH_STYLE)
        self.check5.setStyleSheet(SWITCH_STYLE)
        self.check6.setStyleSheet(SWITCH_STYLE)
        self.check7.setStyleSheet(SWITCH_STYLE)
        self.check8.setStyleSheet(SWITCH_STYLE)
        self.check1.setChecked(True)
        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.check8.setChecked(True)
        self.setWindowOpacity(0.92)


class FontDialogR(QWidget):
    """
    font menu window
    """
    def __init__(self):
        super().__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.27
        width = height*1.37
        grid = QGridLayout(self)
        self.resize(width, height)
        self.setWindowTitle('Select Font')
        self.setWindowIcon(QIcon('ico\\font.svg'))
        self.combobox = QComboBox(self)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.combobox.setFixedHeight(height/7)
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        grid.addWidget(self.combobox, 0, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.label, 1, 0, QtCore.Qt.AlignCenter)
        self.setWindowOpacity(0.92)
