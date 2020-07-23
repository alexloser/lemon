# -*- coding:utf-8 -*-
# author : alexloser
# note   : python3.6+
"""
Tiny utils library for python3.
Copy this file into your project to use.    
"""
import sys
import os
import inspect
import traceback
import threading
import multiprocessing
import subprocess
import functools
import re
import zlib
import json
import pickle
from pathlib import Path
from time import strftime, localtime, sleep, time
from hashlib import md5 as hashlib_md5
from base64 import b64encode, b64decode

# Define current python version, should be (3. x)
PYTHON_VERSION = (sys.version_info.major, sys.version_info.minor)

# The number of logical cores in CPU, return None if indeterminable
NUM_CPU = os.cpu_count()

# CUDA environ informations
CUDA_INFO = {_: os.environ[_] for _ in os.environ if "CUDA" in _}

# Used for add custom path to sys.path
ADD_SYS_PATH = lambda path, index=0: sys.path.insert(index, path)

def ADD_ENV_PATH(path):
    """ Add path to environment values """
    os.environ["PATH"] = os.environ["PATH"].rstrip(";") + F";{path.strip(';')};"


def DisableCuda():
    """ Disable using GPU with cuda """
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def EnableCuda():
    """ Enable using GPU with cuda """
    try:
        os.environ.pop("CUDA_VISIBLE_DEVICES")
    except KeyError:
        pass


def IsCudaEnabled():
    """ Check if cuda enabled """
    try:
        return os.environ["CUDA_VISIBLE_DEVICES"] != "-1"
    except KeyError:
        return True


def EnvironVariable(sre_key=None, sre_val=None):
    """ Get os.environ values """
    if not sre_key and not sre_val:
        return os.environ.copy()
    xk, xv = None, None
    if sre_key:
        xk = re.compile(sre_key)
    if sre_val:
        xv = re.compile(sre_val)
    return {
        k:v for k, v in os.environ.items() \
        if (xk and re.search(xk, k)) or (xv and re.search(xv, v))
    }


def TID() -> int:
    """ Get current thread ID """
    return threading.current_thread().ident


def PID() -> int:
    """ Get current process ID """
    return os.getpid()


def Execute(cmd: str, stdout=subprocess.PIPE, stderr=subprocess.PIPE) -> bytes:
    """ Execute system command using Popen and return the result str """
    with subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr) as p:
        p.wait()
        return p.stdout.read(), p.stderr.read()


def Popen(cmd: str, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """ Same as execute, but return opened pipe, 
        user code should use with...as style to ensuring resource release:
        with Popen("ls -a") as pipe:
            pipe.wait()
            print(pipe.stdout.read().decode())
    """
    return subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)


def SplitPath(path):
    """ Split path to each single parts """
    return os.path.realpath(path).split(os.sep)


def IsDir(path):
    """ Check is dir or not """
    return os.path.isdir(path)


def UserDir():
    """ Get current user's dir with os.sep """
    return os.path.expanduser('~')


def HomeDir():
    """ Get home dir of current user with os.sep """
    return str(Path.home())


def CurrentDir():
    """ Get current dir of user """
    return str(Path(os.path.curdir).absolute())


def ParentDir(name):
    """ Get parent directory of existed filename """
    return str(Path(name).parent.absolute()).rstrip(os.sep)


def GrandDir(name):
    """ Get grand father directory of existed filename """
    return ParentDir(ParentDir(name))


def RealPath(name):
    """ Return real path(absolute) of exist file """
    return os.path.realpath(name)


def Basename(name):
    """ Get base name of filename """
    return os.path.basename(os.path.realpath(name))


def DirName(name):
    """ Get directory name of filename with os.sep """
    return os.path.dirname(os.path.realpath(name))


def ExtName(name):
    """ Get extention name of filename with os.sep """
    return os.path.splitext(name)[1]


def ExtApart(name):
    """ "abc/xyz.exe"  =>  ["abc/xyz", "exe"] """
    return name.rsplit(".", 1)


