# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon, QPainter, QPainterPath, QColor, QFont, QPixmap
from .basics import MAX_WIDTH, MAX_HEIGHT
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
        self.setFixedSize(MAX_WIDTH, MAX_HEIGHT)
        self.setWindowTitle('PDF Editor')
        self.setWindowIcon(
            QIcon('ico\\pdf icon.svg'),
        )
        self.setTabShape(QTabWidget.Rounded)
        self.setIconSize(QtCore.QSize(40, 40))
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
        self.tab1.button1.setIconSize(QtCore.QSize(50, 50))
        self.tab1.button2.setIconSize(QtCore.QSize(50, 50))
        self.tab1.button3.setIconSize(QtCore.QSize(50, 50))
        self.tab1.button4.setIconSize(QtCore.QSize(50, 50))
        self.tab1.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab1.table.setGeometry(
            QtCore.QRect(0, 100, self.width()-5, self.height()-170),
        )
        self.tab1.button1.setGeometry(
            QtCore.QRect(10, 10, 80, 80),
        )
        self.tab1.button2.setGeometry(
            QtCore.QRect(120, 10, 80, 80),
        )
        self.tab1.button3.setGeometry(
            QtCore.QRect(230, 10, 80, 80),
        )
        self.tab1.button4.setGeometry(
            QtCore.QRect(400, 10, 80, 80),
        )
        self.tab1.button5.setGeometry(
            QtCore.QRect(self.width()-80, 20, 50, 50)
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

    def tab2_init(self):
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
        self.tab2.button1.setIconSize(QtCore.QSize(50, 50))
        self.tab2.button2.setIconSize(QtCore.QSize(50, 50))
        self.tab2.button3.setIconSize(QtCore.QSize(50, 50))
        self.tab2.button4.setIconSize(QtCore.QSize(50, 50))
        self.tab2.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab2.table.setGeometry(
            QtCore.QRect(0, 100, self.width()-5, self.height()-170),
        )
        self.tab2.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab2.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab2.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab2.button4.setGeometry(QtCore.QRect(400, 10, 80, 80))
        self.tab2.button5.setGeometry(
            QtCore.QRect(self.width() - 80, 20, 50, 50)
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

    def tab3_init(self):
        self.tab3.setStyleSheet(BGC_STYLE2)
        self.tab3.label0 = QLabel(self.tab3)
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(
            QtCore.QRect(30, 105,
                         (self.height()-195)*3//4,
                         self.height()-195),
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
        self.tab3.button1.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button2.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button3.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button4.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button6.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button7.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button3.setToolTip('Settings')
        self.tab3.button4.setToolTip('colours')
        self.tab3.button5.setToolTip('preview')
        self.tab3.button6.setToolTip('more')
        self.tab3.button7.setToolTip('font')
        self.tab3.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab3.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab3.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab3.button4.setGeometry(QtCore.QRect(1042, 550, 40, 40))
        self.tab3.button5.setGeometry(QtCore.QRect(1042, 600, 40, 40))
        self.tab3.button6.setGeometry(QtCore.QRect(1042, 700, 40, 40))
        self.tab3.button7.setGeometry(QtCore.QRect(1042, 500, 40, 40))
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
        self.tab3.text.setGeometry(QtCore.QRect(733, 360, 300, 120))
        self.tab3.line1.setGeometry(QtCore.QRect(733, 160, 300, 40))
        self.tab3.line2.setGeometry(QtCore.QRect(733, 240, 300, 40))
        self.tab3.line3.setGeometry(QtCore.QRect(952, 500, 40, 40))
        self.tab3.line4.setGeometry(QtCore.QRect(952, 550, 40, 40))
        self.tab3.line5.setGeometry(QtCore.QRect(952, 600, 40, 40))
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
        self.tab3.label0.setStyleSheet('background-color:#daeaef')
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
        self.tab3.label0.setGeometry(QtCore.QRect(
            25,
            100,
            self.tab3.table.width()+10,
            self.tab3.table.height()+10,
        ))
        self.tab3.label1.setGeometry(QtCore.QRect(733, 100, 300, 40))
        self.tab3.label2.setGeometry(QtCore.QRect(733, 300, 300, 40))
        self.tab3.label3.setGeometry(QtCore.QRect(992, 500, 40, 40))
        self.tab3.label4.setGeometry(QtCore.QRect(832, 500, 120, 40))
        self.tab3.label5.setGeometry(QtCore.QRect(733, 780, 220, 40))
        self.tab3.label6.setGeometry(QtCore.QRect(992, 550, 40, 40))
        self.tab3.label7.setGeometry(QtCore.QRect(850, 550, 100, 40))
        self.tab3.label8.setGeometry(QtCore.QRect(733, 640, 300, 40))
        self.tab3.label9.setGeometry(QtCore.QRect(850, 600, 100, 40))
        self.tab3.label10.setGeometry(QtCore.QRect(992, 600, 40, 40))
        self.tab3.label11.setGeometry(QtCore.QRect(733, 740, 220, 40))
        self.tab3.label12.setGeometry(QtCore.QRect(733, 700, 220, 40))
        self.tab3.label1.setText('.'*10+'PASSWORD'+'.'*10)
        self.tab3.label2.setText('.' * 10 + 'WATERMARK' + '.' * 10)
        self.tab3.label3.setText('pt')
        self.tab3.label4.setText('Font Size:')
        self.tab3.label5.setText('Open after saving')
        self.tab3.label6.setText('%')
        self.tab3.label7.setText('Opacity:')
        self.tab3.label8.setText('.'*50)
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
        self.tab3.check.setGeometry(QtCore.QRect(950, 788, 80, 30))
        self.tab3.check1.setGeometry(QtCore.QRect(950, 748, 80, 30))
        self.tab3.check2.setGeometry(QtCore.QRect(950, 708, 80, 30))
        self.tab3.check.setChecked(True)
        self.tab3.check1.setChecked(False)
        self.tab3.check2.setChecked(False)

    def tab4_init(self):
        self.tab4.setStyleSheet(BGC_STYLE2)
        self.tab4.button1 = QPushButton(self.tab4)
        self.tab4.button2 = QPushButton(self.tab4)
        self.tab4.button1.setIcon(QIcon('ico\\Add.svg'))
        self.tab4.button2.setIcon(QIcon('ico\\down.svg'))
        self.tab4.button1.setStyleSheet(BUTTON_STYLE2)
        self.tab4.button2.setStyleSheet(BUTTON_STYLE2)
        self.tab4.button1.setIconSize(QtCore.QSize(40, 40))
        self.tab4.button2.setIconSize(QtCore.QSize(40, 40))
        self.tab4.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab4.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
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
            QtCore.QRect(self.width()//3, 100, self.width()//3, self.height()-170),
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
            QtCore.QRect(40, 350, self.width()//3-80, self.height()-500),
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
                200,
                200,
                QtCore.Qt.IgnoreAspectRatio,
                QtCore.Qt.SmoothTransformation,
            ),
        )
        self.tab4.label2.setText('.'*10+'Title'+'.'*10)
        self.tab4.label3.setText('.'*10+'Author'+'.'*10)
        self.tab4.label4.setText('.'*10+'Subject'+'.'*10)
        self.tab4.label5.setText('.'*10+'Keywords'+'.'*10)
        self.tab4.label1.setGeometry(QtCore.QRect(80, 100, 250, 250))
        self.tab4.label2.setGeometry(
            QtCore.QRect(2*self.width()//3+20, 100, self.width()//3-40, 40),
        )
        self.tab4.label3.setGeometry(
            QtCore.QRect(2*self.width()//3+20, 200, self.width()//3-40, 40),
        )
        self.tab4.label4.setGeometry(
            QtCore.QRect(2*self.width()//3+20, 300, self.width()//3-40, 40),
        )
        self.tab4.label5.setGeometry(
            QtCore.QRect(2*self.width()//3+20, 400, self.width()//3-40, 40),
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
            QtCore.QRect(2*self.width()//3+40, 150, self.width()//3-80, 40),
        )
        self.tab4.line2.setGeometry(
            QtCore.QRect(2*self.width()//3+40, 250, self.width()//3-80, 40),
        )
        self.tab4.line3.setGeometry(
            QtCore.QRect(2*self.width()//3+40, 350, self.width()//3-80, 40),
        )
        self.tab4.line4.setGeometry(
            QtCore.QRect(2*self.width()//3+40, 450, self.width()//3-80, 40),
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
        self.setFixedSize(600, 280)
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
        self.check.setGeometry(QtCore.QRect(480, 140, 80, 30))
        self.line1.setGeometry(QtCore.QRect(160, 20, 400, 40))
        self.line2.setGeometry(QtCore.QRect(160, 80, 400, 40))
        self.label1.setGeometry(QtCore.QRect(40, 25, 100, 40))
        self.label2.setGeometry(QtCore.QRect(40, 85, 100, 40))
        self.label3.setGeometry(QtCore.QRect(40, 140, 200, 40))
        self.button1.setGeometry(QtCore.QRect(510, 20, 50, 40))
        self.button2.setGeometry(QtCore.QRect(510, 80, 50, 40))
        self.combobox.setGeometry(QtCore.QRect(35, 200, 170, 40))
        self.button1.setIcon(QIcon('ico\\folder.svg'))
        self.button2.setIcon(QIcon('ico\\folder.svg'))
        self.setWindowOpacity(0.92)


class AboutR(QWidget):
    """
    about window
    """
    def __init__(self):
        super(AboutR, self).__init__()
        self.setFixedSize(440, 200)
        self.setWindowTitle(' ')
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
            QtCore.QRect(20, 20, self.width()-40, self.height()-20)
        )
        self.label.setOpenExternalLinks(True)
        self.setWindowOpacity(0.92)


class PermMenuR(QWidget):
    """
    permission setting menu window
    """
    def __init__(self):
        super(PermMenuR, self).__init__()
        self.setFixedSize(600, 400)
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
        self.check1.setGeometry(QtCore.QRect(420, 25, 80, 30))
        self.check2.setGeometry(QtCore.QRect(420, 65, 80, 30))
        self.check3.setGeometry(QtCore.QRect(420, 105, 80, 30))
        self.check4.setGeometry(QtCore.QRect(420, 145, 80, 30))
        self.check5.setGeometry(QtCore.QRect(420, 185, 80, 30))
        self.check6.setGeometry(QtCore.QRect(420, 225, 80, 30))
        self.check7.setGeometry(QtCore.QRect(420, 265, 80, 30))
        self.check8.setGeometry(QtCore.QRect(420, 305, 80, 30))
        self.label1.setGeometry(QtCore.QRect(50, 25, 300, 40))
        self.label2.setGeometry(QtCore.QRect(50, 65, 300, 40))
        self.label3.setGeometry(QtCore.QRect(50, 105, 300, 40))
        self.label4.setGeometry(QtCore.QRect(50, 145, 300, 40))
        self.label5.setGeometry(QtCore.QRect(50, 185, 300, 40))
        self.label6.setGeometry(QtCore.QRect(50, 225, 300, 40))
        self.label7.setGeometry(QtCore.QRect(50, 265, 300, 40))
        self.label8.setGeometry(QtCore.QRect(50, 305, 300, 40))
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
        self.setFixedSize(400, 290)
        self.setWindowTitle('Select Font')
        self.setWindowIcon(QIcon('ico\\font.svg'))
        self.combobox = QComboBox(self)
        self.combobox.setGeometry(QtCore.QRect(10, 10, 380, 40))
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setGeometry(QtCore.QRect(10, 60, 380, 220))
        self.setWindowOpacity(0.92)
