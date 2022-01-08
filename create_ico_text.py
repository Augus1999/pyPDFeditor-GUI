# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
create icon_contents.py file
"""
import re
import os

ico_home = 'icons'
end = '.svg'
files = {}

for _, __, file_names in os.walk(ico_home):
    for file_name in file_names:
        if file_name.endswith(end):
            with open(os.path.join(ico_home, file_name)) as f:
                data = f.read()
            files[file_name] = re.sub(r'\s+', ' ', data)

print(files)

with open('pypdfeditor_core/icon_contents.py', 'w', encoding='utf-8') as fh:
    fh.write("data="+str(files))
