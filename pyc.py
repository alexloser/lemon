# coding: utf-8
""" Compile python source file to pyc file """
import os, sys
import py_compile
import shutil

if len(sys.argv) < 2:
    print("Usage: python pyc.py source_dir [exclude]")
    sys.exit()

if len(sys.argv) > 2:
    exclude = [F"\\{s}\\" for s in sys.argv[2:]]
else:
    exclude = []

src_dir = os.path.realpath(sys.argv[1]).rstrip("\\/")

def path_walk(path):
    for root, _, naked in os.walk(path):
        if not root.endswith(os.sep):
            root += os.sep
        for name in naked:
            if name.endswith(".py"):
                yield root + name

release_dir = F"{src_dir}-pyc"

try:
    os.mkdir(release_dir)
except FileExistsError:
    print("Dir exists!")

print("Release:", release_dir)
print("Exclude:", exclude)


for name in path_walk(src_dir):
    ignore = False
    for d in exclude:
        if d in name:
            print(F"Ignored: {name}")
            ignore = True
            break
    if ignore:
        continue  
    cname = py_compile.compile(name, optimize=2)
    dst = cname.replace(src_dir, release_dir)
    for i in range(30, 40):
        dst = dst.replace(F".cpython-{i}.pyc", ".pyc")
        dst = dst.replace(F".cpython-{i}.opt.pyc", ".pyc")
        dst = dst.replace(F".cpython-{i}.opt-1.pyc", ".pyc")
        dst = dst.replace(F".cpython-{i}.opt-2.pyc", ".pyc")
    dst = dst.replace("__pycache__", "")
    try:
        os.makedirs(os.path.dirname(dst))
    except FileExistsError:
        pass
    shutil.copyfile(cname, dst)

