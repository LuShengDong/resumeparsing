# -*- coding: utf-8 -*-
import argparse
import os
import codecs
import re
from shutil import copyfile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='directory')
    parser.add_argument('--dir', type=str, help='Resumes directory.')
    args = parser.parse_args()
    directory = args.dir
    files = os.listdir(directory)
    for file in files:
        path = directory+'\\'+file
        with codecs.open(path, 'r', 'utf-8') as f:
            summation = 0
            cn_word = 0
            for line in f:
                content = line.strip()
                summation += 1
                if len(re.findall(re.compile(u"[\u4e00-\u9fa5]+"), content)) > 0:
                    cn_word += 1
        if cn_word/summation < 0.1:
            os.remove(path)
