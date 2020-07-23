# coding: utf-8
""" Helpers for load and save numpy dataset """
import numpy
import struct
import cv2
import os, sys
from zlib import crc32


def mnist2image(path_train_data, path_label_data, output_dir, howmany):
    """ 
    Read mnist binary data from `path_train_data` and `path_label_data`,
        output pictures in `output_dir` which must be existed. 
    Param:
        path_train_data - path of mnist file "train-images.idx3-ubyte" 
        path_label_data - path of mnist file "train-labels.idx3-ubyte" 
        howmany: should less than 60000
    Return:
        None
    """
    images, labels = [], []

    with open(path_train_data, 'rb') as f:
        buf = f.read()
        offset = 0
        magic, n, rows, cols = struct.unpack_from('>IIII', buf, offset)
        print("reading", path_train_data, "%x" % magic, n, rows, cols)
        offset += struct.calcsize('>IIII')
        for n in range(howmany):
            arr = struct.unpack_from('>784B', buf, offset)
            offset += struct.calcsize('>784B')
            arr = numpy.array(arr, dtype='uint8').reshape(28, 28, 1)
            images.append(arr)

    with open(path_label_data, 'rb') as f:
        buf = f.read()
        offset = 0
        magic, n = struct.unpack_from('>II', buf, offset)
        print("reading", path_label_data, "%x" % magic, n)
        offset += struct.calcsize('>II')
        for n in range(howmany):
            arr = struct.unpack_from('>1B', buf, offset)
            offset += struct.calcsize('>1B')
            labels.append(arr[0])

    for i in range(10):
        classdir = output_dir + str(i)
        if not os.path.exist(classdir):
            print('mkdir', classdir)
            os.makedirs(classdir)

    for n in range(howmany):
        crc = crc32(images[n].tobytes())
        outpath = output_dir + '/%d/mnist-%x-%d.bmp' % (labels[n], crc, labels[n])
        if not cv2.imwrite(outpath, images[n]):
            raise RuntimeError(outpath)

    print(howmany, 'images saved, see', os.path.realpath(output_dir))



if __name__ == '__main__':
    while True:
        print("OK")
    if len(sys.argv) != 5:
        print("Usage: python mnist2image train_data label_data output_dir howmany")
    else:
        mnist2image(path_train_data, path_label_data, output_dir, howmany)