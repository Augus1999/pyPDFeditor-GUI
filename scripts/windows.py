# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QColor, QFont, QPixmap
from .styleSheets import *
from PyQt5 import (
    QtCore,
    QtWidgets,
)
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QLabel,
    QTextEdit,
    QComboBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QApplication,
)


class SwitchBtn(QWidget):
    stateChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.checked = False
        self.bgColorOff = QColor(255, 255, 255)
        self.bgColorOn = QColor("#b7cbc9")
        self.sliderColorOff = QColor(60, 60, 60)
        self.sliderColorOn = QColor(255, 255, 255)
        self.textColorOff = QColor(60, 60, 60)
        self.textColorOn = QColor(255, 255, 255)
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

    def update_value(self) -> None:
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
        self.checked = not self.checked
        self.stateChanged.emit(self.checked)
        self.step = self.width() / 50
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def setChecked(self, on: bool) -> None:
        self.step = self.width() / 50
        if on:
            self.checked = True
            self.endX = self.width() - self.height()
        else:
            self.checked = False
            self.endX = 0
        self.timer.start(5)

    def isChecked(self) -> bool:
        return self.checked

    def paintEvent(self, evt) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_bg(evt, painter)
        self.draw_text(evt, painter)
        self.draw_slider(evt, painter)
        painter.end()

    def draw_text(self, event, painter) -> None:
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

    def draw_bg(self, event, painter) -> None:
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

    def draw_slider(self, event, painter) -> None:
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


