# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5.QtGui import QIcon
from .basics import (
    MAX_WIDTH,
    MAX_HEIGHT,
)
from .styleSheets import (
    SCROLL_BAR_STYLE_H,
    SCROLL_BAR_STYLE_V,
    COMBO_BOX_STYLE,
    LINE_EDIT_STYLE1,
    LINE_EDIT_STYLE2,
    TEXTEDIT_STYlE,
    BUTTON_STYLE1,
    BUTTON_STYLE2,
    BUTTON_STYLE3,
    BUTTON_STYLE4,
    BUTTON_STYLE5,
    BUTTON_STYLE6,
    TABLE_STYLE1,
    TABLE_STYLE2,
    LABEL_STYLE,
    BGC_STYLE1,
    BGC_STYLE2,
)
from PyQt5 import (
    QtCore,
    QtWidgets,
    QtWebEngineWidgets,
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
    QCheckBox,
)


class MainR(QTabWidget):
    """
    main widow
    """
    def __init__(self):
        super(MainR, self).__init__()
        self.setFixedSize(MAX_WIDTH, MAX_HEIGHT)
        self.setWindowTitle('PDF Editor')
        self.setWindowIcon(
            QIcon('ico\\pdf icon.ico'),
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

    def tab1_init(self):
        self.tab1.table = QTableWidget(self.tab1)
        self.tab1.scroll_bar = QtWidgets.QScrollBar(self.tab1)
        self.tab1.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab1.button1 = QPushButton(self.tab1)
        self.tab1.button2 = QPushButton(self.tab1)
        self.tab1.button3 = QPushButton(self.tab1)
        self.tab1.button4 = QPushButton(self.tab1)
        self.tab1.button5 = QPushButton(self.tab1)
        self.tab1.button1.setIcon(QIcon('ico\\new.png'))
        self.tab1.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab1.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab1.button4.setIcon(QIcon('ico\\clean.png'))
        self.tab1.button5.setIcon(QIcon('ico\\about.png'))
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
        self.tab2.button1.setIcon(QIcon('ico\\new.png'))
        self.tab2.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab2.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab2.button4.setIcon(QIcon('ico\\clean.png'))
        self.tab2.button5.setIcon(QIcon('ico\\col1.png'))
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
        self.tab3.table = QTableWidget(self.tab3)
        self.tab3.table.setShowGrid(False)
        self.tab3.table.verticalHeader().setVisible(False)
        self.tab3.table.horizontalHeader().setVisible(False)
        self.tab3.table.setGeometry(
            QtCore.QRect(20, 100,
                         (self.height()-170)*3//4,
                         self.height()-170),
        )
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
        self.tab3.button1.setIcon(QIcon('ico\\new.png'))
        self.tab3.button2.setIcon(QIcon('ico\\disk.png'))
        self.tab3.button3.setIcon(QIcon('ico\\settings.png'))
        self.tab3.button4.setIcon(QIcon('ico\\palette.png'))
        self.tab3.button5.setIcon(QIcon('ico\\view.png'))
        self.tab3.button6.setText('...')
        self.tab3.button1.setStyleSheet(BUTTON_STYLE2)
        self.tab3.button2.setStyleSheet(BUTTON_STYLE2)
        self.tab3.button3.setStyleSheet(BUTTON_STYLE6)
        self.tab3.button4.setStyleSheet(BUTTON_STYLE3)
        self.tab3.button5.setStyleSheet(BUTTON_STYLE3)
        self.tab3.button6.setStyleSheet(BUTTON_STYLE3)
        self.tab3.scroll_bar = QtWidgets.QScrollBar(self.tab3)
        self.tab3.scroll_bar.setStyleSheet(SCROLL_BAR_STYLE_V)
        self.tab3.button1.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button2.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button3.setIconSize(QtCore.QSize(40, 40))
        self.tab3.button4.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button5.setIconSize(QtCore.QSize(30, 30))
        self.tab3.button3.setToolTip('Settings')
        self.tab3.button4.setToolTip('colours')
        self.tab3.button5.setToolTip('preview')
        self.tab3.button6.setToolTip('more')
        self.tab3.button1.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.tab3.button2.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.tab3.button3.setGeometry(QtCore.QRect(230, 10, 80, 80))
        self.tab3.button4.setGeometry(QtCore.QRect(1042, 550, 40, 40))
        self.tab3.button5.setGeometry(QtCore.QRect(1042, 600, 40, 40))
        self.tab3.button6.setGeometry(QtCore.QRect(1090, 760, 40, 40))
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
        self.tab3.line1.setPlaceholderText('user password here')
        self.tab3.line2.setPlaceholderText('owner password here')
        self.tab3.line3.setText('90')
        self.tab3.line4.setText('40')
        self.tab3.line5.setText(' 0')
        self.tab3.text.setStyleSheet(TEXTEDIT_STYlE.format('14'))
        self.tab3.line1.setStyleSheet(LINE_EDIT_STYLE1.format("#F1F2FF"))
        self.tab3.line2.setStyleSheet(LINE_EDIT_STYLE1.format("#F1F1FF"))
        self.tab3.line3.setStyleSheet(LINE_EDIT_STYLE1.format("#F1F3FF"))
        self.tab3.line4.setStyleSheet(LINE_EDIT_STYLE1.format("#F1F3FF"))
        self.tab3.line5.setStyleSheet(LINE_EDIT_STYLE1.format("#F1F3FF"))
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
        self.tab3.label1.setGeometry(QtCore.QRect(733, 100, 300, 40))
        self.tab3.label2.setGeometry(QtCore.QRect(733, 300, 300, 40))
        self.tab3.label3.setGeometry(QtCore.QRect(992, 500, 40, 40))
        self.tab3.label4.setGeometry(QtCore.QRect(832, 500, 120, 40))
        self.tab3.label5.setGeometry(QtCore.QRect(880, 840, 160, 40))
        self.tab3.label6.setGeometry(QtCore.QRect(992, 550, 40, 40))
        self.tab3.label7.setGeometry(QtCore.QRect(850, 550, 100, 40))
        self.tab3.label8.setGeometry(QtCore.QRect(733, 640, 300, 40))
        self.tab3.label9.setGeometry(QtCore.QRect(850, 600, 100, 40))
        self.tab3.label10.setGeometry(QtCore.QRect(992, 600, 40, 40))
        self.tab3.label11.setGeometry(QtCore.QRect(880, 800, 160, 40))
        self.tab3.label12.setGeometry(QtCore.QRect(880, 760, 160, 40))
        self.tab3.label1.setText('.'*10+'password'+'.'*10)
        self.tab3.label2.setText('.' * 10 + 'watermark' + '.' * 10)
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
        self.tab3.check = QCheckBox(self.tab3)
        self.tab3.check1 = QCheckBox(self.tab3)
        self.tab3.check2 = QCheckBox(self.tab3)
        self.tab3.check.setChecked(True)
        self.tab3.check1.setChecked(False)
        self.tab3.check2.setChecked(False)
        self.tab3.check.setGeometry(QtCore.QRect(1050, 840, 40, 40))
        self.tab3.check1.setGeometry(QtCore.QRect(1050, 800, 40, 40))
        self.tab3.check2.setGeometry(QtCore.QRect(1050, 760, 40, 40))

    def tab4_init(self):
        self.tab4.setStyleSheet(BGC_STYLE2)
        self.tab4.button1 = QPushButton(self.tab4)
        self.tab4.button2 = QPushButton(self.tab4)
        self.tab4.button1.setIcon(QIcon('ico\\new.png'))
        self.tab4.button2.setIcon(QIcon('ico\\disk.png'))
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
        self.tab4.label1.setText(
            '''
            {}Catalogue{}\n
            Edit the catalog in the format of 
            \"lvl-->title-->page\"
            e.g.
            *-->chapter 1-->1
            **-->section 1-->1
            **-->section 2-->5
            *-->chapter 2-->17
            '''.format('.'*10, '.'*10)
        )
        self.tab4.label2.setText('.'*10+'Title'+'.'*10)
        self.tab4.label3.setText('.'*10+'Author'+'.'*10)
        self.tab4.label4.setText('.'*10+'Subject'+'.'*10)
        self.tab4.label5.setText('.'*10+'Keywords'+'.'*10)
        self.tab4.label1.setGeometry(
            QtCore.QRect(10, 100, self.width()//3-20, 250),
        )
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
        self.tab4.line1.setStyleSheet(LINE_EDIT_STYLE1.format('#F1F3FF'))
        self.tab4.line2.setStyleSheet(LINE_EDIT_STYLE1.format('#F1F3FF'))
        self.tab4.line3.setStyleSheet(LINE_EDIT_STYLE1.format('#F1F3FF'))
        self.tab4.line4.setStyleSheet(LINE_EDIT_STYLE1.format('#F1F3FF'))
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
        self.setFixedSize(600, 400)
        self.setWindowTitle('Setting')
        self.setWindowIcon(
            QIcon('ico\\settings.png'),
        )
        self.setStyleSheet(BGC_STYLE2)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.line1 = QLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line3 = QLineEdit(self)
        self.line4 = QLineEdit(self)
        self.button1 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.button3 = QPushButton(self)
        self.button4 = QPushButton(self)
        self.button5 = QPushButton(self)
        self.combobox = QComboBox(self)
        self.button1.setText('view')
        self.button2.setText('view')
        self.button3.setText('Apply')
        self.button4.setText('view')
        self.button5.setText('view')
        self.label1.setText('START DIR')
        self.label2.setText('SAVE DIR')
        self.label3.setText('PDF.JS DIR')
        self.label4.setText('FONT FILE')
        self.combobox.addItem('English')
        self.combobox.addItem('中文')
        self.combobox.addItem('日本語')
        self.label1.setStyleSheet(LABEL_STYLE)
        self.label2.setStyleSheet(LABEL_STYLE)
        self.label3.setStyleSheet(LABEL_STYLE)
        self.label4.setStyleSheet(LABEL_STYLE)
        self.combobox.setStyleSheet(COMBO_BOX_STYLE)
        self.button1.setStyleSheet(BUTTON_STYLE4)
        self.button2.setStyleSheet(BUTTON_STYLE4)
        self.button3.setStyleSheet(BUTTON_STYLE5)
        self.button4.setStyleSheet(BUTTON_STYLE4)
        self.button5.setStyleSheet(BUTTON_STYLE4)
        self.line1.setStyleSheet(LINE_EDIT_STYLE2.format("#F5DCE3"))
        self.line2.setStyleSheet(LINE_EDIT_STYLE2.format("#F5DCE3"))
        self.line3.setStyleSheet(LINE_EDIT_STYLE2.format("#F1F2FF"))
        self.line4.setStyleSheet(LINE_EDIT_STYLE2.format("#F3F2FF"))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.line1.setGeometry(QtCore.QRect(160, 20, 400, 40))
        self.line2.setGeometry(QtCore.QRect(160, 80, 400, 40))
        self.line3.setGeometry(QtCore.QRect(160, 140, 400, 40))
        self.line4.setGeometry(QtCore.QRect(160, 200, 400, 40))
        self.label1.setGeometry(QtCore.QRect(40, 20, 100, 40))
        self.label2.setGeometry(QtCore.QRect(40, 80, 100, 40))
        self.label3.setGeometry(QtCore.QRect(40, 140, 100, 40))
        self.label4.setGeometry(QtCore.QRect(40, 200, 100, 40))
        self.button1.setGeometry(QtCore.QRect(510, 20, 50, 40))
        self.button2.setGeometry(QtCore.QRect(510, 80, 50, 40))
        self.button3.setGeometry(QtCore.QRect(510, 350, 80, 40))
        self.button4.setGeometry(QtCore.QRect(510, 140, 50, 40))
        self.button5.setGeometry(QtCore.QRect(510, 200, 50, 40))
        self.combobox.setGeometry(QtCore.QRect(370, 260, 180, 40))


class PDFViewR(QtWebEngineWidgets.QWebEngineView):
    """
    PDF viewer window
    """
    def __init__(self):
        super(PDFViewR, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('PDF viewer')
        self.setWindowIcon(
            QIcon('ico\\pdf icon.ico'),
        )

    def view(self, pdf_address, pdf_js_address):
        self.load(QtCore.QUrl.fromUserInput(
            '%s?file=%s' % (pdf_js_address, pdf_address))
        )


class AboutR(QWidget):
    """
    about window
    """
    def __init__(self):
        super(AboutR, self).__init__()
        self.setFixedSize(350, 200)
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('ico\\about.png'))
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
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setGeometry(
            QtCore.QRect(20, 0, self.width()-40, self.height()-20)
        )
        self.label.setOpenExternalLinks(True)


class PermMenuR(QWidget):
    """
    permission setting menu window
    """
    def __init__(self):
        super(PermMenuR, self).__init__()
        self.setFixedSize(400, 240)
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('ico\\tab3.png'))
        self.setStyleSheet(BGC_STYLE2)
        self.check1 = QCheckBox(self)
        self.check2 = QCheckBox(self)
        self.check3 = QCheckBox(self)
        self.check4 = QCheckBox(self)
        self.check5 = QCheckBox(self)
        self.check6 = QCheckBox(self)
        self.check7 = QCheckBox(self)
        self.check8 = QCheckBox(self)
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)
        self.button = QPushButton(self)
        self.button.setText('Apply')
        self.label1.setText('permit print')
        self.label2.setText('allow modify')
        self.label3.setText('allow copy')
        self.label4.setText('allow annotate')
        self.label5.setText('allow fill in form')
        self.label6.setText('access content')
        self.label7.setText('allow page edit')
        self.label8.setText('permit HD print')
        self.label1.setAlignment(QtCore.Qt.AlignLeft)
        self.label2.setAlignment(QtCore.Qt.AlignLeft)
        self.label3.setAlignment(QtCore.Qt.AlignLeft)
        self.label4.setAlignment(QtCore.Qt.AlignLeft)
        self.label5.setAlignment(QtCore.Qt.AlignLeft)
        self.label6.setAlignment(QtCore.Qt.AlignLeft)
        self.label7.setAlignment(QtCore.Qt.AlignLeft)
        self.label8.setAlignment(QtCore.Qt.AlignLeft)
        self.button.setGeometry(QtCore.QRect(300, 180, 80, 40))
        self.check1.setGeometry(QtCore.QRect(20, 20, 40, 40))
        self.check2.setGeometry(QtCore.QRect(20, 60, 40, 40))
        self.check3.setGeometry(QtCore.QRect(20, 100, 40, 40))
        self.check4.setGeometry(QtCore.QRect(20, 140, 40, 40))
        self.check5.setGeometry(QtCore.QRect(220, 20, 40, 40))
        self.check6.setGeometry(QtCore.QRect(220, 60, 40, 40))
        self.check7.setGeometry(QtCore.QRect(220, 100, 40, 40))
        self.check8.setGeometry(QtCore.QRect(220, 140, 40, 40))
        self.label1.setGeometry(QtCore.QRect(50, 25, 120, 40))
        self.label2.setGeometry(QtCore.QRect(50, 65, 120, 40))
        self.label3.setGeometry(QtCore.QRect(50, 105, 120, 40))
        self.label4.setGeometry(QtCore.QRect(50, 145, 120, 40))
        self.label5.setGeometry(QtCore.QRect(250, 25, 120, 40))
        self.label6.setGeometry(QtCore.QRect(250, 65, 120, 40))
        self.label7.setGeometry(QtCore.QRect(250, 105, 120, 40))
        self.label8.setGeometry(QtCore.QRect(250, 145, 120, 40))
        self.button.setStyleSheet(BUTTON_STYLE5)
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
