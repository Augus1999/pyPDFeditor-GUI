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
    '<img src="./screenshots/tab2.png" width="400" alt="tab2 win11"/>',
    '<img src="https://user-images.githubusercontent.com/39725660/149351062-323c8688-9739-4072-b070-d6c15bd7dbd8.png"'
    ' width="400" alt="tab2 win11"/>',
)

setup(
    name="pyPDFeditor-GUI",
    version=version,
    description="A desktop application to edit PDF files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nianze A. TAO",
    author_email="Augus_1999@outlook.com",
    packages=["pypdfeditor_core"],
    package_dir={"pypdfeditor_core": "pypdfeditor_core"},
    license="MIT",
    python_requires=">=3.7",
    install_requires=["PyMuPDF>=1.19.2", "PyQt5>=5.15.4"],
    url="https://github.com/Augus1999/pyPDFeditor-GUI/",
    project_urls={"Source": "https://github.com/Augus1999/pyPDFeditor-GUI"},
    include_package_data=True,
    package_data={"pypdfeditor_core": ["icons/*.svg", "icons/*.py"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: English",
        "Natural Language :: Japanese",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
    ],
    entry_points={"console_scripts": ["pdfeditor=pypdfeditor_core:main"]},
)

if os.path.exists("build"):
    rmtree("build")
if os.path.exists("pyPDFeditor_GUI.egg-info"):
    rmtree("pyPDFeditor_GUI.egg-info")  # remove egg-info dir
