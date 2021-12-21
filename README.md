# pyPDFeditor-GUI 

This project is based on PyQt5 and PyMuPDF and tested on Python 3.8.6 & 3.9.7 on Windows 10 & 11.

Current version is v2.0.1 ⌛

## Welcome 🎃🎉

Welcome to use pyPDFeditor-GUI. pyPDFeditor-GUI is a simple cross-platform application, thanks
to [Python](https://www.python.org/), [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
and [PyMuPDF](https://github.com/pymupdf/PyMuPDF), designed to work on simple PDF handling.

I tried my best to make it close to Fluent UI. Icons used can be found [🔗here](https://fluenticons.co/).

## Features

* Support 3 languages: English, 日本語 (Japanese), and 中文 (Traditional Chinese)
* Fluent UI design
* Cross-platform support
* Open-source and free to use under MIT licence

## What's in

* Merge files no matter they are PDF files (`.pdf`), image files (`.jpg` `.png` `.jpeg` `.bmp` `.tiff` `.svg`), or
  e-book files (`.epub` `.xps` `.fb2` `.cbz`) into one PDF file📚
* (...right-click the page then) Delete pages or rearrange pages
* (...right-click the page then) Extract images from a page
* (...right-click the page then) Rotate a page
* (...right-click the page then) Save a page as a PDF file or image file (`.png` `.psd` `.ppm`)
* Add watermark (PDF only)
* Set password either user or/and owner password (PDF only)🔒
* Set permissions (PDF only)🔏
* Edit catalogue structure of the file (PDF only)📑
* Edit metadata of the file (PDF only)📝
* Convert image files or e-book files to PDF

## Required Packages 🧩

Core:

```ASN.1
PyQt5>=5.15.4
PyMuPDF>=1.19.2
```

optional if running on Windows:

```ASN.1
pywin32>=301
```

## Install & Run

Run `$ pip install -r requirements.txt` to install all required packages.

Run `$ python pdfEditor.py` to open the application window.

If you are working on Windows platform and having no Python 3 installed, download pyinstaller-prepackaged executable
files [here](https://github.com/Augus1999/pyPDFeditor-GUI/releases).

### Using on Windows

[Snap Layout Menu](https://docs.microsoft.com/zh-cn/windows/apps/desktop/modernize/apply-snap-layout-menu) in
Windows 11 is fully supported.

## Screenshot 🎞️

on Windows 11:

![tab2 win11](./screenshots/tab2.png)

## Others

I wrote this scripts as robust as possible. If you encountered any crash and could not see any error from PyQt and
python itself, open the python file [`📄pdfEditor.py`](pdfEditor.py) in IDE, find <u>line 10</u>, change the
state `debug=False` into `debug=True`, and run the application again. Then you will see all mupdf errors (and warnings)
in terminal. Please report these errors to [Issues](https://github.com/Augus1999/pyPDFeditor-GUI/issues). Thank you!
