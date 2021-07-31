# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
import os
import fitz
import json
import time
from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets,
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QWidget,
)
# Attention: ignore all warnings in fitz.open(.)


def open_pdf(file_name: str):
    """
    :param file_name: pdf file name
    :return (doc, bool)
    """
    try:
        doc = fitz.open(file_name)
        if doc.needsPass:
            QMessageBox.critical(
                None,
                'Error',
                'Cannot open an encrypted file.',
                QMessageBox.Yes | QMessageBox.No,
            )
            doc.close()
            del doc
            return None, False
        else:
            return doc, True
    except RuntimeError:
        QMessageBox.critical(
            None,
            'Error',
            ' Format error:\n cannot open this file',
            QMessageBox.Yes | QMessageBox.No,
        )
        return None, False


def render_pdf_page(page_data):
    """
    render PDF page

    :param page_data: page data
    :return: a QPixmap
    """
    page_pixmap = page_data.get_pixmap(
        matrix=fitz.Matrix(1.0, 1.0),
        clip=True,
    )
    if page_pixmap.alpha:
        image_format = QtGui.QImage.Format_RGBA8888
    else:
        image_format = QtGui.QImage.Format_RGB888
    page_image = QtGui.QImage(
        page_pixmap.samples,
        page_pixmap.width,
        page_pixmap.height,
        page_pixmap.stride,
        image_format,
    )
    pixmap = QtGui.QPixmap()
    pixmap.convertFromImage(page_image)
    del page_pixmap
    return pixmap


def pdf_split(doc: fitz.fitz):
    """
    split the selected PDF file into pages;

    :param doc: target PDF file to be split
    :return: book_list
    """
    book_list = list()
    for page in range(doc.pageCount):
        book_list.append(page)
    return book_list


def security(input_pdf: str,
             output_pdf: (str, None,),
             text: str,
             rotate: int,
             colour: tuple,
             font_size: int,
             font_file: str,
             perm: int = 0,
             opacity=0.5,
             owner_pass='',
             user_pass='',
             save=True,
             select=None):
    """
    add password and/or watermark

    :param input_pdf: import file name
    :param output_pdf: export file name
    :param text: content of watermark
    :param rotate: rotation angle of watermark
    :param colour: colour of watermark; in form of (a, b, c,)
    :param font_size: font size of letter in watermark
    :param font_file: font file location
    :param perm: int; set permissions
    :param opacity: opacity of the watermark; range from 0 to 100
    :param owner_pass: owner password
    :param user_pass: user password
    :param save: bool, whether save or return doc
    :param select: None or int;
    :return: None if save==True; fitz.doc if save==False
    """
    encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm
    doc = fitz.open(input_pdf)
    if select is not None:
        doc.select([select])
    for page in doc:
        r1 = fitz.Rect(
            10,
            10,
            page.rect.width-10,
            page.rect.height-10,
        )
        pos0 = fitz.Point(
            page.rect.width//2,
            page.rect.height//2,
        )
        shape = page.newShape()
        shape.insertTextbox(
            r1,
            text,
            rotate=0,
            color=colour,
            fontsize=font_size,
            stroke_opacity=0.5,
            fill_opacity=opacity,
            align=1,
            fontfile=font_file,
            fontname="EXT_0",
            morph=(
                pos0,
                fitz.Matrix(rotate)
            ),
        )
        shape.commit()
    if not save:
        return doc
    if save:
        doc.save(
            output_pdf,
            garbage=1,  # remove unused objects
            encryption=encrypt_meth,  # set the encryption method
            owner_pw=owner_pass,  # set the owner password
            user_pw=user_pass,  # set the user password
            permissions=perm,  # set permissions
        )
        doc.close()
        del doc


def setting_warning(set_file_name: str):
    """
    import settings in JSON file

    :param set_file_name: JSON file name
    :return: a dict loaded from JSON file
    """
    try:
        with open(
                set_file_name,
                'r',
                encoding='utf-8',
        ) as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        QMessageBox.warning(
            None,
            'Error',
            'Cannot find '+set_file_name.split('\\')[-1],
            QMessageBox.Yes | QMessageBox.No,
        )
        exit()


