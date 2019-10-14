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
CC  += -std=c99   -m64 -pthread -fopenmp -fPIC
CXX += -std=c++11 -m64 -pthread -fopenmp -fPIC -D_GLIBCXX_USE_CXX11_ABI=${CXX11_ABI}

DEFINE     = ${DEFINE}

WARNING    = ${WARNING}

OPTIMIZE0  = ${OPTIMIZE0}

OPTIMIZE3  = ${OPTIMIZE3}
OPTIMIZE3 += ${OPTIMIZE3_EXTRA}

CFLAGS = $(DEFINE) $(WARNING)

LINK = ${LINK}

LIBS = ${LIBS1}
LIBS += ${LIBS2}
LIBS += ${LIBS3}

all: debug release
    rm -rf debug/*.o
    rm -rf release/*.o

debug: main.d
    $(CXX) $(CFLAGS) $(OPTIMIZE0) $(LINK) debug/*.o -o debug/${PRONAME}.d $(LIBS)
    rm -rf debug/*.o

release: main
    $(CXX) $(CFLAGS) $(OPTIMIZE3) $(LINK) release/*.o -o release/${PRONAME} $(LIBS)
    rm -rf release/*.o

main.d:
    $(CXX) $(CFLAGS) $(OPTIMIZE0)  -c src/main.cc  -o debug/main.o

main:
    $(CXX) $(CFLAGS) $(OPTIMIZE3)  -c src/main.cc  -o release/main.o


clean:
    mkdir -p debug release
    rm -rf debug/*
    rm -rf release/*

""")



DATE = '2019-10'

PRONAME = 'xxxx'

PHONY = []

CXX11_ABI = 1

DEFINE = ['-D_GNU_SOURCE', '-D_REENTRANT', '-DARMA_64BIT_WORD', '-DARMA_NO_DEBUG', '-DDEEPX_USE_TCMALLOC', '-DPIC']

WARNING = ['-Wall', '-Wextra', '-Wno-unused-parameter']

OPTIMIZE0 = ['-DDEBUG', '-O0', '-gdwarf-3']

OPTIMIZE3 = ['-DNDEBUG', '-Ofast', '-g0', '-mcrc32', '-mavx', '-march=native', '-mtune=intel']

OPTIMIZE3_EXTRA = ['-funroll-loops', '-ffast-math', '-fomit-frame-pointer', '-minline-stringops-dynamically']

LINK = ['-L.', '-L ./libs', '-Wl,-rpath=.', '-Wl,-rpath=./.lib']

LIBS1 = ['-lboost_system']
LIBS2 = ['-lunwind', '-lglog', '-lgflags', '-ltcmalloc']
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
    rargs['OPTIMIZE0'] = ' '.join(OPTIMIZE0)
    rargs['OPTIMIZE3'] = ' '.join(OPTIMIZE3)
    rargs['OPTIMIZE3_EXTRA'] = ' '.join(OPTIMIZE3_EXTRA)
    rargs['LINK'] = ' '.join(LINK)
    rargs['LIBS1'] = ' '.join(LIBS1)
    rargs['LIBS2'] = ' '.join(LIBS2)
    rargs['LIBS3'] = ' '.join(LIBS3)
    
    content = mkt.render(**rargs).replace('    ', '\t')
    print(content)
    


if __name__ == '__main__':
    find_gcc()
    create_makefile()







