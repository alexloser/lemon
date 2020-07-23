#!python
# coding: utf-8
""" Get file's MD5 value """
from runtime import *

for name in ListDir(sys.argv[1]):
    if IsDir(name):
        continue
    val = FileMD5(name)    
    print("%-16s %s" % (Basename(name), val.upper()))


