# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import fitz
import json
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget


def render_pdf_page(page_data):
    """
    render PDF page

    :param page_data: page data
    :return: a QPixmap
    """
    zoom_matrix = fitz.Matrix(1, 1)
    page_pixmap = page_data.getPixmap(matrix=zoom_matrix,
                                      alpha=False)
    image_format = QtGui.QImage.Format_RGB888
    page_image = QtGui.QImage(
        page_pixmap.samples,
        page_pixmap.width,
        page_pixmap.height,
        page_pixmap.stride,
        image_format)
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(page_image)
    return pixmap


def pdf_split(input_pdf: str):
    """
    split the selected PDF file into one page a file;
    then save all into cache\\

    :param input_pdf: target PDF file to be split
    :return: book_list
    """
    book_list = list()
    f_name = os.path.splitext(os.path.basename(input_pdf))[0]
    doc0 = fitz.open(input_pdf)
    for page in range(doc0.pageCount):
        out_file_name = 'cache\\{}-{}.pdf'.format(f_name, page)
        book_list.append(out_file_name)
        doc = fitz.open(input_pdf)
        doc.select([page])
        doc.save(out_file_name)
        doc.close()
    doc0.close()
    return book_list


def security(input_pdf: str,
             output_pdf: str,
             text: str,
             rotate: int,
             colour: tuple,
             font_size: int,
             opacity=0.5,
             owner_pass='',
             user_pass=''):
    """
    add password and/or watermark

    :param input_pdf: import file name
    :param output_pdf: export file name
    :param text: content of watermark
    :param rotate: rotation angle of watermark; must be 0, 90, 180, 270, 360
    :param colour: colour of watermark; in form of (a, b, c,); all element in tuple range from 0 to 1
    :param font_size: font size of little in watermark
    :param opacity: opacity of the watermark; range from 0 to 100
    :param owner_pass: owner password
    :param user_pass: user password
    :return: None
    """
    perm = int(
        fitz.PDF_PERM_ACCESSIBILITY  # always use this
        | fitz.PDF_PERM_PRINT  # permit printing
        | fitz.PDF_PERM_COPY  # permit copying
        | fitz.PDF_PERM_ANNOTATE  # permit annotations
    )
    encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm
    doc = fitz.open(input_pdf)
    for page in doc:
        p1 = fitz.Point(page.rect.width//2-150, page.rect.height//2-150)
        shape = page.newShape()
        shape.insert_text(p1, text, rotate=rotate, color=colour, fontsize=font_size,
                          stroke_opacity=0.5, fill_opacity=opacity)
        shape.commit()
    doc.save(output_pdf,
             encryption=encrypt_meth,  # set the encryption method
             owner_pw=owner_pass,  # set the owner password
             user_pw=user_pass,  # set the user password
             permissions=perm,  # set permissions
             )
    doc.close()


def setting_warning(set_file_name: str):
    """
    import settings in JSON file

    :param set_file_name: JSON file name
    :return: a dist loaded from JSON file
    """
    try:
        with open(set_file_name, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return content
    except FileNotFoundError:  # do this first
        QMessageBox.warning(None, 'Error', 'Cannot find '+set_file_name.split('\\')[-1],
                            QMessageBox.Yes | QMessageBox.No)
        exit()


def set_icon(f_name, widget):
    """
    add image of first page into table element

    :param f_name: import file name
    :param widget: widget
    :return: None
    """
    doc = fitz.open(f_name)
    page = doc.loadPage(0)
    _cover = render_pdf_page(page)
    label = QtWidgets.QLabel(None)
    label.setScaledContents(True)
    label.setPixmap(QtGui.QPixmap(_cover))
    widget.table.setCellWidget(widget.x, widget.y, label)
    del label  # delete label (important)
    widget.crow, widget.col = widget.x, widget.y
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
    """
    add a image to table element

    :param words: word in table element
    :param widget: widget
    :return: None
    """
    for i in range(widget.w_row):
        for j in range(widget.w_col):
            icon = QtWidgets.QTableWidgetItem(QtGui.QIcon('.\\ico\\pdf.png'), "\n"+words)
            widget.table.setItem(i, j, icon)
            del icon  # delete icon (important)


def add(main: QWidget, widget: QWidget):
    """
    add a file

    :param main: main widget
    :param widget: widget
    :return: None
    """
    f_name, _ = QFileDialog.getOpenFileName(None, 'Open files',
                                            main.s_dir, '(*.pdf)')
    if _:
        if f_name not in widget.book_list:
            widget.book_list.append(f_name)
            set_icon(f_name, widget)
    else:
        pass


def delete(row, col, widget: QWidget):
    """
    delete select file/page

    :param row: row index
    :param col: column index
    :param widget: widget
    :return: None
    """
    index = row * widget.w_col + col  # get position
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
        widget.crow = -1
        widget.col = -1
    for f_name in widget.book_list[index:]:
        # reset images
        cover(words='', widget=widget)
        set_icon(f_name, widget)


def generate_menu(pos, widget: QWidget):
    """
    generate menu

    :param pos: position
    :param widget: widget
    :return: None
    """
    row_num = col_num = -1
    for i in widget.table.selectionModel().selection().indexes():
        row_num = i.row()
        col_num = i.column()
    if (row_num < widget.crow) or (row_num == widget.crow and col_num <= widget.col):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction('delete')
        action = menu.exec_(widget.table.mapToGlobal(pos))
        if action == item1:
            try:
                delete(row_num, col_num, widget)
            except IndexError:
                pass


def reset_table(book_len, widget: QWidget):
    """
    reset the table element

    :param book_len: length of book_list
    :param widget: widget
    :return: None
    """
    w_row = book_len//4 + book_len % 4
    widget.w_row = w_row
    widget.table.setRowCount(widget.w_row)
    for i in range(widget.w_col):
        widget.table.setColumnWidth(i, (875 - 16) // widget.w_col)
    for i in range(widget.w_row):
        widget.table.setRowHeight(i, ((875 - 16) // widget.w_col) * 4 // 3)
    cover(words='page', widget=widget)
