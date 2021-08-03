# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import fitz
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QApplication,
)


class MyLineEdit(QLineEdit):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(500, 300)
        self.setWindowTitle('decrypter')
        self.setWindowIcon(QIcon('ico\\tab3.png'))
        self.setStyleSheet('background-color:#ffffff')
        self.file = None
        self.file_name = str()
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.line1 = MyLineEdit(self)
        self.line2 = QLineEdit(self)
        self.line1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line1.setPlaceholderText('click here to open a file')
        self.line2.setPlaceholderText('press \"Enter\" to apply')
        self.label1.setGeometry(QtCore.QRect(40, 40, 80, 40))
        self.label2.setGeometry(QtCore.QRect(40, 120, 80, 40))
        self.label3.setGeometry(QtCore.QRect(40, 160, 420, 100))
        self.line1.setGeometry(QtCore.QRect(160, 40, 300, 40))
        self.line2.setGeometry(QtCore.QRect(160, 120, 300, 40))
        self.label1.setText('File:')
        self.label2.setText('Password:')
        self.line1.clicked.connect(self._open)
        self.line2.returnPressed.connect(self._decrypt)

    def _open(self):
        file_name, state = QFileDialog.getOpenFileName(
            None,
            'open file',
            os.getcwd(),
            '*.pdf'
        )
        if state:
            self.line1.clear()
            self.label3.clear()
            try:
                self.file_name = file_name.replace('/', '\\')
                self.file = fitz.open(self.file_name)
                self.line1.setText(self.file_name)
                if not self.file.needsPass:
                    self.label3.setText('no password needed')
                    self.file = None
                else:
                    pass
            except RuntimeError:
                QMessageBox.critical(
                    None,
                    'Error',
                    ' Format error:\n cannot open this file',
                    QMessageBox.Yes,
                )
        else:
            pass

    def _decrypt(self):
        if self.file is not None:
            self.label3.clear()
            self.file.authenticate(self.line2.text())
            if self.file.is_encrypted:
                self.label3.setText('wrong password')
            else:
                outfile = os.path.join(
                    os.path.dirname(self.file_name),
                    os.path.basename(self.file_name).split('.')[0]+'_d.pdf',
                )
                self.file.save(
                    outfile,
                    garbage=4,
                    owner_pw=None,
                    user_pw=None,
                )
                self.label3.setText('finished!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    # **************** 8 9 6 4 ****************
