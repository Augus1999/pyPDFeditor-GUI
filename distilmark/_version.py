# -*- coding: utf-8 -*-
"""Single source of truth for the package version.

Kept import-free so it can be imported from both ``distilmark/__init__.py`` and
``distilmark/app.py`` without creating a circular import, and so it resolves
correctly inside a frozen PyInstaller bundle (no file reads or installed
package metadata required).
"""
__version__ = "1.2.0"
