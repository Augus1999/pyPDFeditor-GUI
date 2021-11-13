# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import win32api
import win32gui
from win32.lib import win32con
from ctypes import POINTER, c_int, WinDLL, Structure, byref
from ctypes.wintypes import RECT, UINT, HWND


class PWindowPOS(Structure):
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
    _fields_ = [
        ('rgrc', RECT*3),
        ('lppos', POINTER(PWindowPOS))
    ]


class MARGINS(Structure):
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
        
    @staticmethod
    def move_window(h_wnd: int) -> None:
        """
        move the window

        :param h_wnd: winID
        :return: None
        """
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            h_wnd,
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE + win32con.HTCAPTION,
            0,
        )

    @staticmethod
    def addWindowAnimation(h_wnd: int) -> None:
        """
        Windows type animation

        :param h_wnd: winID
        :return: None
        """
        style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            h_wnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )

    def addShadowEffect(self, h_wnd: int) -> None:
        """
        add shadow to the window

        :param h_wnd: winID
        :return: None
        """
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))
