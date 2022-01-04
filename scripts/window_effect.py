# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
win32api functions and classes
"""
from ctypes import POINTER, c_int, WinDLL, Structure, byref, cast
from ctypes.wintypes import RECT, UINT, HWND, MSG


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
        self._dwm_api = WinDLL("dwmapi")
        self._user32 = WinDLL("user32")
        self._extend = self._dwm_api.DwmExtendFrameIntoClientArea
        self._GetWindowLong = self._user32.GetWindowLongA
        self._SetWindowLong = self._user32.SetWindowLongA
        self._SendMessage = self._user32.SendMessageA
        self.isMaximised = self._user32.IsZoomed

    def addShadowEffect(self, h_wnd: int) -> None:
        """
        add shadow to the window
        :param h_wnd: winID
        :return: None
        """
        margins = MARGINS(-1)
        self._extend(h_wnd, byref(margins))

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

    def addWindowStyle(self, h_wnd: int) -> None:
        style = self._GetWindowLong(h_wnd, -16)
        self._SetWindowLong(
            h_wnd,
            -16,  # GWL_STYLE
            style |
            0x00C00000 |  # WS_CAPTION
            0x00010000 |  # WS_MAXIMIZEBOX
            0x00020000 |  # WS_MINIMIZEBOX
            0x0008 |  # CS_DBLCLKS
            0x00040000 |  # WS_SIZEBOX
            0x00080000,  # WS_SYSMENU
        )

    def move_window(self, h_wnd: int) -> None:
        self._user32.ReleaseCapture()
        self._SendMessage(
            h_wnd,
            0x0112,  # WM_SYSCOMMAND
            0xF010 + 2,  # SC_MOVE + HTCAPTION
            0,
        )
