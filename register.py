#!/usr/bin/env python
# import pandoc
import os
# module for converting markdown to whatever it is that pypi uses
import pypandoc
import platform

path_choices = {
    "Windows": r"C:\Program Files (x86)\Pandoc\pandoc.exe",
    "Linux": r'/usr/bin/pandoc'
}

os.environ.setdefault('PYPANDOC_PANDOC', path_choices[platform.system()])
output = pypandoc.convert("README.md","rst", outputfile="README.txt")
print(output)
# with open('README.txt', 'w') as f:
#     f.write(output)
os.system("python3 setup.py register")
# print(output)
