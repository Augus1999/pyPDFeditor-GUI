import sys
import fitz
from PyQt5.QtWidgets import QApplication
from scripts import Main, __system__, __version__


if __name__ == '__main__':
    fitz.TOOLS.mupdf_display_errors(True)
    arg = sys.argv
    app = QApplication(arg)
    main = Main(__system__, __version__)
    main.show()
    main.windowChange()
    main.showMinimized()
    main.showNormal()
    main.close()
    sys.exit(app.exec_())