def set_icon(doc: fitz.fitz,
             widget: QWidget.window,
             _page: int = 0):
    """
    add image of first page into table element

    :param doc: from open_pdf(.)
    :param widget: widget
    :param _page: page index
    :return: None
    """
    page = doc.loadPage(_page)
    _cover = render_pdf_page(page)
    label = QtWidgets.QLabel(None)
    scaled_width, scaled_height = int, int
    if _cover.height()/_cover.width() > 4/3:
        scaled_height = (widget.table.width()-15)//widget.w_col*4/3-5
        scaled_width = scaled_height*(_cover.width()/_cover.height())
    if _cover.height()/_cover.width() <= 4/3:
        scaled_width = (widget.table.width()-15)//widget.w_col-5
        scaled_height = scaled_width*(_cover.height()/_cover.width())
    label.setPixmap(
        QtGui.QPixmap(_cover).scaled(
            scaled_width,
            scaled_height,
            QtCore.Qt.IgnoreAspectRatio,
            QtCore.Qt.SmoothTransformation,
        ),
    )
    label.setAlignment(
        QtCore.Qt.AlignCenter,
    )
    # print(widget.x, widget.y)
    widget.table.setCellWidget(
        widget.x,
        widget.y,
        label,
    )
    del label  # delete label (important)
    del _cover, scaled_width, scaled_height
    # do not change the following codes
    # --------------------------------------------------------------
    if ((widget.x+1)*(widget.y+1))//((widget.x+1)*widget.w_col) == 0:
        widget.y += 1
    else:
        widget.x += 1
        widget.y -= (widget.w_col-1)
    # --------------------------------------------------------------
    # doc.close()
    # del doc


def add(main: QWidget,
        widget: QWidget):
    """
    add a file

    :param main: main widget
    :param widget: widget
    :return: None
    """
    f_name, _ = QFileDialog.getOpenFileName(
        None,
        'Open files',
        main.s_dir,
        '(*.pdf)',
    )
    if _ and (f_name not in widget.book_list):
        doc, state = open_pdf(file_name=f_name)
        if state:
            set_icon(
                doc=doc,
                widget=widget,
            )
            widget.book_list.append(f_name)
        else:
            pass
        del doc
    else:
        pass


def delete(index: int,
           widget: QWidget):
    """
    delete select file/page

    :param index: position index
    :param widget: widget
    :return: None
    """
    if index >= 0:
        widget.book_list.pop(index)
    widget.table.clearContents()
    widget.x, widget.y = 0, 0
    if len(widget.book_list) != 0:
        reset_table(
            book_len=len(widget.book_list),
            widget=widget,
        )
        # reset images
        if type(widget.book_list[0]) == int:
            doc = fitz.open(widget.book_name)
            for page in widget.book_list:
                set_icon(
                    doc=doc,
                    widget=widget,
                    _page=page,
                )
            doc.close()
            del doc
        else:
            for f_name in widget.book_list:
                doc = fitz.open(f_name)
                set_icon(doc, widget)
                doc.close()
                del doc


def generate_menu(pos,
                  widget: QWidget,
                  select: int = 0,
                  main=None):
    """
    generate menu

    :param pos: position
    :param select: select=0 => only delete;
                   select=1 => with save as
    :param widget: widget
    :param main: main
    :return: None
    """
    row_num = col_num = -1
    for i in widget.table.selectionModel().selection().indexes():
        row_num = i.row()
        col_num = i.column()
    index = row_num * widget.w_col + col_num  # get position
    if 0 <= index < len(widget.book_list):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction(
            QtGui.QIcon('ico\\clean.png'),
            'delete',
        )
        item2, item3, item4 = None, None, None
        if select == 0:
            item3 = menu.addAction(
                QtGui.QIcon('ico\\view.png'),
                'view',
            )
        if select == 1:
            item2 = menu.addAction(
                QtGui.QIcon('ico\\disk.png'),
                'save as',
            )
            item4 = menu.addAction(
                QtGui.QIcon('ico\\img.png'),
                'extract images',
            )
        action = menu.exec_(
            widget.table.mapToGlobal(pos),
        )
        if action == item1:
            try:
                delete(
                    index=index,
                    widget=widget,
                )
            except IndexError:
                pass
        if action == item2 and select == 1:
            try:
                save_as(
                    index=index,
                    widget=widget,
                    main=main,
                )
            except IndexError:
                pass
        if action == item4 and select == 1:
            extract_img(
                index=index,
                widget=widget,
                main=main,
            )
        if action == item3 and select == 0 and main is not None:
            main.view(index, widget)


