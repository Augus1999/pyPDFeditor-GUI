# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QColor, QFont, QPixmap, QTransform
from .styleSheets import *
from PyQt5 import (
    QtCore,
    QtWidgets,
)
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
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
        self.draw_bg(painter)
        self.draw_text(painter)
        self.draw_slider(painter)
        painter.end()

    def draw_text(self, painter) -> None:
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
        self.size1 = height * 0.04
        self.size2 = height * 0.03
        self.resize(width, height)
        self.setMinimumSize(width * 0.9, height * 0.9)
        self.setWindowTitle('PDF Editor')
        self.setWindowIcon(QIcon('ico\\pdf icon.svg'))
        self.setTabShape(QTabWidget.Rounded)
        self.setTabPosition(QTabWidget.West)
        self.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.setStyleSheet(TAB_STYLE)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab1_init()
        self.tab2_init()
        self.tab3_init()
        self.tab4_init()
        matrix = QTransform()
        matrix.rotate(90)
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

    def tab1_init(self) -> None:
        grid = QGridLayout(self.tab1)
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.scroll_bar = QtWidgets.QScrollBar(self.tab1)
        self.tab1.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE)
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
        self.tab1.button1.setStyleSheet(BUTTON_STYLE)
        self.tab1.button2.setStyleSheet(BUTTON_STYLE)
        self.tab1.button3.setStyleSheet(BUTTON_STYLE)
        self.tab1.button4.setStyleSheet(BUTTON_STYLE)
        self.tab1.button5.setStyleSheet(BUTTON_STYLE)
        self.tab1.button1.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab1.button2.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab1.button3.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab1.button4.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab1.button5.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab1.button1.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab1.button2.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab1.button3.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab1.button4.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab1.button5.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab1.table.setVerticalScrollBar(self.tab1.scroll_bar)
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
        grid.addWidget(self.tab1.button1, 0, 0)
        grid.addWidget(self.tab1.button2, 0, 1)
        grid.addWidget(self.tab1.button3, 0, 2)
        grid.addWidget(self.tab1.button4, 0, 3)
        grid.addWidget(self.tab1.button5, 0, 8)
        grid.addWidget(self.tab1.table, 1, 0, 10, 9)

    def tab2_init(self) -> None:
        grid = QGridLayout(self.tab2)
        self.tab2.table = QTableWidget(self.tab2)
        self.tab2.scroll_bar = QtWidgets.QScrollBar(self.tab2)
        self.tab2.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE)
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
        self.tab2.button1.setStyleSheet(BUTTON_STYLE)
        self.tab2.button2.setStyleSheet(BUTTON_STYLE)
        self.tab2.button3.setStyleSheet(BUTTON_STYLE)
        self.tab2.button4.setStyleSheet(BUTTON_STYLE)
        self.tab2.button5.setStyleSheet(BUTTON_STYLE)
        self.tab2.button1.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab2.button2.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab2.button3.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab2.button4.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab2.button5.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab2.button1.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab2.button2.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab2.button3.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab2.button4.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab2.button5.setFixedSize(self.size1 * 2, self.size1 * 2)
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
        grid.addWidget(self.tab2.button1, 0, 0)
        grid.addWidget(self.tab2.button2, 0, 1)
        grid.addWidget(self.tab2.button3, 0, 2)
        grid.addWidget(self.tab2.button4, 0, 3)
        grid.addWidget(self.tab2.button5, 0, 8)
        grid.addWidget(self.tab2.table, 1, 0, 10, 9)

    def tab3_init(self) -> None:
        grid = QGridLayout(self.tab3)
        self.tab3.setStyleSheet(BGC_STYLE2)
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(True)
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
        self.tab3.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab3.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab3.button3.setIcon(QIcon('ico\\settings.svg'))
        self.tab3.button4.setIcon(QIcon('ico\\color.svg'))
        self.tab3.button5.setIcon(QIcon('ico\\view.svg'))
        self.tab3.button6.setIcon(QIcon('ico\\row.svg'))
        self.tab3.button7.setIcon(QIcon('ico\\font.svg'))
        self.tab3.button1.setStyleSheet(BUTTON_STYLE)
        self.tab3.button2.setStyleSheet(BUTTON_STYLE)
        self.tab3.button3.setStyleSheet(BUTTON_STYLE)
        self.tab3.button4.setStyleSheet(BUTTON_STYLE)
        self.tab3.button5.setStyleSheet(BUTTON_STYLE)
        self.tab3.button6.setStyleSheet(BUTTON_STYLE)
        self.tab3.button7.setStyleSheet(BUTTON_STYLE)
        self.tab3.scroll_bar = QtWidgets.QScrollBar(self.tab3)
        self.tab3.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE)
        self.tab3.button1.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab3.button2.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab3.button3.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab3.button4.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab3.button5.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab3.button6.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab3.button7.setIconSize(QtCore.QSize(self.size2, self.size2))
        self.tab3.table.setFixedSize(self.height() * 0.6, self.height() * 0.8)
        self.tab3.button1.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab3.button2.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab3.button3.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab3.button4.setFixedSize(self.size1, self.size1)
        self.tab3.button5.setFixedSize(self.size1, self.size1)
        self.tab3.button6.setFixedSize(self.size1, self.size1)
        self.tab3.button7.setFixedSize(self.size1, self.size1)
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
        self.tab3.text.setVerticalScrollBar(self.tab3.scroll_bar)
        self.tab3.label3.setFixedSize(self.size1, self.size1)
        self.tab3.label6.setFixedSize(self.size1, self.size1)
        self.tab3.label10.setFixedSize(self.size1, self.size1)
        self.tab3.label3.setText('pt')
        self.tab3.label6.setText('%')
        self.tab3.label8.setText('* '*26)
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
        grid.addWidget(self.tab3.button1, 0, 0)
        grid.addWidget(self.tab3.button2, 0, 1)
        grid.addWidget(self.tab3.button3, 0, 2)
        grid.addWidget(self.tab3.table, 1, 0, 14, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.label1, 1, 5, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.line1, 2, 5, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.line2, 3, 5, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.label2, 4, 5, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.text, 5, 5, 2, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.label4, 7, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label7, 8, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label9, 9, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.line3, 7, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.line4, 8, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.line5, 9, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.label3, 7, 7, 1, 1, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label6, 8, 7, 1, 1, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label10, 9, 7, 1, 1, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.button7, 7, 8, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.tab3.button4, 8, 8, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.tab3.button5, 9, 8, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.tab3.label8, 10, 5, 1, 4, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.label12, 11, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label11, 12, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.label5, 13, 5, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.tab3.check2, 11, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.check1, 12, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.check, 13, 7, 1, 1, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab3.button6, 11, 8, 1, 1, QtCore.Qt.AlignLeft)

    def tab4_init(self) -> None:
        grid = QGridLayout(self.tab4)
        self.tab4.setStyleSheet(BGC_STYLE2)
        self.tab4.button1 = QPushButton(self.tab4)
        self.tab4.button2 = QPushButton(self.tab4)
        self.tab4.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab4.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab4.button1.setStyleSheet(BUTTON_STYLE)
        self.tab4.button2.setStyleSheet(BUTTON_STYLE)
        self.tab4.button1.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab4.button2.setIconSize(QtCore.QSize(self.size1, self.size1))
        self.tab4.button1.setFixedSize(self.size1 * 2, self.size1 * 2)
        self.tab4.button2.setFixedSize(self.size1 * 2, self.size1 * 2)
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
        self.tab4.table.setStyleSheet(TABLE_STYLE2)
        self.tab4.scroll_bar0 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar1 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar2 = QtWidgets.QScrollBar(self.tab4)
        self.tab4.scroll_bar0.setStyleSheet(SCROLL_BAR_STYLE)
        self.tab4.scroll_bar1.setStyleSheet(SCROLL_BAR_STYLE)
        self.tab4.scroll_bar2.setStyleSheet(SCROLL_BAR_STYLE_0)
        self.tab4.table.setVerticalScrollBar(self.tab4.scroll_bar0)
        self.tab4.text = QTextEdit(self.tab4)
        self.tab4.text.setStyleSheet(TEXTEDIT_STYlE)
        self.tab4.text.setVerticalScrollBar(self.tab4.scroll_bar1)
        self.tab4.text.setHorizontalScrollBar(self.tab4.scroll_bar2)
        self.tab4.text.setLineWrapColumnOrWidth(2000)
        self.tab4.text.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.tab4.label1 = QLabel(self.tab4)
        self.tab4.label2 = QLabel(self.tab4)
        self.tab4.label3 = QLabel(self.tab4)
        self.tab4.label4 = QLabel(self.tab4)
        self.tab4.label5 = QLabel(self.tab4)
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
        self.tab4.line1.setFixedSize(self.width() * 0.27, self.size1)
        self.tab4.line2.setFixedSize(self.width() * 0.27, self.size1)
        self.tab4.line3.setFixedSize(self.width() * 0.27, self.size1)
        self.tab4.line4.setFixedSize(self.width() * 0.27, self.size1)
        self.tab4.text.setFixedSize(self.width() * 0.25, self.height() * 0.47)
        self.tab4.line1.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line2.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line3.setAlignment(QtCore.Qt.AlignCenter)
        self.tab4.line4.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.button1, 0, 0)
        grid.addWidget(self.tab4.button2, 0, 1)
        grid.addWidget(self.tab4.text, 5, 0, 8, 3, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.table, 1, 3, 20, 3)
        grid.addWidget(self.tab4.label1, 2, 0, 3, 3, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.label2, 2, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.label3, 4, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.label4, 6, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.label5, 8, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.line1, 3, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.line2, 5, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.line3, 7, 7, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(self.tab4.line4, 9, 7, 1, 2, QtCore.Qt.AlignCenter)


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
        grid = QGridLayout(self)
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
        self.label1.setStyleSheet(LABEL_STYLE)
        self.label2.setStyleSheet(LABEL_STYLE)
        self.label3.setStyleSheet(LABEL_STYLE)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.button1.setStyleSheet(BUTTON_STYLE)
        self.button2.setStyleSheet(BUTTON_STYLE)
        self.line1.setStyleSheet(LINE_EDIT_STYLE)
        self.line2.setStyleSheet(LINE_EDIT_STYLE)
        self.label1.setAlignment(QtCore.Qt.AlignVCenter)
        self.label2.setAlignment(QtCore.Qt.AlignVCenter)
        self.label3.setAlignment(QtCore.Qt.AlignVCenter)
        self.check.setFixedSize(fixed_h*2, fixed_h*0.75)
        self.line1.setFixedSize(fixed_h*10, fixed_h)
        self.line2.setFixedSize(fixed_h * 10, fixed_h)
        self.button1.setFixedSize(fixed_h, fixed_h)
        self.button2.setFixedSize(fixed_h, fixed_h)
        self.combobox.setFixedSize(fixed_h*17/4, fixed_h)
        grid.addWidget(self.label1, 0, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label2, 1, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.label3, 2, 0, 1, 4, QtCore.Qt.AlignLeft)
        grid.addWidget(self.combobox, 3, 0)
        grid.addWidget(self.line1, 0, 1, 1, 5)
        grid.addWidget(self.line2, 1, 1, 1, 5)
        grid.addWidget(self.button1, 0, 4, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.button2, 1, 4, 1, 2, QtCore.Qt.AlignRight)
        grid.addWidget(self.check, 2, 5)
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
        width = height*1.8
        grid = QGridLayout(self)
        self.setFixedSize(width, height)
        self.setWindowTitle('version 1.6')
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
        self.label.setStyleSheet(LABEL_STYLE)
        self.label.setOpenExternalLinks(True)
        grid.addWidget(self.label, 0, 0, QtCore.Qt.AlignCenter)
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
        width = height*1.2  # 480
        x = height/5
        y = width/16
        grid = QGridLayout(self)
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
        grid = QGridLayout(self)
        self.resize(width, height)
        self.setWindowTitle('Select Font')
        self.setWindowIcon(QIcon('ico\\font.svg'))
        self.combobox = QComboBox(self)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        grid.addWidget(self.combobox, 0, 0, QtCore.Qt.AlignCenter)
        grid.addWidget(self.label, 1, 0, QtCore.Qt.AlignCenter)
        self.setWindowOpacity(0.92)
