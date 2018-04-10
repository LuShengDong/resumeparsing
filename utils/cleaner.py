# -*- coding: utf-8 -*-
import argparse
import os
import codecs

def clean(filename):
    with open(filename, 'rb') as f:
        for line in f:
            linelist = [subchunk for chunk in line.strip().decode('utf-8').split('\t') for subchunk in chunk.split('  ')]
            for pline in linelist:
                if len(pline) > 1:
                    yield pline

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='aps')
    argparser.add_argument('-f', '--file', type=str, required=True)
    args = argparser.parse_args()
    fname = args.file
    with codecs.open(fname.replace('.txt', '')+'.cd.txt', 'w', 'utf-8') as of:
        of.write('\n'.join(clean(fname)))