def FileTime(name) -> tuple:
    """ Get file time, return (ctime, mtime, atime) """
    assert os.path.exists(name)
    fstat = os.lstat(name)
    ct, mt, at = fstat.st_ctime, fstat.st_mtime, fstat.st_atime
    return (localtime(ct), localtime(mt), localtime(at))


def FileExist(name):
    """ Check file exist or not """
    return os.path.exists(name)


def MakeDir(path, check_existed=False):
    """ Make new dir """
    if check_existed and os.path.exists(path):
        raise FileExistsError(F"Create failed: {path}")
    try:
        os.mkdir(path)
        return True
    except:
        # print(F"Path {path} already exists!!!")
        return False


def SpanWildcard(path: str, wildcard: str) -> list:
    """ Get a list contains after span the wildcard in path """
    # print(os.path.realpath(path))
    return [str(p) for p in Path(os.path.realpath(path)).glob(wildcard)]


def SpanWildcardRecurse(path: str, wildcard: str) -> list:
    """ Same as SpanWildcard, but recursive """
    # print(os.path.realpath(path))
    return [str(p) for p in Path(os.path.realpath(path)).rglob(wildcard)]


def FileMonitor(filename, interval=0.5, repeat=2) -> bool:
    """ Monitor any changes of file, return if no changes after speciafic time(interval * repeat). """
    if os.path.isfile(filename) and os.path.exists(filename):
        t = FileTime(filename)
        n = os.path.getsize(filename)
        for _ in range(repeat):
            sleep(interval)
            if FileTime(filename) != t:
                return False
            if n != os.path.getsize(filename):
                return False
        return True
    raise FileNotFoundError(filename)


def IsoTime(fmt="%F %T"):
    """ Return iso datetime, like 2014-03-28 19:45:59 """
    return strftime(fmt)


def PathWalk(path, callback=lambda _: True):
    """ Walking in path and call user's function with file names in path """
    assert os.path.exists(path)
    for root, _, naked in os.walk(path):
        if not root.endswith(os.sep):
            root += os.sep
        for name in naked:
            if callback(root + name):
                yield root + name


def ListDir(path, sre=None, callback=lambda _: True):
    """ List all filenames in `path` which matched `sre` recursive """
    names = list(PathWalk(path, callback))
    if not sre:
        return names
    else:
        rgx = re.compile(sre)
        return [_ for _ in names if rgx.match(_)]


def FileSize(name):
    """ Get size(in bytes) of file """
    return os.path.getsize(name)


def PickleLoad(path):
    """ Load pickle file """
    with open(path, "rb") as fin:
        return pickle.load(fin)


def PickleSave(path, obj):
    """ Save to pickle file """
    with open(path, "wb") as fout:
        pickle.dump(obj, fout)


def LoadJson(path, obj_hook=None) -> dict:
    """ Load json from file and return dict 
        `obj_hook` : callback for building non-builtin objects
    """
    for enc in ("utf-8", "utf-8-sig"):
        try:
            with open(path, encoding=enc) as f:
                return json.loads(f.read(), encoding=enc, object_hook=obj_hook)
        except UnicodeError:
            pass
    with open(path, encoding='gbk') as f:
        return json.loads(f.read(), encoding='gbk', object_hook=obj_hook)


def SaveJson(obj, path=None) -> str:
    """ Dump dict objects to file and return string """
    jstr = json.dumps(obj, indent=4, ensure_ascii=False)
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(jstr)
    return jstr


def Base64Encode(s):
    if isinstance(s, str):
        s = s.encode('utf8')
    return b64encode(s, altchars=None).decode()


def Base64Decode(s):
    return b64decode(s, altchars=None, validate=False).decode()


def ToBytes(obj: object) -> bytes:
    """ Get bytes of object if supported, 
        using 'ascii' or 'utf-8' as defualt string encode 
    """
    if isinstance(obj, str):
        try:
            return bytes(obj, 'ascii')
        except UnicodeEncodeError:
            return bytes(obj, 'utf-8')
    elif isinstance(obj, (bytes, bytearray)):
        return obj
    return memoryview(obj).tobytes()


