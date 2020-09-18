#!python
# Rename file to it's hashvalue.ext
import os, sys, re, json
from zlib import crc32
from hashlib import blake2s, md5 as hash_md5

print("Start rename files using configure:")

try:
    with open("rename2.json") as fin:
        conf = json.load(fin)
        print(json.dumps(conf, indent=4))
        sre = conf["sre"]
        srcdir = conf["srcdir"]
        method = conf["method"]
        exclude = conf["exclude"]
except Exception as e:
    print(e, file=sys.stderr)

record = {}
if sre:
    x = re.compile(sre)
else:
    x = None

for dirname in srcdir:
    names = os.listdir(dirname)
    print("Process:", dirname, len(names))

    for name in names:
        oldpath = F"{dirname}\\{name}"
        if x and not x.match(name):
            record[oldpath] = oldpath
            continue

        if exclude and exclude in name:
            record[oldpath] = oldpath
            continue

        with open(oldpath, "rb") as fin:
            data = fin.read()

        if method == "md5":
            hval = hash_md5(data).hexdigest()
        elif method == "blake":
            hval = blake2s(data, digest_size=8).hexdigest()
        elif method == "crc":
            hval = str(crc32(data))
            while len(hval) < 8:
                hval = "0" + hval
        else:
            raise ValueError(method)

        ext = name.rsplit(".", 1)[-1]
        if ext == name:
            ext = ""
        else:
            ext = "." + ext

        newpath = F"{dirname}\\{hval}{ext}"
        if not os.path.exists(newpath):
            with open(newpath, "wb") as fout:
                fout.write(data)
        if newpath.lower() != oldpath.lower():
            os.remove(oldpath)

        record[oldpath] = newpath

print(len(list(k for k in record if record[k] != k)), "files renamed")
os.system("pause")
