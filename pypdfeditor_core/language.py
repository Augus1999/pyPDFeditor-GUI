# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
language related functions
"""
from PyQt5 import QtWidgets

TAB_L = {
    "English": [
        "     Merge PDF    ",
        "    Organise    ",
        "    Security    ",
        "    Metadata    ",
    ],
    "中文": ["    合并文檔    ", "    分割頁面    ", "    檔案保護    ", "    元數據    "],
    "日本語": ["ファイル結合", "ページオルガナイズ", "電子透かし", "メタデータ"],
}
TIP_L = {
    "English": [
        "Open",
        "Save",
        "Settings",
        "Clean",
        "colours",
        "preview",
        "more",
        "font",
        "update font",
    ],
    "中文": ["開啓檔案", "保存", "設定", "清除", "顔色", "預覽", "更多", "字體", "更新字體庫"],
    "日本語": ["開く", "保存する", "設定", "全て閉じる", "色選ぶ", "プレビュー", "詳細設定", "字体", "字体を更新"],
}
LAB_L3 = {
    "English": [
        "PASSWORD",
        "WATERMARK",
        "Font Size:",
        "Open after saving",
        "Opacity:",
        "Rotation:",
        "Preview Mode",
        "Edit Restriction",
    ],
    "中文": ["密碼", "水印", "字號：", "保存後開啓", "透明度：", "旋轉：", "預覽模式", "限制編輯"],
    "日本語": [
        "パスワード",
        "電子透かし",
        "フォントサイズ：",
        "保存してから開く",
        "不透明度：",
        "回転：",
        "プレビューモード",
        "編集制限",
    ],
}
LAB_L4 = {
    "English": ["Title", "Author", "Subject", "Keywords"],
    "中文": ["題目", "作者", "主題", "關鍵詞"],
    "日本語": ["タイトル", "作者", "主題", "キーワード"],
}
LAB_LS = {
    "English": ["START DIR", "SAVE DIR", "OPEN AS PREVIOUS"],
    "中文": ["開啓路徑", "保存路徑", "記住先前的路徑"],
    "日本語": ["開くルーチング", "保存するルーチング", "前使ったルーチングを覚える"],
}
LAB_LP = {
    "English": [
        "Enable Print",
        "Enable Modifying File",
        "Enable Copy",
        "Enable Adding Annotations",
        "Enable Filling in Form",
        "Enable Accessing Adjuvant Contents",
        "Enable Page Editing",
        "Enable HD Print",
    ],
    "中文": [
        "允許列印",
        "允許修改内容",
        "允許複製内容",
        "允許添加注釋",
        "允許填充表單字節",
        "允許辅助功能的内容複製",
        "允許頁面重排",
        "允許高清列印",
    ],
    "日本語": [
        "プリントを許可にする",
        "ファイルの変更を許可にする",
        "コピーを許可にする",
        "注釈の追加を許可にする",
        "フォームへの入力を許可にする",
        "助コンテンツのアクセスを許可にする",
        "ページ編集を許可にする",
        "HDプリントを許可にする",
    ],
}
MENU_L = {
    "English": [
        "delete",
        "view",
        "save as",
        "extract images",
        "rotate 90°",
        "rotate -90°",
        "move to",
        "set watermark position",
    ],
    "中文": [
        "刪除",
        "檢視",
        "另存新檔",
        "提取圖片",
        "旋轉90°",
        "旋轉-90°",
        "移動到",
        "設置水印位置",
    ],
    "日本語": [
        "削除",
        "ビュー",
        "名前を付けて保存",
        "イメージを出す",
        "90°を旋転する",
        "-90°を旋転する",
        "ページを移動する",
        "透かしの位置を移動する",
    ],
}
LINE_L = {
    "English": [
        "    user password here",
        "    owner password here",
        """
    Catalogue edit here
    e.g.

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
    "中文": [
        "    使用者密碼",
        "    所有者密碼",
        """
    在此處編輯目錄
    例如：

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
    "日本語": [
        "    使用者のパスワード",
        "    所有者のパスワード",
        """
    此処に目録を編集
    例は以下の通り

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        """,
    ],
}
MESSAGE = {
    "English": [
        "   Format error:\n cannot open this file",
        "{} image(s) saved to {}",
        "Cannot save! Try a new file name...",
    ],
    "中文": ["    格式錯誤：\n 無法開啓此檔案", "已保存{}張圖像至{}", "無法保存欸。請嘗試新的文檔名稱。。。"],
    "日本語": [
        "    格式エラー：\n このファイルが開けません",
        "{}幅のイメージが{}に保存されました",
        "すみません。保存できませんでした。\n 新たな名前を付けてみて下さい。。。",
    ],
}


def set_language(widget: QtWidgets.QWidget) -> None:
    """
    set language

    :param widget: QWidget -> self
    :return: None
    """
    widget.setTabToolTip(1, TAB_L[widget.language][0])
    widget.setTabToolTip(2, TAB_L[widget.language][1])
    widget.setTabToolTip(3, TAB_L[widget.language][2])
    widget.setTabToolTip(4, TAB_L[widget.language][3])
    widget.tab1.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab1.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab1.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab1.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab2.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab2.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab2.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab2.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab3.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab3.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab3.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab3.button4.setToolTip(TIP_L[widget.language][4])
    widget.tab3.button5.setToolTip(TIP_L[widget.language][5])
    widget.tab3.button6.setToolTip(TIP_L[widget.language][6])
    widget.tab3.button7.setToolTip(TIP_L[widget.language][7])
    widget.tab3.button8.setToolTip(TIP_L[widget.language][3])
    widget.tab3.button9.setToolTip(TIP_L[widget.language][8])
    widget.tab4.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab4.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab4.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab4.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab3.label1.setText(". " * 9 + LAB_L3[widget.language][0] + " ." * 9)
    widget.tab3.label2.setText(". " * 8 + LAB_L3[widget.language][1] + " ." * 8)
    widget.tab3.label4.setText(LAB_L3[widget.language][2])
    widget.tab3.label5.setText(LAB_L3[widget.language][3])
    widget.tab3.label7.setText(LAB_L3[widget.language][4])
    widget.tab3.label9.setText(LAB_L3[widget.language][5])
    widget.tab3.label11.setText(LAB_L3[widget.language][6])
    widget.tab3.label12.setText(LAB_L3[widget.language][7])
    widget.tab4.label2.setText("." * 10 + LAB_L4[widget.language][0] + "." * 10)
    widget.tab4.label3.setText("." * 10 + LAB_L4[widget.language][1] + "." * 10)
    widget.tab4.label4.setText("." * 10 + LAB_L4[widget.language][2] + "." * 10)
    widget.tab4.label5.setText("." * 10 + LAB_L4[widget.language][3] + "." * 10)
    widget.tab3.line1.setPlaceholderText(LINE_L[widget.language][0])
    widget.tab3.line2.setPlaceholderText(LINE_L[widget.language][1])
    widget.tab4.text.setPlaceholderText(LINE_L[widget.language][2])


def lag_s(parent: QtWidgets.QWidget, language: str) -> None:
    """
    set language
    """
    parent.label1.setText(LAB_LS[language][0])
    parent.label2.setText(LAB_LS[language][1])
    parent.label3.setText(LAB_LS[language][2])


def lag_p(parent: QtWidgets.QWidget, language: str) -> None:
    """
    set language
    """
    parent.label1.setText(LAB_LP[language][0])
    parent.label2.setText(LAB_LP[language][1])
    parent.label3.setText(LAB_LP[language][2])
    parent.label4.setText(LAB_LP[language][3])
    parent.label5.setText(LAB_LP[language][4])
    parent.label6.setText(LAB_LP[language][5])
    parent.label7.setText(LAB_LP[language][6])
    parent.label8.setText(LAB_LP[language][7])
