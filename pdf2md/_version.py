# -*- coding: utf-8 -*-
"""Single source of truth for the package version.

Kept import-free so it can be imported from both ``pdf2md/__init__.py`` and
``pdf2md/app.py`` without creating a circular import, and so it resolves
correctly inside a frozen PyInstaller bundle (no file reads or installed
package metadata required).
"""
__version__ = "0.5.0"
