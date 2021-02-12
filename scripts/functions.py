# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import sys
import fitz
import json
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyPDF2 import PdfFileWriter, PdfFileReader


def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def render_pdf_page(page_data):
    # 图像缩放比例
    zoom_matrix = fitz.Matrix(1, 1)

    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    page_pixmap = page_data.getPixmap(matrix=zoom_matrix,
                                      alpha=False)
    # 获取 image 格式
    image_format = QtGui.QImage.Format_RGB888
    # 生成 QImage 对象
    page_image = QtGui.QImage(
        page_pixmap.samples,
        page_pixmap.width,
        page_pixmap.height,
        page_pixmap.stride,
        image_format)

    # 生成 pixmap 对象
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(page_image)
    return pixmap


def add_encryption(input_pdf, output_pdf, u_password, o_password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
    pdf_writer.encrypt(user_pwd=u_password, owner_pwd=o_password,
                       use_128bit=True)
    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)


def pdf_split(input_pdf):
    book_list = list()
    f_name = os.path.splitext(os.path.basename(input_pdf))[0]
    pdf_reader = PdfFileReader(input_pdf)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(page))
        out_file_name = 'cache\\{}-{}.pdf'.format(f_name, page)
        book_list.append(out_file_name)
        with open(out_file_name, 'wb') as f:
            pdf_writer.write(f)
    return book_list


def create_watermark(input_pdf, output_pdf, text, rotate,
                     colour, font_size, opacity=0.5):
    """PyMuPDF矩形方案"""
    doc = fitz.open(input_pdf)
    for page in doc:
        p1 = fitz.Point(page.rect.width//2-150, page.rect.height//2-150)
        shape = page.newShape()
        shape.insert_text(p1, text, rotate=rotate, color=colour, fontsize=font_size,
                          stroke_opacity=0.5, fill_opacity=opacity)
        shape.commit()
    doc.save(output_pdf)


def setting_warning(set_file_name):
    try:
        with open(set_file_name, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return content
    except FileNotFoundError:  # do this first
        QMessageBox.warning(None, 'Error', 'Cannot find '+set_file_name.split('\\')[-1],
                            QMessageBox.Yes | QMessageBox.No)
        exit()


def set_icon(f_name, widget):
    # 填充文件首页图像入对应单元格
    doc = fitz.open(f_name)  # 打开文件
    page = doc.loadPage(0)  # 加载封面
    _cover = render_pdf_page(page)  # 生成首页图像
    label = QtWidgets.QLabel(None)
    label.setScaledContents(True)  # 设置图像自动填充
    label.setPixmap(QtGui.QPixmap(_cover))  # 设置首页图像
    widget.table.setCellWidget(widget.x, widget.y, label)  # 设置单元格元素为label
    del label  # 删除label（重要）
    widget.crow, widget.col = widget.x, widget.y  # 设置当前行数与列数
    try:
        if (not widget.y % (widget.w_col-1)) and widget.y:
            # 每（self.w_col）个元素换行
            widget.x += 1
            widget.y = 0
        else:
            widget.y += 1
    except ZeroDivisionError:
        pass


def cover(words: str, widget: QWidget):
    # 填充单元格图像
    for i in range(widget.w_row):
        for j in range(widget.w_col):
            icon = QtWidgets.QTableWidgetItem(QtGui.QIcon('.\\ico\\pdf.png'), "\n"+words)
            widget.table.setItem(i, j, icon)
            del icon  # 删除icon（重要）


def add(main: QWidget, widget: QWidget):
    # 添加文件
    f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                            main.s_dir, '(*.pdf)')
    if _:
        if f_name not in widget.book_list:
            widget.book_list.append(f_name)
            set_icon(f_name, widget)
    else:
        pass


def delete(row, col, widget: QWidget):
    # 右键删除单元格文件首页图像
    index = row * widget.w_col + col  # 获取图书在列表中的位置
    widget.x = row
    widget.y = col
    if index >= 0:
        widget.book_list.pop(index)
    i, j = row, col
    while 1:
        # 移除 i 行 j 列单元格的元素
        widget.table.removeCellWidget(i, j)
        # 一直删到最后一个有元素的单元格
        if i == widget.crow and j == widget.col:
            break
        if (not j % (widget.w_col-1)) and j:
            i += 1
            j = 0
        else:
            j += 1
    if not widget.book_list:
        # 如果book_list为空，设置当前单元格为-1
        widget.crow = -1
        widget.col = -1
    for f_name in widget.book_list[index:]:
        # 删除文件后，重新按顺序显示首页图像
        cover(words='', widget=widget)
        set_icon(f_name, widget)


def generate_menu(pos, widget: QWidget):
    row_num = col_num = -1
    for i in widget.table.selectionModel().selection().indexes():
        # 获取选中的单元格的行数以及列数
        row_num = i.row()
        col_num = i.column()
    if (row_num < widget.crow) or (row_num == widget.crow and col_num <= widget.col):
        menu = QtWidgets.QMenu()  # 添加选项
        item1 = menu.addAction('delete')  # 获取选项
        action = menu.exec_(widget.table.mapToGlobal(pos))
        if action == item1:
            try:
                delete(row_num, col_num, widget)
            except IndexError:
                pass


def reset_table(book_len, widget: QWidget):
    w_row = book_len//4 + book_len % 4
    widget.w_row = w_row
    widget.table.setRowCount(widget.w_row)
    for i in range(widget.w_col):
        widget.table.setColumnWidth(i, (875 - 16) // widget.w_col)
    for i in range(widget.w_row):
        widget.table.setRowHeight(i, ((875 - 16) // widget.w_col) * 4 // 3)
    cover(words='page', widget=widget)
