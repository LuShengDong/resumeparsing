# -*- coding: utf-8 -*-
import argparse
import os
import codecs
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='directory')
    parser.add_argument('--dir', type=str, help='Resumes directory.')
    args = parser.parse_args()
    directory = args.dir
    files = os.listdir(directory)
    is_subsection = []
    not_subsection = []
    for file in files:
        path = directory+'\\'+file
        with codecs.open(path, 'r', 'utf-8') as f:
            font_content = {}
            for line in f:
                content = line.strip()
                number = re.match(r'{[0-9.]+}', content)
                content = re.sub(r'{[0-9.]+}', '', content)
                if number is None:
                    continue
                number = float(number[0][1:-1])
                if number < 20:
                    if number not in font_content:
                        font_content[number] = []
                    font_content[number].append(content)
            maxfont = max(font_content.keys())
            if 3 < len(font_content[maxfont]) < 10:
                for word in font_content[maxfont]:
                    if len(re.findall(re.compile(u"[\u4e00-\u9fa5]+"), word)) > 0:
                        is_subsection.append(word)
                    else:
                        not_subsection.append(word)
            else:
                not_subsection += font_content[maxfont]
            for font in font_content:
                if font != maxfont:
                    not_subsection += font_content[font]
            not_subsection = [word for word in not_subsection if len(word) > 1]

    my_path = os.path.abspath(os.path.dirname(__file__))
    is_path = os.path.join(my_path, './training/is_subsection.txt')
    with codecs.open(is_path, 'w', 'utf-8') as f:
        f.write('\n'.join(is_subsection))
    ns_path = os.path.join(my_path, './training/not_subsection.txt')
    with codecs.open(ns_path, 'w', 'utf-8') as f:
        f.write('\n'.join(not_subsection))
