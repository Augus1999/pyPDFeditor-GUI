# -*- coding: utf-8 -*-
# ! Python
# Author: Nianze A. TAO
import os

for root, _, files in os.walk('cache'):
    for name in files:
        if name.endswith('.pdf'):
            os.remove(os.path.join(root, name))