def UTF8(s, errors='replace') -> str:
    """ Transform str to 'utf-8' coding """
    return str(s, 'utf-8', errors=errors)


def CRC32(filename):
    """ Get CRC32 value of file """
    with open(filename, "rb") as fin:
        buf = fin.read()
    return zlib.crc32(buf)


def MD5(buf: bytes) -> str:
    """ Get MD5 hexdigest of bytes """
    return hashlib_md5(buf).hexdigest()


def FileMD5(name):
    """ Get MD5 string of file """
    with open(name, 'rb') as fin:
        return MD5(fin.read())


def Parallel(callback, data=[], num_cores=0):
    """ User redefined """
    assert data
    if num_cores > 0:
        nc = num_cores
    else:
        nc = os.cpu_count() // 2
    ret = []
    if len(data) <= nc * 10:
        for i in range(len(data)):
            ret.append(callback(data[i:i + 1]))
    else:
        with multiprocessing.Pool(nc) as mp:
            group_size = len(data) // nc
            for i in range(0, nc + 1):
                l, r = i * group_size, (i + 1) * group_size
                ret.append(mp.apply_async(callback, (data[l:r], )))
            ret = [p.get(timeout=None) for p in ret]
    sys.stdout.flush()
    sys.stderr.flush()
    return ret


def Chronotime():
    """ Date and time for debug info """
    t = time()
    return strftime(F"%F %T.{str(t).split('.')[1][:3]}", localtime(t))


def ClassName(cls):
    """ return object's class name """
    if isinstance(cls, type):
        return str(cls).split()[1].split("'")[1]
    return str(type(cls)).split()[1].split("'")[1]


def CallerOfScope(depth=1):
    """ Get caller of current frame, return Traceback object """
    cf = inspect.currentframe()
    for _ in range(depth + 1):
        cf = cf.f_back
    try:
        return inspect.getframeinfo(cf).function
    except AttributeError:
        return inspect.getframeinfo(inspect.currentframe()).function


def FormatTrackback(tb, depth=3):
    """ Get trackback info when error happened """
    return ''.join(traceback.format_tb(tb, limit=depth))


def Flush(stream=None):
    """ Flush stream(opened file or list), also flush stdout, stderr """
    global _DBG_OFS_
    if _DBG_OFS_:
        _DBG_OFS_.flush()
    sys.stdout.flush()
    sys.stderr.flush()
    if not stream:
        return
    if isinstance(stream, (list, tuple)):
        for s in stream:
            if hasattr(s, "flush"):
                s.flush()
    elif hasattr(stream, "flush"):
        stream.flush()


def PrintLastError(prefix="", output=sys.stderr):
    """ Print exception info, only used in except block """
    cls, val, tb = sys.exc_info()
    name = ClassName(cls)
    if prefix:
        name = F"{prefix} {name}"
    else:
        name = F"[{strftime('%F %T')}] {name}"
    print(F"{name}(\"{val}\") from:\n{FormatTrackback(tb)}", file=output, end='')
    Flush(output)
    return val, tb


# Output stream for DEBUG 
_DBG_OFS_ = None

def RedirectDEBUG(name, mode="a"):
    """ Set debug info redirect file, should be called only once in Main """
    global _DBG_OFS_
    if _DBG_OFS_:
        _DBG_OFS_.close()
    _DBG_OFS_ = open(name, mode=mode, buffering=1)


def DEBUG(*info, stream=sys.stderr):
    """ Print to stderr debug info """
    print(F"[{Chronotime()} {CallerOfScope()}]", *info, file=stream, flush=True)
    if _DBG_OFS_ is not None:
        print(F"[{Chronotime()} {CallerOfScope()}]", *info, file=_DBG_OFS_, flush=True)


