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


import os
import pythoncom
from win32com.shell import shell


def set_shortcut():
    try:
        filename = os.getcwd()+"\\run.vbs"
        iconname = os.getcwd()+"\\ico\\pdf icon.ico"
        lnk_name = os.getcwd()+"\\pdfEditor.lnk"
        shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None,
                                              pythoncom.CLSCTX_INPROC_SERVER,
                                              shell.IID_IShellLink)
        shortcut.SetPath(filename)
        shortcut.SetWorkingDirectory(os.getcwd())
        shortcut.SetIconLocation(iconname, 0)
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnk_name, 0)
    except Exception as e:
        print(e.args)


set_shortcut()
