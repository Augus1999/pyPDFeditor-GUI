# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
set up the application
"""
from shutil import rmtree
from setuptools import setup
from pypdfeditor_core import __version__

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = f.read()

long_description = long_description.replace(
    '<img src="./screenshots/tab2.png" width="400" alt="tab2 win11"/>',
    '<img src="https://user-images.githubusercontent.com/39725660/149351062-323c8688-9739-4072-b070-d6c15bd7dbd8.png" width="400" alt="tab2 win11"/>',
)

setup(
    name="pyPDFeditor-GUI",
    version=__version__,
    description="A desktop application to edit PDF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nianze A. TAO",
    author_email="Augus_1999@outlook.com",
    packages=["pypdfeditor_core"],
    package_dir={"pypdfeditor_core": "pypdfeditor_core"},
    scripts=["pdfEditor", "pdfEditor.py"],
    script_name="pdfEditor",
    license="MIT",
    python_requires='>=3.7',
    install_requires=["PyMuPDF>=1.19.2", "PyQt5>=5.15.4"],
    url="https://augus1999.github.io/pyPDFeditor-GUI/",
)
rmtree('pyPDFeditor_GUI.egg-info')  # remove egg-info dir
