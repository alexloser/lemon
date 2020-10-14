#!python
import os, sys, re, json, threading
from zlib import crc32
from hashlib import md5 as hashMD5


def rename2(srcdir: str, sre: str, method: str, excludes: list):
    x = re.compile(sre)
    record = {}
    names = os.listdir(srcdir)
    print("Process:", os.path.realpath(srcdir), len(names), file=sys.stderr)

    for i, name in enumerate(names):
        if (i + 1) % 1000 == 0:
            print(("TID-%-5d Processed %d" % (threading.get_ident(), i+1)), file=sys.stderr, flush=True)
        if not x.match(name):
            continue

        skip = False
        for ex in excludes:
            if ex in name:
                skip = True
                break
        if skip:
            continue

        oldpath = F"{srcdir}\\{name}"
        with open(oldpath, "rb") as fin:
            data = fin.read()
        if method == "md5":
            hval = hashMD5(data).hexdigest()
        else:  # "crc32-size"
            hval = str(crc32(data))
            while len(hval) < 8:
                hval = "0" + hval
            hval = F"{hval}-{os.path.getsize(oldpath)}"
        
        ext = name.rsplit(".", 1)[-1]
        if ext == name:
            ext = ""
        else:
            ext = "." + ext
        
        newpath = F"{srcdir}\\{hval}{ext}"
        if not os.path.exists(newpath):
            with open(newpath, "wb") as fout:
                fout.write(data)
            if newpath.lower() != oldpath.lower():
                os.remove(oldpath)
        else:
            if newpath.lower() != oldpath.lower():
                print(F"Already exist: {newpath}", file=sys.stderr)
        
        record[oldpath] = newpath
    
    n = len(list(k for k in record if record[k] != k))
    print(n, F"files renamed in {os.path.realpath(srcdir)}", file=sys.stderr)


def Rename2(srcdirs: list, sre: str, method: str, excludes: list):
    """ Rename all files info specific format """
    x = re.compile(sre)
    if method not in ("md5", "crc32-size"):
        raise ValueError(method)
    tasks = [threading.Thread(target=rename2, args=[d, sre, method, excludes]) for d in srcdirs]
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()


if __name__ == "__main__":
    with open("rename2.json") as fin:
        conf = json.load(fin)
    srcdirs = conf["srcdir"]
    sre = conf["regex"]
    method = conf["method"]
    excludes = conf["excludes"]
    print("Start rename files using configure:", file=sys.stderr)
    print(json.dumps(conf, indent=4), "\n", file=sys.stderr)
    Rename2(srcdirs, sre, method, excludes)
    print()
    os.system("pause")
