# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
call pypdfeditor_core.main and others
"""
import sys
from argparse import ArgumentParser
from pypdfeditor_core import main, reset, remove


if __name__ == '__main__':
    parser = ArgumentParser(description="pyPDFeditor-GUI")
    parser.add_argument('--reset', action='store_true',
                        help='only remove all settings, caches and icons; '
                             'default settings and icons will be created at next launch')
    parser.add_argument('--remove', action='store_true',
                        help='remove the whole application')
    args = parser.parse_args()
    if args.reset and args.remove:
        print('reset or remove?')
        sys.exit(0)
    if args.reset:
        reset()
        sys.exit(0)
    if args.remove:
        remove()
        print('removed successfully')
        sys.exit(0)
    main()