def reset_table(book_len: int,
                widget: QWidget):
    """
    reset the table element

    :param book_len: length of book_list
    :param widget: widget
    :return: None
    """
    if book_len % widget.w_col == 0:
        w_row = book_len//widget.w_col
    else:
        w_row = book_len//widget.w_col + 1
    widget.w_row = w_row
    widget.table.setRowCount(widget.w_row)
    for i in range(widget.w_col):
        widget.table.setColumnWidth(
            i,
            (widget.table.width()-15)//widget.w_col,
        )
    for i in range(widget.w_row):
        widget.table.setRowHeight(
            i,
            ((widget.table.width()-15)//widget.w_col)*4//3,
        )


def save_as(index: int,
            widget: QWidget,
            main: QWidget):
    """
    save the selected page as PDF file

    :param index: position index
    :param widget: widget
    :param main: main
    :return: None
    """
    doc = fitz.open(widget.book_name)
    f_name = os.path.splitext(
        os.path.basename(widget.book_name),
    )[0]+'-{}.pdf'.format(
        widget.book_list[index]+1,
    )
    file_name, ok = QFileDialog.getSaveFileName(
        None,
        "save",
        main.o_dir + f_name,
        "PDF file (*.pdf);;images (*.png *.jpg)",
    )
    if ok:
        if file_name.endswith('.pdf'):
            doc.select([widget.book_list[index]])
            doc.save(file_name.replace('/', '\\'))
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            pix = doc[index].get_pixmap(
                matrix=fitz.Matrix(1.0, 1.0),
                alpha=False,
            )
            pix.writePNG(file_name.replace('/', '\\'))
    doc.close()


def clean(widget: QWidget):
    """

    :param widget: widget
    :return: None
    """
    widget.book_list = list()
    widget.x, widget.y = 0, 0
    widget.col, widget.crow = -1, -1
    widget.table.clearContents()
    reset_table(
        book_len=1,
        widget=widget,
    )


def extract_img(index: int,
                widget: QWidget,
                main: QWidget):
    """
    extract images from pdf page.

    :param index: page index
    :param widget: widget
    :param main: main
    :return: None
    """
    doc = fitz.open(widget.book_name)
    img_inf = doc[index].get_images()
    for key, inf in enumerate(img_inf):
        f_name = os.path.splitext(
            os.path.basename(widget.book_name),
        )[0] + '-{}-{}.png'.format(
            widget.book_list[index] + 1,
            key + 1,
        )
        img_name = main.s_dir+'\\'+f_name
        # xref is inf[0]
        img = fitz.Pixmap(
            doc,
            inf[0],
        )
        # ignore the warning here
        img.writePNG(img_name)
    QMessageBox.information(
        None,
        'Saved',
        '{} images saved to {}'.format(
            len(img_inf),
            main.s_dir,
        ),
        QMessageBox.Yes | QMessageBox.No,
    )


def choose(widget: QWidget,
           c_dir: str):
    """

    :param widget: widget
    :param c_dir: from where to choose
    :return: None
    """
    root = QFileDialog.getExistingDirectory(
        None,
        "choose",
        c_dir,
    )
    if len(root) != 0:
        widget.setText(
            root.replace('/', '\\'),
        )


def set_metadata0(doc: fitz.open,
                  author: (str, None)):
    """
    set defeat metadata

    :param doc: fitz Document
    :param author: str or None
    :return: None
    """
    _time = time.localtime(time.time())
    metadata = doc.metadata
    metadata["producer"] = "pyPDFEditor-GUI"
    metadata["modDate"] = "D:{}{}{}{}{}{}".format(
        _time[0],
        str(_time[1]).zfill(2),
        str(_time[2]).zfill(2),
        str(_time[3]).zfill(2),
        str(_time[4]).zfill(2),
        str(_time[5]).zfill(2),
    )
    if author is not None:
        metadata["author"] = author
    doc.set_metadata(metadata)


def set_metadata1(metadata: dict,
                  title: str,
                  author: str,
                  subject: str,
                  keywords: str):
    """
    set metadata to pdf document

    :return: a dict -> metadata
    """
    _time = time.localtime(time.time())
    metadata["producer"] = "pyPDFEditor-GUI"
    metadata["modDate"] = "D:{}{}{}{}{}{}".format(
        _time[0],
        str(_time[1]).zfill(2),
        str(_time[2]).zfill(2),
        str(_time[3]).zfill(2),
        str(_time[4]).zfill(2),
        str(_time[5]).zfill(2),
    )
    metadata["title"] = title
    metadata["author"] = author
    metadata["subject"] = subject
    metadata["keywords"] = keywords
    return metadata


def toc2plaintext(toc: list):
    """
    :param toc: table of content <- DOCUMENT.get_toc()
    :return: plaintext
    """
    plaintext = ''
    for content in toc:
        head = '{}-->{}-->{}\n'.format(
            int(content[0])*'*',
            content[1],
            content[2],
        )
        plaintext += head
    return plaintext


def plaintext2toc(plaintext: str):
    """
    :param plaintext: plaintext
    :return: table of content -> DOCUMENT.get_toc()
    """
    toc = list()
    contents = plaintext.split('\n')
    for content in contents:
        if len(content) != 0:
            c = content.split('-->')
            t = list()
            t.append(len(c[0]))
            t.append(c[1])
            t.append(int(c[2]))
            toc.append(t)
    return toc
