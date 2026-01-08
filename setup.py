# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
set up the application
"""
import os
import re
from pathlib import Path
from shutil import rmtree
from setuptools import setup

init_file = Path("pypdfeditor_core") / "__init__.py"

with open(init_file, mode="r", encoding="utf-8") as fh:
    lines = fh.readlines()
    for line in lines:
        if "__version__" in line:
            version = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+", line)
            if len(version) != 0:
                version = version[0]
                print("version:", version)
                break

with open("README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()

long_description = long_description.replace(
    '## Screenshot 🎞️\n\non Windows 11:\n\n<img src="./screenshots/tab2.png" width="400" alt="tab2 win11"/>',
    "",
)

setup(
    name="pyPDFeditor-GUI",
    version=version,
    description="A desktop application to edit PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nianze A. TAO",
    author_email="Augus_1999@outlook.com",
    packages=["pypdfeditor_core", "pypdfeditor_core.icons"],
    package_dir={
        "pypdfeditor_core": "pypdfeditor_core",
        "pypdfeditor_core.icons": "pypdfeditor_core/icons",
    },
    license="MIT",
    python_requires=">=3.10",
    install_requires=["PyMuPDF>=1.26.5,<1.28.0", "PyQt6>=6.7.0"],
    url="https://github.com/Augus1999/pyPDFeditor-GUI/",
    project_urls={"Source": "https://github.com/Augus1999/pyPDFeditor-GUI"},
    include_package_data=True,
    package_data={"pypdfeditor_core": ["icons/*.svg", "icons/*.py"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English",
        "Natural Language :: Japanese",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business",
    ],
    entry_points={"gui_scripts": ["pdfeditor=pypdfeditor_core:main"]},
)

if os.path.exists("build"):
    rmtree("build")
if os.path.exists("pyPDFeditor_GUI.egg-info"):
    rmtree("pyPDFeditor_GUI.egg-info")  # remove egg-info dir
