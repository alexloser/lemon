#!python
import os, sys, re, json
from zlib import crc32
from hashlib import md5 as hashMD5


def Rename2(srcdir:list, sre:str, method:str, excludes:list):
    """ Rename all files info specific format """
    x = re.compile(sre)
    if method not in ("md5", "crc32-size"):
        raise ValueError(method)

    record = {}
    for dirname in srcdir:
        names = os.listdir(dirname)
        print("Process:", dirname, len(names), file=sys.stderr)
        for name in names:
            oldpath = F"{dirname}\\{name}"
            if not x.match(name):
                continue
            skip = False
            for ex in excludes:
                if ex in name:
                    skip = True
                    break
            if skip:
                continue
            with open(oldpath, "rb") as fin:
                data = fin.read()
            if method == "md5":
                hval = hashMD5(data).hexdigest()
            else:
                hval = str(crc32(data))
                while len(hval) < 8:
                    hval = "0" + hval
                hval = F"{hval}-{os.path.getsize(oldpath)}"
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
            else:
                if newpath.lower() != oldpath.lower():
                    print(F"Already exist: {newpath}")
            record[oldpath] = newpath

    print(len(list(k for k in record if record[k] != k)), "files renamed", file=sys.stderr)


if __name__ == "__main__":
    with open("rename2.json") as fin:
        conf = json.load(fin)
        srcdir = conf["srcdir"]
        sre = conf["regex"]
        method = conf["method"]
        excludes = conf["excludes"]
        print("Start rename files using configure:", file=sys.stderr)
        print(json.dumps(conf, indent=4), file=sys.stderr)
        Rename2(srcdir, sre, method, excludes)
    
    os.system("pause")