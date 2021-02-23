# -*- coding: utf-8 -*-
# ! Python
# Author: Nianze A. TAO
import platform
import subprocess as sp
try:
    import PyQt5
    import fitz
except ImportError:
    while True:
        c = sp.call('pip install -r requirements.txt', shell=True)
        if c == 0:
            break
_platform = platform.system()
if _platform == 'Windows':
    bat_script = '@echo off\npython main.py'
    vbs_script = r'CreateObject("WScript.Shell").Run "run.bat \c*",0'
    try:
        from win32com.shell import shell
    except ImportError:
        while True:
            c = sp.call('pip install pywin32')
            if c == 0:
                break
        from win32com.shell import shell

    import os
    import pythoncom


    def set_shortcut(filename, iconname, lnk_name):
        try:
            shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None,
                                                  pythoncom.CLSCTX_INPROC_SERVER,
                                                  shell.IID_IShellLink)
            shortcut.SetPath(filename)
            shortcut.SetWorkingDirectory(os.getcwd())
            shortcut.SetIconLocation(iconname, 0)
            shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnk_name, 0)
        except Exception as e:
            print(e.args)


    with open('run.bat', 'w', encoding='utf-8') as f:
        f.write(bat_script)
    with open('run.vbs', 'w', encoding='utf-8') as f:
        f.write(vbs_script)
    set_shortcut(filename=os.getcwd()+"\\run.vbs",
                 iconname=os.getcwd()+"\\ico\\pdf icon.ico",
                 lnk_name=os.getcwd()+"\\pdfEditor.lnk")
print('Finished!')
