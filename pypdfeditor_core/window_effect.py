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
        ("hWnd", HWND),
        ("hwndInsertAfter", HWND),
        ("x", c_int),
        ("y", c_int),
        ("cx", c_int),
        ("cy", c_int),
        ("flags", UINT),
    ]


class NCCalcSizePARAMS(Structure):
    """
    NCCalcSizePARAMS
    """

    _fields_ = [("rgrc", RECT * 3), ("lppos", POINTER(PWindowPOS))]


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

    def add_shadow_effect(self, h_wnd: int) -> None:
        """
        add shadow to the window (extend the client area)

        :param h_wnd: window ID
        :return: None
        """
        margins = MARGINS(-1)
        self._extend(h_wnd, byref(margins))

    @staticmethod
    def monitorNCCALCSIZE(_msg: MSG, geometry) -> None:
        """
        resize the window to fit the screen

        :param _msg: MSG
        :param geometry: QRect() object
        :return: None
        """
        params = cast(_msg.lParam, POINTER(NCCalcSizePARAMS)).contents
        params.rgrc[0].left = geometry.x()
        params.rgrc[0].top = geometry.y()
        params.rgrc[0].right = geometry.width()
        params.rgrc[0].bottom = (
            geometry.height() - 1
        )  # enable to show taskbar when it is set to auto-hide

    def add_window_style(self, h_wnd: int) -> None:
        """
        add native window behaviour

        :param h_wnd: window ID
        :return: None
        """
        style = self._GetWindowLong(h_wnd, -16)
        self._SetWindowLong(
            h_wnd,
            -16,  # GWL_STYLE
            style
            | 0x00C00000
            | 0x00010000  # WS_CAPTION
            | 0x00020000  # WS_MAXIMIZEBOX
            | 0x0008  # WS_MINIMIZEBOX
            | 0x00040000  # CS_DBLCLKS
            | 0x00080000,  # WS_SIZEBOX  # WS_SYSMENU
        )

    def move_window(self, h_wnd: int) -> None:
        """
        send message to system the window is moving

        :param h_wnd: window ID
        :return: None
        """
        self._user32.ReleaseCapture()
        self._SendMessage(
            h_wnd,
            0x0112,  # WM_SYSCOMMAND
            0xF010 + 2,  # SC_MOVE + HTCAPTION
            0,
        )

    def screen_change(self, h_wnd: int) -> None:
        """
        reset window position after screen changed;
        this method probably can solve displaying problem
        after moving into another screen with different dpi

        :param h_wnd: window ID
        :return: None
        """
        self._user32.SetWindowPos(
            h_wnd,
            None,
            0,
            0,
            0,
            0,  # left top right bottom
            0x0002 | 0x0001 | 0x0020,  # SWP_NOMOVE  # SWP_NOSIZE  # SWP_FRAMECHANGED
        )
