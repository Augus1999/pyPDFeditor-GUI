# pyPDFeditor-GUI

[![PyPI](https://img.shields.io/pypi/v/pypdfeditor-gui?color=green)](https://pypi.org/project/pypdfeditor-gui/)
![pylint](https://github.com/Augus1999/pyPDFeditor-GUI/actions/workflows/pylint.yml/badge.svg)
![black](https://img.shields.io/badge/code%20style-black-black)
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

**IMPORTANT: Development of this project has been stopped but maintenance will be continued.**

## Features

* Support 3 languages: English, 日本語 (Japanese), and 中文 (Traditional Chinese)
* Fluent UI design (Icons used can be found [🔗here](https://fluenticons.co/))
* Cross-platform support
* Open-source and free to use under MIT licence
* Frameless Window on
  Windows ([Snap Layout](https://answers.microsoft.com/en-us/windows/forum/all/how-to-use-snap-layouts-and-snap-groups-in-windows/3213a6b6-5a33-4d40-bbce-e01388a40976)
  on Windows 11 is supported)

## What's in

* Merge files no matter they are PDF files (`.pdf`), image files (`.jpg` `.png` `.jpeg` `.bmp` `.tiff` `.svg`), or
  e-book files (`.epub` `.xps` `.fb2` `.cbz`) into one PDF file📚
* (...right-click the page then) Delete pages or rearrange pages
* (...right-click the page then) Extract images from a page
* (...right-click the page then) Rotate a page
* (...right-click the page then) Save a page as a PDF file or image file (`.png` `.psd` `.ppm`)
* Add watermark (PDF only)
* (...right-click the page then) Adjust the posotion of the watermark
* Set password either user or/and owner password (PDF only)🔒
* Set permissions (PDF only)🔏
* Edit catalogue structure of the file (PDF only)📑
* Edit metadata of the file (PDF only)📝
* Convert image files or e-book files to PDF

## Requirements 🧩

```text
Python>=3.10
```

```text
PyQt6>=6.7.0
PyMuPDF>=1.26.5,<1.28.0
```

## Install & Run

### install from PyPI

```bash
$ pip install pypdfeditor-gui
```

### install from source

you will need git, `setuptools` and `wheel` installed

```bash
$ pip install git+https://github.com/Augus1999/pyPDFeditor-GUI.git
```

### build thy own package

this requires `build`, `setuptools` and `wheel` installed

```bash
$ pip install -r requirements.txt
$ python -m build
```

### Run

* `$ pdfeditor` to launch the application.

* `$ python -m pypdfeditor_core --reset` to reset the application; this will delete all settings and caches. Default
  settings will be created at next launch.

* `$ python -m pypdfeditor_core --remove` to remove the whole application.
* `$ python -m pypdfeditor_core --debug` to enable showing all mupdf errors and/or warnings.

## Screenshot 🎞️

on Windows 11:

<img src="./screenshots/tab2.png" width="400" alt="tab2 win11"/>

## Cache files

Setting and cache files are stored in the directory `C:\User\USER\.pyPDFeditor-GUI` (Windows) or `home/USER/.pyPDFeditor-GUI`
(Linux and macOS).