class MainR(QTabWidget):
    """
    main widow
    """
    def __init__(self):
        super(MainR, self).__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.88  # 950
        width = height*1.36  # 1290
        self.icon_size = height*0.04
        self.icon_size_2 = height*0.03
        self.setFixedSize(width, height)
        self.setWindowTitle('PDF Editor')
        self.setWindowIcon(
            QIcon('ico\\pdf icon.svg'),
        )
        self.setTabShape(QTabWidget.Rounded)
        self.setTabPosition(QTabWidget.North)
        self.setIconSize(
            QtCore.QSize(self.icon_size, self.icon_size),
        )
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab1_init()
        self.tab2_init()
        self.tab3_init()
        self.tab4_init()

    def tab1_init(self) -> None:
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.scroll_bar = QtWidgets.QScrollBar(self.tab1)
        self.tab1.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab1.button1 = QPushButton(self.tab1)
        self.tab1.button2 = QPushButton(self.tab1)
        self.tab1.button3 = QPushButton(self.tab1)
        self.tab1.button4 = QPushButton(self.tab1)
        self.tab1.button5 = QPushButton(self.tab1)
        self.tab1.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab1.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab1.button3.setIcon(QIcon('ico\\settings.svg'))
        self.tab1.button4.setIcon(QIcon('ico\\delete.svg'))
        self.tab1.button5.setIcon(QIcon('ico\\info.svg'))
        self.tab1.button1.setStyleSheet(BUTTON_STYLE1)
        self.tab1.button2.setStyleSheet(BUTTON_STYLE1)
        self.tab1.button3.setStyleSheet(BUTTON_STYLE6)
        self.tab1.button4.setStyleSheet(BUTTON_STYLE1)
        self.tab1.button5.setStyleSheet(BUTTON_STYLE6)
        self.tab1.button1.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab1.button2.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab1.button3.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab1.button4.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab1.button5.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab1.table.setGeometry(
            QtCore.QRect(0, int(self.height()*0.1), self.width(), int(self.height()*0.82)),
        )
        self.tab1.button1.setGeometry(
            QtCore.QRect(int(self.width()*0.008), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab1.button2.setGeometry(
            QtCore.QRect(int(self.width()*0.09), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab1.button3.setGeometry(
            QtCore.QRect(int(self.width()*0.18), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab1.button4.setGeometry(
            QtCore.QRect(int(self.width()*0.31), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab1.button5.setGeometry(
            QtCore.QRect(int(self.width()*0.94), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab1.button3.setToolTip('Settings')
        self.tab1.button5.setToolTip('about')
        self.tab1.table.setVerticalScrollBar(
            self.tab1.scroll_bar,
        )
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
        self.tab1.setStyleSheet(BGC_STYLE1)

    def tab2_init(self) -> None:
        self.tab2.table = QTableWidget(self.tab2)
        self.tab2.scroll_bar = QtWidgets.QScrollBar(self.tab2)
        self.tab2.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab2.button1 = QPushButton(self.tab2)
        self.tab2.button2 = QPushButton(self.tab2)
        self.tab2.button3 = QPushButton(self.tab2)
        self.tab2.button4 = QPushButton(self.tab2)
        self.tab2.button5 = QPushButton(self.tab2)
        self.tab2.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab2.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab2.button3.setIcon(QIcon('ico\\settings.svg'))
        self.tab2.button4.setIcon(QIcon('ico\\delete.svg'))
        self.tab2.button5.setIcon(QIcon('ico\\pane.svg'))
        self.tab2.button1.setStyleSheet(BUTTON_STYLE1)
        self.tab2.button2.setStyleSheet(BUTTON_STYLE1)
        self.tab2.button3.setStyleSheet(BUTTON_STYLE6)
        self.tab2.button4.setStyleSheet(BUTTON_STYLE1)
        self.tab2.button5.setStyleSheet(BUTTON_STYLE6)
        self.tab2.button1.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab2.button2.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab2.button3.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab2.button4.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab2.button5.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab2.table.setGeometry(
            QtCore.QRect(0, int(self.height()*0.1), self.width(), int(self.height()*0.82)),
        )
        self.tab2.button1.setGeometry(
            QtCore.QRect(int(self.width()*0.008), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab2.button2.setGeometry(
            QtCore.QRect(int(self.width()*0.09), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab2.button3.setGeometry(
            QtCore.QRect(int(self.width()*0.18), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab2.button4.setGeometry(
            QtCore.QRect(int(self.width()*0.31), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab2.button5.setGeometry(
            QtCore.QRect(int(self.width()*0.94), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab2.button3.setToolTip('Settings')
        self.tab2.button5.setToolTip('dual columns')
        self.tab2.table.setShowGrid(False)
        self.tab2.table.setVerticalScrollBar(self.tab2.scroll_bar)
        self.tab2.table.verticalHeader().setVisible(False)
        self.tab2.table.horizontalHeader().setVisible(False)
        self.tab2.table.setStyleSheet(TABLE_STYLE1)
        self.tab2.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab2.table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn,
        )
        self.tab2.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab2.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab2.table.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu,
        )
        self.tab2.setStyleSheet(BGC_STYLE1)

    def tab3_init(self) -> None:
        self.tab3.setStyleSheet(BGC_STYLE2)
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(
            QtCore.QRect(self.icon_size_2, int(self.height()*0.11), int(self.height()*0.6), int(self.height()*0.8)),
        )
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
        self.tab3.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab3.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab3.button3.setIcon(QIcon('ico\\settings.svg'))
        self.tab3.button4.setIcon(QIcon('ico\\color.svg'))
        self.tab3.button5.setIcon(QIcon('ico\\view.svg'))
        self.tab3.button6.setIcon(QIcon('ico\\row.svg'))
        self.tab3.button7.setIcon(QIcon('ico\\font.svg'))
        self.tab3.button1.setStyleSheet(BUTTON_STYLE2)
        self.tab3.button2.setStyleSheet(BUTTON_STYLE2)
        self.tab3.button3.setStyleSheet(BUTTON_STYLE6)
        self.tab3.button4.setStyleSheet(BUTTON_STYLE3)
        self.tab3.button5.setStyleSheet(BUTTON_STYLE3)
        self.tab3.button6.setStyleSheet(BUTTON_STYLE3)
        self.tab3.button7.setStyleSheet(BUTTON_STYLE3)
        self.tab3.scroll_bar = QtWidgets.QScrollBar(self.tab3)
        self.tab3.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab3.button1.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab3.button2.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab3.button3.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab3.button4.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab3.button5.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab3.button6.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab3.button7.setIconSize(QtCore.QSize(self.icon_size_2, self.icon_size_2))
        self.tab3.button3.setToolTip('Settings')
        self.tab3.button4.setToolTip('colours')
        self.tab3.button5.setToolTip('preview')
        self.tab3.button6.setToolTip('more')
        self.tab3.button7.setToolTip('font')
        self.tab3.button1.setGeometry(
            QtCore.QRect(int(self.width()*0.008), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab3.button2.setGeometry(
            QtCore.QRect(int(self.width()*0.09), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab3.button3.setGeometry(
            QtCore.QRect(int(self.width()*0.18), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab3.button4.setGeometry(
            QtCore.QRect(int(self.width()*0.81), int(self.width()*0.426), self.icon_size, self.icon_size),
        )
        self.tab3.button5.setGeometry(
            QtCore.QRect(int(self.width()*0.81), int(self.width()*0.465), self.icon_size, self.icon_size),
        )
        self.tab3.button6.setGeometry(
            QtCore.QRect(int(self.width()*0.81), int(self.width()*0.545), self.icon_size, self.icon_size),
        )
        self.tab3.button7.setGeometry(
            QtCore.QRect(int(self.width()*0.81), int(self.width()*0.388), self.icon_size, self.icon_size),
        )
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
        self.tab3.text.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.279), self.icon_size_2*10, self.icon_size*3),
        )
        self.tab3.line1.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.124), self.icon_size_2*10, self.icon_size),
        )
        self.tab3.line2.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.186), self.icon_size_2*10, self.icon_size),
        )
        self.tab3.line3.setGeometry(
            QtCore.QRect(int(self.width()*0.74), int(self.width()*0.388), self.icon_size, self.icon_size),
        )
        self.tab3.line4.setGeometry(
            QtCore.QRect(int(self.width()*0.74), int(self.width()*0.426), self.icon_size, self.icon_size),
        )
        self.tab3.line5.setGeometry(
            QtCore.QRect(int(self.width()*0.74), int(self.width()*0.465), self.icon_size, self.icon_size),
        )
        self.tab3.line1.setPlaceholderText('  user password here')
        self.tab3.line2.setPlaceholderText('  owner password here')
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('40')
        self.tab3.line5.setText(' 0')
        self.tab3.text.setStyleSheet(TEXTEDIT_STYlE.format('14'))
        self.tab3.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line3.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line4.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.line5.setStyleSheet(LINE_EDIT_STYLE)
        self.tab3.label1.setStyleSheet(LABEL_STYLE1)
        self.tab3.label2.setStyleSheet(LABEL_STYLE1)
        self.tab3.label3.setStyleSheet(LABEL_STYLE1)
        self.tab3.label4.setStyleSheet(LABEL_STYLE1)
        self.tab3.label5.setStyleSheet(LABEL_STYLE1)
        self.tab3.label6.setStyleSheet(LABEL_STYLE1)
        self.tab3.label7.setStyleSheet(LABEL_STYLE1)
        self.tab3.label8.setStyleSheet(LABEL_STYLE1)
        self.tab3.label9.setStyleSheet(LABEL_STYLE1)
        self.tab3.label10.setStyleSheet(LABEL_STYLE1)
        self.tab3.label11.setStyleSheet(LABEL_STYLE1)
        self.tab3.label12.setStyleSheet(LABEL_STYLE1)
        self.tab3.text.setVerticalScrollBar(self.tab3.scroll_bar)
        self.tab3.label1.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.078), self.icon_size_2*10, self.icon_size),
        )
        self.tab3.label2.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.233), self.icon_size_2*10, self.icon_size),
        )
        self.tab3.label3.setGeometry(
            QtCore.QRect(int(self.width()*0.77), int(self.width()*0.388), self.icon_size, self.icon_size),
        )
        self.tab3.label4.setGeometry(
            QtCore.QRect(int(self.width()*0.64), int(self.width()*0.388), self.icon_size*3, self.icon_size),
        )
        self.tab3.label5.setGeometry(
            QtCore.QRect(int(self.height()*0.77), int(self.width()*0.605), int(self.width()*0.17), self.icon_size),
        )
        self.tab3.label6.setGeometry(
            QtCore.QRect(int(self.width()*0.77), int(self.width()*0.426), self.icon_size, self.icon_size),
        )
        self.tab3.label7.setGeometry(
            QtCore.QRect(int(self.width()*0.66), int(self.width()*0.426), self.icon_size*2.5, self.icon_size),
        )
        self.tab3.label8.setGeometry(
            QtCore.QRect(int(self.width()*0.57), int(self.width()*0.496), self.icon_size_2*10, self.icon_size),
        )
        self.tab3.label9.setGeometry(
            QtCore.QRect(int(self.width()*0.66), int(self.width()*0.465), self.icon_size*2.5, self.icon_size),
        )
        self.tab3.label10.setGeometry(
            QtCore.QRect(int(self.width()*0.77), int(self.width()*0.465), self.icon_size, self.icon_size),
        )
        self.tab3.label11.setGeometry(
            QtCore.QRect(int(self.height()*0.77), int(self.width()*0.575), int(self.width()*0.17), self.icon_size),
        )
        self.tab3.label12.setGeometry(
            QtCore.QRect(int(self.height()*0.77), int(self.width()*0.545), int(self.width()*0.17), self.icon_size),
        )
        self.tab3.label1.setText('.'*9+'PASSWORD'+'.'*9)
        self.tab3.label2.setText('.'*8+'WATERMARK'+'.'*8)
        self.tab3.label3.setText('pt')
        self.tab3.label4.setText('Font Size:')
        self.tab3.label5.setText('Open after saving')
        self.tab3.label6.setText('%')
        self.tab3.label7.setText('Opacity:')
        self.tab3.label8.setText('.'*26)
        self.tab3.label9.setText('Rotation:')
        self.tab3.label10.setText('°')
        self.tab3.label11.setText('Preview Mode')
        self.tab3.label12.setText('Edit Restriction')
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
        self.tab3.check.setGeometry(
            QtCore.QRect(self.height(), int(self.width()*0.61), self.icon_size*2.1, self.icon_size_2),
        )
        self.tab3.check1.setGeometry(
            QtCore.QRect(self.height(), int(self.width()*0.58), self.icon_size*2.1, self.icon_size_2),
        )
        self.tab3.check2.setGeometry(
            QtCore.QRect(self.height(), int(self.width()*0.55), self.icon_size*2.1, self.icon_size_2),
        )
        self.tab3.check.setChecked(True)
        self.tab3.check1.setChecked(False)
        self.tab3.check2.setChecked(False)

    def tab4_init(self) -> None:
        self.tab4.setStyleSheet(BGC_STYLE2)
        self.tab4.button1 = QPushButton(self.tab4)
        self.tab4.button2 = QPushButton(self.tab4)
        self.tab4.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab4.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab4.button1.setStyleSheet(BUTTON_STYLE2)
        self.tab4.button2.setStyleSheet(BUTTON_STYLE2)
        self.tab4.button1.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab4.button2.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.tab4.button1.setGeometry(
            QtCore.QRect(int(self.width()*0.008), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab4.button2.setGeometry(
            QtCore.QRect(int(self.width()*0.09), self.icon_size/4, self.icon_size*2, self.icon_size*2),
        )
        self.tab4.table = QTableWidget(self.tab4)
        self.tab4.table.setShowGrid(False)
        self.tab4.table.verticalHeader().setVisible(True)
        self.tab4.table.horizontalHeader().setVisible(False)
        self.tab4.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab4.table.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff,
        )
        self.tab4.table.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn,
        )
        self.tab4.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers,
        )
        self.tab4.table.setGeometry(
            QtCore.QRect(self.width()//3, int(self.height()*0.1), self.width()//3, int(self.height()*0.82)),
        )
        self.tab4.table.setStyleSheet(TABLE_STYLE2)
        self.tab4.scroll_bar0 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar1 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar2 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar0.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab4.scroll_bar1.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab4.scroll_bar2.setStyleSheet(SCROLL_BAR_STYLE_H)
        self.tab4.table.setVerticalScrollBar(self.tab4.scroll_bar0)
        self.tab4.text = QTextEdit(self.tab4)
        self.tab4.text.setStyleSheet(TEXTEDIT_STYlE.format('12'))
        self.tab4.text.setVerticalScrollBar(self.tab4.scroll_bar1)
        self.tab4.text.setHorizontalScrollBar(self.tab4.scroll_bar2)
        self.tab4.text.setGeometry(
            QtCore.QRect(self.height()//25, int(self.width()*0.275), int(self.width()*0.27), int(self.height()*0.47)),
        )
        self.tab4.text.setLineWrapColumnOrWidth(2000)
        self.tab4.text.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.tab4.text.setPlaceholderText(
            '''
            Catalogue edit here
            e.g.
        
            *-->chapter 1-->1
            **-->section 1-->1
            **-->section 2-->5
            *-->chapter 2-->17
            '''
        )
        self.tab4.label1 = QLabel(self.tab4)
        self.tab4.label2 = QLabel(self.tab4)
        self.tab4.label3 = QLabel(self.tab4)
        self.tab4.label4 = QLabel(self.tab4)
        self.tab4.label5 = QLabel(self.tab4)
        self.tab4.label1.setStyleSheet(LABEL_STYLE2)
        self.tab4.label2.setStyleSheet(LABEL_STYLE2)
        self.tab4.label3.setStyleSheet(LABEL_STYLE2)
        self.tab4.label4.setStyleSheet(LABEL_STYLE2)
        self.tab4.label5.setStyleSheet(LABEL_STYLE2)
        self.tab4.label1.setPixmap(
            QPixmap('ico\\book2.svg').scaled(
                self.height()*0.2,
                self.height()*0.2,
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation,
            ),
        )
        self.tab4.label2.setText('.'*10+'Title'+'.'*10)
        self.tab4.label3.setText('.'*10+'Author'+'.'*10)
        self.tab4.label4.setText('.'*10+'Subject'+'.'*10)
        self.tab4.label5.setText('.'*10+'Keywords'+'.'*10)
        self.tab4.label1.setGeometry(
            QtCore.QRect(int(self.width()*0.06), int(self.width()*0.078), self.icon_size*6.25, self.icon_size*6.25),
        )
        self.tab4.label2.setGeometry(
            QtCore.QRect(int(self.width()*0.68), int(self.width()*0.078), int(self.width()*0.3), self.icon_size),
        )
        self.tab4.label3.setGeometry(
            QtCore.QRect(int(self.width()*0.68), int(self.width()*0.155), int(self.width()*0.3), self.icon_size),
        )
        self.tab4.label4.setGeometry(
            QtCore.QRect(int(self.width()*0.68), int(self.width()*0.233), int(self.width()*0.3), self.icon_size),
        )
        self.tab4.label5.setGeometry(
            QtCore.QRect(int(self.width()*0.68), int(self.width()*0.310), int(self.width()*0.3), self.icon_size),
        )
        self.tab4.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.label5.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line1 = QLineEdit(self.tab4)
        self.tab4.line2 = QLineEdit(self.tab4)
        self.tab4.line3 = QLineEdit(self.tab4)
        self.tab4.line4 = QLineEdit(self.tab4)
        self.tab4.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line3.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line4.setStyleSheet(LINE_EDIT_STYLE)
        self.tab4.line1.setGeometry(
            QtCore.QRect(int(self.width()*0.698), int(self.width()*0.116), int(self.width()*0.27), self.icon_size),
        )
        self.tab4.line2.setGeometry(
            QtCore.QRect(int(self.width()*0.698), int(self.width()*0.194), int(self.width()*0.27), self.icon_size),
        )
        self.tab4.line3.setGeometry(
            QtCore.QRect(int(self.width()*0.698), int(self.width()*0.271), int(self.width()*0.27), self.icon_size),
        )
        self.tab4.line4.setGeometry(
            QtCore.QRect(int(self.width()*0.698), int(self.width()*0.349), int(self.width()*0.27), self.icon_size),
        )
        self.tab4.line1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line4.setAlignment(QtCore.Qt.AlignCenter)


class SettingR(QWidget):
    """
    setting window
    """

    def __init__(self):
        super(SettingR, self).__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.26  # 280
        width = height*2.14  # 600
        fixed_h = width*2//30
        self.setFixedSize(width, height)
        self.setWindowTitle('Setting')
        self.setWindowIcon(
            QIcon('ico\\settings.svg'),
        )
        self.setStyleSheet(BGC_STYLE2)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.check = SwitchBtn(self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.combobox = QComboBox(self)
        self.label1.setText('START DIR')
        self.label2.setText('SAVE DIR')
        self.label3.setText('OPEN AS PREVIOUS')
        self.combobox.addItem('English')
        self.combobox.addItem('中文')
        self.combobox.addItem('日本語')
        self.label1.setStyleSheet(LABEL_STYLE2)
        self.label2.setStyleSheet(LABEL_STYLE2)
        self.label3.setStyleSheet(LABEL_STYLE2)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.button1.setStyleSheet(BUTTON_STYLE4)
        self.button2.setStyleSheet(BUTTON_STYLE4)
        self.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.label1.setAlignment(QtCore.Qt.AlignLeft)
        self.label2.setAlignment(QtCore.Qt.AlignLeft)
        self.label3.setAlignment(QtCore.Qt.AlignLeft)
        self.check.setGeometry(
            QtCore.QRect(width*0.8, height/2, fixed_h*2, fixed_h*0.75),
        )
        self.line1.setGeometry(
            QtCore.QRect(width*0.27, height//14, fixed_h*10, fixed_h),
        )
        self.line2.setGeometry(
            QtCore.QRect(width*0.27, height*2//7, fixed_h*10, fixed_h),
        )
        self.label1.setGeometry(
            QtCore.QRect(width*0.07, height*0.09, fixed_h*2.5, fixed_h),
        )
        self.label2.setGeometry(
            QtCore.QRect(width*0.07, height*0.3, fixed_h*2.5, fixed_h),
        )
        self.label3.setGeometry(
            QtCore.QRect(width*0.07, height/2, fixed_h*5, fixed_h),
        )
        self.button1.setGeometry(
            QtCore.QRect(width*0.85, height//14, fixed_h*1.2, fixed_h),
        )
        self.button2.setGeometry(
            QtCore.QRect(width*0.85, height*2//7, fixed_h*1.2, fixed_h),
        )
        self.combobox.setGeometry(
            QtCore.QRect(width*0.06, width/3, fixed_h*17/4, fixed_h),
        )
        self.button1.setIcon(QIcon('ico\\folder.svg'))
        self.button2.setIcon(QIcon('ico\\folder.svg'))
        self.setWindowOpacity(0.92)


class AboutR(QWidget):
    """
    about window
    """
    def __init__(self):
        super(AboutR, self).__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.19
        width = height*2.2
        self.setFixedSize(width, height)
        self.setWindowTitle('version 1.5')
        self.setWindowIcon(QIcon('ico\\info.svg'))
        self.setStyleSheet(BGC_STYLE2)
        self.label = QLabel(self)
        self.label.setText(
            "<p>Author: Nianze A. Tao</p>"
            "<p>MIT licence</p>"
            "<p>Github page:</p>"
            "<a href='https://github.com/Augus1999/pyPDFeditor-GUI'>"
            "<small>https://github.com/Augus1999/pyPDFeditor-GUI</small></a>"
        )
        self.label.setStyleSheet(LABEL_STYLE1)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setGeometry(
            QtCore.QRect(height//10, height//10, int(width*0.91), int(height*0.9)),
        )
        self.label.setOpenExternalLinks(True)
        self.setWindowOpacity(0.92)


class PermMenuR(QWidget):
    """
    permission setting menu window
    """
    def __init__(self):
        super(PermMenuR, self).__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.37  # 400
        width = height*1.5  # 600
        icon_size_1 = height//10
        icon_size_2 = width//20
        self.setFixedSize(width, height)
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('ico\\lock.svg'))
        self.setStyleSheet(BGC_STYLE2)
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
        self.label1.setText('Enable Print')
        self.label2.setText('Enable Modifying File')
        self.label3.setText('Enable Copy')
        self.label4.setText('Enable Adding Annotations')
        self.label5.setText('Enable Filling in Form')
        self.label6.setText('Enable Accessing Contents')
        self.label7.setText('Enable Page Editing')
        self.label8.setText('Enable HD Print')
        self.label1.setAlignment(QtCore.Qt.AlignLeft)
        self.label2.setAlignment(QtCore.Qt.AlignLeft)
        self.label3.setAlignment(QtCore.Qt.AlignLeft)
        self.label4.setAlignment(QtCore.Qt.AlignLeft)
        self.label5.setAlignment(QtCore.Qt.AlignLeft)
        self.label6.setAlignment(QtCore.Qt.AlignLeft)
        self.label7.setAlignment(QtCore.Qt.AlignLeft)
        self.label8.setAlignment(QtCore.Qt.AlignLeft)
        self.check1.setGeometry(
            QtCore.QRect(width*0.7, height/16, icon_size_1*2, icon_size_2),
        )
        self.check2.setGeometry(
            QtCore.QRect(width*0.7, height*13/80, icon_size_1*2, icon_size_2),
        )
        self.check3.setGeometry(
            QtCore.QRect(width*0.7, height*21/80, icon_size_1*2, icon_size_2),
        )
        self.check4.setGeometry(
            QtCore.QRect(width*0.7, height*29/80, icon_size_1*2, icon_size_2),
        )
        self.check5.setGeometry(
            QtCore.QRect(width*0.7, height*37/80, icon_size_1*2, icon_size_2),
        )
        self.check6.setGeometry(
            QtCore.QRect(width*0.7, height*9/16, icon_size_1*2, icon_size_2),
        )
        self.check7.setGeometry(
            QtCore.QRect(width*0.7, height*53/80, icon_size_1*2, icon_size_2),
        )
        self.check8.setGeometry(
            QtCore.QRect(width*0.7, height*61/80, icon_size_1*2, icon_size_2),
        )
        self.label1.setGeometry(
            QtCore.QRect(height/8, height/16, icon_size_2*10, icon_size_1),
        )
        self.label2.setGeometry(
            QtCore.QRect(height/8, height*13/80, icon_size_2*10, icon_size_1),
        )
        self.label3.setGeometry(
            QtCore.QRect(height/8, height*21/80, icon_size_2*10, icon_size_1),
        )
        self.label4.setGeometry(
            QtCore.QRect(height/8, height*29/80, icon_size_2*10, icon_size_1),
        )
        self.label5.setGeometry(
            QtCore.QRect(height/8, height*37/80, icon_size_2*10, icon_size_1),
        )
        self.label6.setGeometry(
            QtCore.QRect(height/8, height*9/16, icon_size_2*10, icon_size_1),
        )
        self.label7.setGeometry(
            QtCore.QRect(height/8, height*53/80, icon_size_2*10, icon_size_1),
        )
        self.label8.setGeometry(
            QtCore.QRect(height/8, height*61/80, icon_size_2*10, icon_size_1),
        )
        self.label1.setStyleSheet(LABEL_STYLE1)
        self.label2.setStyleSheet(LABEL_STYLE1)
        self.label3.setStyleSheet(LABEL_STYLE1)
        self.label4.setStyleSheet(LABEL_STYLE1)
        self.label5.setStyleSheet(LABEL_STYLE1)
        self.label6.setStyleSheet(LABEL_STYLE1)
        self.label7.setStyleSheet(LABEL_STYLE1)
        self.label8.setStyleSheet(LABEL_STYLE1)
        self.check1.setChecked(True)
        self.check5.setChecked(True)
        self.check6.setChecked(True)
        self.check8.setChecked(True)
        self.setWindowOpacity(0.92)


class FontDialogR(QWidget):
    def __init__(self):
        super(FontDialogR, self).__init__()
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()*0.27
        width = height*1.38
        self.setFixedSize(width, height)
        self.setWindowTitle('Select Font')
        self.setWindowIcon(QIcon('ico\\font.svg'))
        self.combobox = QComboBox(self)
        self.combobox.setGeometry(
            QtCore.QRect(width//40, width//40, int(width*0.95), width//10),
        )
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setGeometry(
            QtCore.QRect(width//40, int(width*0.15), int(width*0.95), int(width*0.55)),
        )
        self.setWindowOpacity(0.92)