def ERROR_EXIT(e):
    """ Print exception info and exit """
    DEBUG(F"{ClassName(e)}: {e}")
    Flush()
    Exit(1)


class _IOFlusher(threading.Thread):
    """ Flush iostream every `delay` seconds """
    def __init__(self, streams=[sys.stdout, sys.stderr]):
        super().__init__()
        self.daemon = True
        self._streams = streams
        self._interval = 1
    def set_interval(self, seconds):
        self._interval = seconds
    def run(self):
        while True:
            sleep(self._interval)
            Flush(self._streams)


# the global io flusher
__io_flusher__ = _IOFlusher([sys.stdout, sys.stderr])

def RunIOFlusher(interval=1) -> bool:
    """ Daemon flusher, call only once in Main """
    global __io_flusher__
    __io_flusher__.set_interval(interval)
    if __io_flusher__.is_alive():
        return False
    __io_flusher__.start()
    return True


def Exit(code):
    """ Exit without raise SystemExit exception """
    if _DBG_OFS_ is not None:
        _DBG_OFS_.close()
    os._exit(code)


def WatchElapsed(func):
    """ Decorator for print elapsed time """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print(F"[{Chronotime()}] Enter {func}", file=sys.stderr, flush=True)
        ret = func(*args, **kwargs)
        print(F"[{Chronotime()}] Leave {func}", file=sys.stderr, flush=True)
        return ret
    return wrapped



if __name__ == "__main__":
    """ simple test """
    print(F"PYTHON_VERSION: {PYTHON_VERSION}")
    print(F"NUM_CPU: {NUM_CPU}")
    print(F"CUDA_INFO: {CUDA_INFO}")
    ADD_SYS_PATH("test")
    assert sys.path[0] == "test"
    ADD_SYS_PATH("test", -2)
    assert sys.path[-3] == "test"

    env = EnvironVariable()
    assert env == os.environ
    print(len(env))
    env = EnvironVariable("CUDA")
    assert env == CUDA_INFO
    print(env)
    env = EnvironVariable(sre_val="[Ii]ntel|AMD[0-9]+")
    print(env)

    RunIOFlusher(0.1)
    print(F"FileSize: {FileSize(__file__)}")
    print(F"FileTime: {FileTime(__file__)}")
    print(F"IsDir: {IsDir(__file__)}")
    print(F"FileExist: {FileExist(__file__)}")
    print(F"DirName: {DirName(__file__)}")
    print(F"ParentDir: {ParentDir(__file__)}")
    print(F"GrandDir: {GrandDir(__file__)}")
    print(F"Basename: {Basename(__file__)}")
    print(F"ExtName: {ExtName(__file__)}")
    print(F"UserDir: {UserDir()}")
    print(F"HomeDir: {HomeDir()}")
    print(F"CurrentDir: {CurrentDir()}")
    print(F"FileMonitor: {FileMonitor(__file__, 0.2, 2)}")
    print(F"IsoTime: {IsoTime()}")
    print(F"SplitPath: {SplitPath(__file__)}")
    print(list(PathWalk(".")))
    print(SpanWildcard("..", "*.py"))
    print(SpanWildcardRecurse("..", "i*.py"))

    cout, cerr = Execute("python -V")
    print(cout.decode())

    with Popen("python -V") as p:
        p.wait()
        print(p.stdout.read())

    print(F"MD5: {MD5(open(__file__, 'rb').read())}")
    print(f"CRC32: {CRC32(__file__)}")
    print(F"ToBytes: {ToBytes(__file__)}")
    s = UTF8(b"Test+string")
    b = Base64Encode(s)
    print(b)
    print(Base64Decode(b))
    Flush()

    class Beta(object):
        @WatchElapsed
        def test_func(self):
            DEBUG("test info")
            try:
                raise RuntimeError("test")
            except:
                PrintLastError()

        @WatchElapsed
        def run(self):
            return sum(list(range(1000000)))

    Beta().test_func()
    Beta().run()
    Flush()

