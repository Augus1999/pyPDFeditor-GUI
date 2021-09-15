# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
from PyQt5 import QtWidgets

TAB_L = {
    "English": ['     Merge PDF    ', '    Organise    ', '    Security    ', '    Metadata    '],
    "中文": ['    合并文檔    ', '    分割頁面    ', '    檔案保護    ', '    元數據    '],
    "日本語": ['ファイル結合', 'ページオルガナイズ', '電子透かし', 'メタデータ']
}
TIP_L = {
    "English": ['Open', 'Save', 'Settings', 'Clean', 'about', 'change view', 'colours', 'preview', 'more', 'font'],
    "中文": ['開啓檔案', '保存', '設定', '清除', '關於本程式', '改變視圖', '顔色', '預覽', '更多', '字體'],
    "日本語": ['開く', '保存', '設定', '全て閉じる', 'バージョン情報', 'ビュー転換', '色選ぶ', 'プレビュー', '詳細設定', '字体']
}
LAB_L3 = {
    "English": ['PASSWORD', 'WATERMARK', 'Font Size:', 'Open after saving',
                'Opacity:', 'Rotation:', 'Preview Mode', 'Edit Restriction'],
    "中文": ['密碼', '水印', '字號：', '保存後開啓', '透明度：', '旋轉：', '預覽模式', '限制編輯'],
    "日本語": ['パスワード', '電子透かし', 'フォントサイズ：', '保存してから開く',
            '不透明度：', '回転：', 'プレビューモード', '編集制限']
}
LAB_L4 = {
    "English": ['Title', 'Author', 'Subject', 'Keywords'],
    "中文": ['題目', '作者', '主題', '關鍵詞'],
    "日本語": ['タイトル', '作者', '主題', 'キーワード']
}
LINE_L = {
    "English": ['    user password here',
                '    owner password here',
                '''
    Catalogue edit here
    e.g.

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        '''],
    "中文": ['    使用者密碼',
           '    所有者密碼',
           '''
    在此處編輯目錄
    例如：

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        '''],
    "日本語": ['    使用者のパスワード',
            '    所有者のパスワード',
            '''
    此処に目録を編集
    例は以下の通り

    *-->chapter 1-->1
    **-->section 1-->1
    **-->section 2-->5
    *-->chapter 2-->17
        ''']
}


def set_language(widget: QtWidgets.QWidget) -> None:
    """
    set language

    :param widget: QWidget -> self
    :return: None
    """
    widget.setTabToolTip(0, TAB_L[widget.language][0])
    widget.setTabToolTip(1, TAB_L[widget.language][1])
    widget.setTabToolTip(2, TAB_L[widget.language][2])
    widget.setTabToolTip(3, TAB_L[widget.language][3])
    widget.tab1.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab1.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab1.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab1.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab1.button5.setToolTip(TIP_L[widget.language][4])
    widget.tab2.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab2.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab2.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab2.button4.setToolTip(TIP_L[widget.language][3])
    widget.tab2.button5.setToolTip(TIP_L[widget.language][5])
    widget.tab3.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab3.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab3.button3.setToolTip(TIP_L[widget.language][2])
    widget.tab3.button4.setToolTip(TIP_L[widget.language][6])
    widget.tab3.button5.setToolTip(TIP_L[widget.language][7])
    widget.tab3.button6.setToolTip(TIP_L[widget.language][8])
    widget.tab3.button7.setToolTip(TIP_L[widget.language][9])
    widget.tab4.button1.setToolTip(TIP_L[widget.language][0])
    widget.tab4.button2.setToolTip(TIP_L[widget.language][1])
    widget.tab3.label1.setText('. ' * 9 + LAB_L3[widget.language][0] + ' .' * 9)
    widget.tab3.label2.setText('. ' * 8 + LAB_L3[widget.language][1] + ' .' * 8)
    widget.tab3.label4.setText(LAB_L3[widget.language][2])
    widget.tab3.label5.setText(LAB_L3[widget.language][3])
    widget.tab3.label7.setText(LAB_L3[widget.language][4])
    widget.tab3.label9.setText(LAB_L3[widget.language][5])
    widget.tab3.label11.setText(LAB_L3[widget.language][6])
    widget.tab3.label12.setText(LAB_L3[widget.language][7])
    widget.tab4.label2.setText('.' * 10 + LAB_L4[widget.language][0] + '.' * 10)
    widget.tab4.label3.setText('.' * 10 + LAB_L4[widget.language][1] + '.' * 10)
    widget.tab4.label4.setText('.' * 10 + LAB_L4[widget.language][2] + '.' * 10)
    widget.tab4.label5.setText('.' * 10 + LAB_L4[widget.language][3] + '.' * 10)
    widget.tab3.line1.setPlaceholderText(LINE_L[widget.language][0])
    widget.tab3.line2.setPlaceholderText(LINE_L[widget.language][1])
    widget.tab4.text.setPlaceholderText(LINE_L[widget.language][2])
