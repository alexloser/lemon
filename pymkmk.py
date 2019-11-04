#!/usr/bin/env python3
# coding: utf-8
''' This script works only for internal program '''
import sys, os, re
import subprocess

error = __file__.split(os.sep)[-1] + ' Error:'
try:
    from mako.template import Template
except ImportError:
    print(error, 'mako library can not be imported!', file=sys.stderr)
    sys.exit()


mkt = Template("""#!/usr/bin/env make
# Makefile of ${PRONAME}
# This file was created by python script with template.
# Don't change this file unless you know the details and consequence.
# Only works on linux system with gcc-5.4+ and necessary libraries.
# Author: AlexLoser
# Create: ${DATE}

.PHONY: all debug release main ${PHONY}
CC  = ${CC}
CXX = ${CXX}
CC  += -std=gnu99   -m64 -pthread -fopenmp -fPIC
CXX += -std=gnu++11 -m64 -pthread -fopenmp -fPIC -D_GLIBCXX_USE_CXX11_ABI=${CXX11_ABI}

DEFINE  = ${DEFINE}

WARNING = ${WARNING}

OPT0  = ${OPT0}

OPT3  = ${OPT3}
OPT3 += ${OPT3_EXTRA}

CF = $(DEFINE) $(WARNING)

LINK = ${LINK}

LIBS = ${LIBS1}
LIBS += ${LIBS2}
LIBS += ${LIBS3}

VER = 1.0

all: build
    rm -rf build/*.o

build: main
    mkdir -p ./build
    $(CXX) $(CF) $(OPT3) $(LINK) build/*.o -o build/${PRONAME}.$(VER) $(LIBS)
    rm -rf release/*.o

main:
    $(CXX) $(CF) $(OPT3) -c src/main.cc  -o build/main.o


clean:
    mkdir -p build
    rm -rf build/*.o build/${PRONAME}.$(VER)

""")



DATE = '2019-10'

PRONAME = 'xxxx'

PHONY = []

CXX11_ABI = 1

DEFINE = ['-D_GNU_SOURCE', '-D_REENTRANT', '-DARMA_64BIT_WORD', '-DARMA_NO_DEBUG', '-DDEEPX_USE_TCMALLOC', '-DPIC']

WARNING = ['-Wall', '-Wextra', '-Wno-unused-parameter']

OPT0 = ['-DDEBUG', '-O0', '-gdwarf-3']

OPT3 = ['-DNDEBUG', '-Ofast', '-g0', '-mcrc32', '-mavx', '-march=native', '-mtune=intel']

OPT3_EXTRA = ['-funroll-loops', '-ffast-math', '-fomit-frame-pointer', '-minline-stringops-dynamically']

LINK = ['-L.', '-L ./libs', '-Wl,-rpath=.', '-Wl,-rpath=./.lib']

LIBS1 = ['-lboost_system']
LIBS2 = ['/usr/local/lib/libglog.a', '/usr/local/lib/libgflags.a', '/usr/local/lib/libtcmalloc_minimal.a']
LIBS3 = ['-lm', '-lmvec', '-ldl', '-static-libgcc', '-static-libstdc++']


def find_gcc():
    if not os.path.exists('/usr/bin/gcc'):
        print(error, 'can Not find gcc and g++ compiler!')
    pipe = subprocess.Popen(['/usr/bin/gcc -v'], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = pipe.stderr.read().decode()
    target = re.compile('gcc version ([5-9])').findall(output)
    if not target:
        print(error, "can not find correct gcc or g++ compiler!")
        sys.exit()
    return 'gcc-' + target[0]


def create_makefile():
    gccver = find_gcc()
    rargs = {
        'CC' : gccver,
        'CXX' : gccver.replace('cc', '++')
    }
    rargs['DATE'] = DATE
    rargs['PRONAME'] = PRONAME
    rargs['CXX11_ABI'] = CXX11_ABI
    rargs['PHONY'] = ' '.join(PHONY)
    rargs['DEFINE'] = ' '.join(DEFINE)
    rargs['WARNING'] = ' '.join(WARNING)
    rargs['OPT0'] = ' '.join(OPT0)
    rargs['OPT3'] = ' '.join(OPT3)
    rargs['OPT3_EXTRA'] = ' '.join(OPT3_EXTRA)
    rargs['LINK'] = ' '.join(LINK)
    rargs['LIBS1'] = ' '.join(LIBS1)
    rargs['LIBS2'] = ' '.join(LIBS2)
    rargs['LIBS3'] = ' '.join(LIBS3)
    
    content = mkt.render(**rargs).replace('    ', '\t')
    print(content)
    


if __name__ == '__main__':
    find_gcc()
    create_makefile()







