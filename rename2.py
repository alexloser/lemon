# Rename image file to {blake2s}.jpg
# Put this script into samples dir with hand, mouth subdirs
import os, sys
from zlib import crc32
from hashlib import blake2s

def rename2(image_dir):
    names = os.listdir(image_dir)
    print("Process:", image_dir, len(names))
    n = 0
    for name in names:
        oldpath = F"{image_dir}\\{name}"
        with open(oldpath, "rb") as fin:
            data = fin.read()
        hval = blake2s(data, digest_size=8).hexdigest()
        newpath = F"{image_dir}\\{hval}.jpg"
        if not os.path.exists(newpath):
           with open(newpath, "wb") as fout:
               fout.write(data)
               n += 1
        if newpath.lower() != oldpath.lower():
           os.remove(oldpath)
    if n > 0:
        print(n, "files renamed")

rename2("hand")
rename2("mouth")


