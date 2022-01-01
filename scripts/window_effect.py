# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
win32api functions and classes
"""
from ctypes import POINTER, c_int, WinDLL, Structure, byref, cast
from ctypes.wintypes import RECT, UINT, HWND, MSG
from win32gui import GetWindowPlacement


class PWindowPOS(Structure):
    """
    PWindowPOS
    """
    _fields_ = [
        ('hWnd', HWND),
        ('hwndInsertAfter', HWND),
        ('x', c_int),
        ('y', c_int),
        ('cx', c_int),
        ('cy', c_int),
        ('flags', UINT)
    ]


class NCCalcSizePARAMS(Structure):
    """
    NCCalcSizePARAMS
    """
    _fields_ = [
        ('rgrc', RECT*3),
        ('lppos', POINTER(PWindowPOS))
    ]


class MARGINS(Structure):
    """
    MARGINS
    """
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


class WindowEffect:
    """
    use Windows api to re-enable Windows type window-effects
    """
    def __init__(self):
        self.dwm_api = WinDLL("dwmapi")
        self.DwmExtendFrameIntoClientArea = self.dwm_api.DwmExtendFrameIntoClientArea

    def addShadowEffect(self, h_wnd: int) -> None:
        """
        add shadow to the window
        :param h_wnd: winID
        :return: None
        """
        margins = MARGINS(-1)
        self.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))

    @staticmethod
    def monitorNCCALCSIZE(_msg: MSG, geometry) -> None:
        """
        resize the window to fit the screen
        """
        params = cast(_msg.lParam, POINTER(NCCalcSizePARAMS)).contents
        params.rgrc[0].left = geometry.x()
        params.rgrc[0].top = geometry.y()
        params.rgrc[0].right = geometry.width()
        params.rgrc[0].bottom = geometry.height()

    @staticmethod
    def isWindowMaximised(h_wnd: MSG.hWnd) -> bool:
        """
        is window maximised
        """
        window_placement = GetWindowPlacement(h_wnd)
        if not window_placement:
            return False
        return window_placement[1] == 3  # SW_MAXIMIZE
