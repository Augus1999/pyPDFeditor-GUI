# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
set up the application
"""
from setuptools import setup

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

long_description = long_description.replace(
    '<img src="./screenshots/tab2.png" width="400" alt="tab2 win11"/>',
    '![tab2 win11](https://github.com/Augus1999/pyPDFeditor-GUI/blob/main/screenshots/tab2.png)',
)

setup(
    name="pyPDFeditor-GUI",
    version="2.0.2",
    description="A desktop application to edit PDF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nianze A. TAO",
    author_email="Augus_1999@outlook.com",
    packages=["pypdfeditor_core"],
    package_dir={"pypdfeditor_core": "pypdfeditor_core"},
    scripts=["pdfEditor.pyw"],
    script_name="pdfEditor",
    license="MIT",
    python_requires='>=3.7',
    install_requires=["PyMuPDF>=1.19.2", "PyQt5>=5.15.4"],
    url="https://github.com/Augus1999/pyPDFeditor-GUI",
)
