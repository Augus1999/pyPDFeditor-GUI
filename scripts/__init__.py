# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
initialise the module
"""
import platform
from .application import __main__


_system = platform.system()
if _system == 'Windows':
    try:
        import win32
        __system__ = _system
    except ImportError:
        __system__ = 'Windows without pywin32'
        print('WARNING: \"pywin32\" is not installed on your computer')
else:
    __system__ = _system

__author__ = 'Nianze A. TAO (Omozawa SUENO)'
__version__ = 'v2.0.1'
__all__ = ['__main__', '__system__', '__version__']
# --------------完成！2021年八月十日に--------------
