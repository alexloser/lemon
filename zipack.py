# coding: utf-8
""" Zip python files """
import zipfile, sys
from runtime import *

if len(sys.argv) < 2:
    print("Usage: python zipack.py source_dir")
    sys.exit()

srcdir = sys.argv[1]
assert IsDir(srcdir)

output = F"{Basename(srcdir)}.zip"
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
    for name in ListDir(srcdir):
        arcname = name.replace(srcdir, "")
        print("Write to zip:", name)
        zf.write(name, arcname)
print(F"\nFinished: {RealPath(output)}\n")

