# -*- coding: utf-8 -*-
# ! Python
# Author: Nianze A. TAO
import subprocess as sp
try:
    import PyQt5
    import fitz
except ImportError:
    while True:
        c = sp.call('pip install -r requirement.txt', shell=True)
        if c == 0:
            break
