# pyPDFeditor-GUI

This project is based on PyQt5 and PyMuPDF and tested on Python 3.8.6 & 3.9.7 on Windows 10.

Current version is v1.6.1

## Welcome

<img src=".\ico\pdf icon.svg" width="40" />

Welcome to use pyPDFeditor-GUI. pyPDFeditor-GUI is a simple cross-platform application, thanks to [Python](https://www.python.org/), [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) and [PyMuPDF](https://github.com/pymupdf/PyMuPDF), designed to work on simple PDF handling including merging files, organising pages, saving page as image, extracting images from page, setting passwords (user or/and owner password), and adding watermarks.

I tried my best to make it close to Fluent UI. Icons used can be found [here](https://fluenticons.co/). 

## Required Packages

Core:

```ASN.1
PyQt5>=5.15.4
PyMuPDF!=1.18.18
```

optional if running on Windows:

```ASN.1
pywin32>=301
```



## Install & Run
Run `$ pip install -r requirements.txt` to install all required packages.

Run `$ python pdfEditor.py` to open the application window.



If you are working on Windows platform and having no Python 3 installed, download pyinstaller-prepackaged executable files [here](https://github.com/Augus1999/pyPDFeditor-GUI/releases).

## Screenshot
<img src=".\screenshots\welcome.jpg" width=400 alt="welcome page">

<img src=".\screenshots\tab2.jpg" width=400 alt="tab2"/>

<img src=".\screenshots\tab3.jpg" width=400 alt="tab3"/>

## If you want to change the theme

The default Theme is written in the file `styleSheets.py` of folder `scripts`. Of course, you are welcomed to change it or create a new one. Just remember to keep the same variable names and same formats, especially the format of `SWITCH_STYLE` item, or you may well encounter errors : ) If you create a new theme, then put it into folder `scripts`, go to line 4 of `windows.py` and change:

```python
from .styleSheets import *
```

into `from YOUR_STYLESHEETS import *` for instance:

```python
from .styleSheets_yurucamp_shimaRIN import *
```

 You are also welcomed to share your themes [here](https://github.com/Augus1999/pyPDFeditor-GUI/pulls).

## Others

I wrote this scripts as robust as possible. If you encountered any crash and could not see any error from PyQt and python itself, open the python file `pdfEditor.py` in IDE, find line 8, change the state `debug=False` into `debug=True`, and run the application again. Then you will see all mupdf errors (and warnings) in terminal. Please report these errors to [Issues](https://github.com/Augus1999/pyPDFeditor-GUI/issues). Thank you!

