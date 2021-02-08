# -*- coding: utf-8 -*-
# ! Python
# Author: Nianze A. TAO
import subprocess as sp
try:
    import PyQt5
except ImportError:
    while True:
        c = sp.call('pip install PyQt5', shell=True)
        if c == 0:
            break
try:
    import fitz
except ImportError:
    while True:
        c = sp.call('pip install PyMuPDF', shell=True)
        if c == 0:
            break
try:
    import PyPDF2
except ImportError:
    while True:
        c = sp.call('pip install PyPDF2', shell=True)
        if c == 0:
            break
