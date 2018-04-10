# -*- coding: utf-8 -*-

from cutter.bayes import get_classifier, features_gen, cls_path
import codecs
import argparse
import pickle


def cut(lines, train=False) -> dict:
    struct = {}
    if train:
        classifier, _ = get_classifier()
    else:
        with open(cls_path, 'rb') as cls_f:
            classifier = pickle.load(cls_f)
    current = []
    struct['Personal_Info'] = current
    for line in lines:
        line = line.strip()
        if classifier.classify(features_gen(line)) == 'title':
            current = []
            struct[line] = current
            continue
        current.append(line)
    return struct


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=str, help='resume')
    args = parser.parse_args()
    with codecs.open(args.r, 'r', 'utf-8') as f:
        resume = f.readlines()
        structure = cut(resume)
    import json
    with codecs.open('data.txt', 'w', 'utf-8') as outfile:
        json.dump(structure, outfile)
