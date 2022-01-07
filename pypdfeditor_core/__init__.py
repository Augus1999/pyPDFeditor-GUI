# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
initialise the module
"""
import os
import platform
from .application import __main__

user_home = os.path.expanduser('~')
app_home = os.path.join(user_home, '.pyPDFeditor-GUI')

if not os.path.exists(app_home):
    os.makedirs(app_home)

if not os.path.exists(os.path.join(app_home, 'ico')):
    os.makedirs(os.path.join(app_home, 'ico'))
    from .icon_contents import data
    for icon_name in data:
        with open(
                os.path.join(app_home, 'ico', icon_name),
                mode='w',
                encoding='utf-8',
        ) as i:
            i.write(data[icon_name])

__system__ = platform.system()
__author__ = 'Nianze A. TAO (Omozawa SUENO)'
__version__ = '2.0.3'
__all__ = ['__main__', '__system__', '__version__']
# --------------完成！2021年八月十日に--------------
