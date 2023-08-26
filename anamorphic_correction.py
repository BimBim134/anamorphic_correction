#!/usr/bin/env python
from pathlib import Path
from glob import glob
import argparse
from os.path import isdir, exists
from os import mkdir
import multiprocessing as mp
from pprint import pprint

from PIL import Image


def correct(data):
    p = Path(data[0])
    name = p.stem
    fileType = p.suffix
    parent = str(p.parent) + '/'
    out_fp = parent + '/corrected/' + name + '_corrected' + fileType
    try:
        im = Image.open(p)
        exif = im.getexif()
        width, height = im.size
        width *= data[1]
        newsize = (int(width), height)
        im_out = im.resize(newsize)
        im_out.save(out_fp, exif=exif)
        print(name + ' done.')
    except:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-r', '--ratio', type=float, default=1.33)
    args = vars(parser.parse_args())
    user_filepath = args['path']
    if not exists(user_filepath+'/corrected'):
        mkdir(user_filepath + '/corrected')
    else:
        print('destination folder allready exist')
    ratio = args['ratio']
    if isdir(user_filepath):
        if user_filepath[-1] != '/':
            paths = glob(user_filepath+'/*')
        else:
            paths = glob(user_filepath+'*')
    tasks = [[p, ratio] for p in paths]
    with mp.Pool() as p:
        p.map(correct, tasks)

if __name__ == '__main__':
    main()

# /home/bimbim/Pictures/photos
# C:\Users\pmben\Pictures\FUJI
# C:\Users\pmben\Pictures\FUJI\test