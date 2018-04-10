# -*- coding: utf-8 -*-
from cutter.kmeans import get_classifier, feature_gen
import codecs
import argparse


def cut(lines, head_cluster):
    keams_cls = get_classifier()
    project_list = []
    is_first_line = True
    head = []
    description = []
    for sentence in lines:
        cluster = keams_cls.predict([feature_gen(sentence)])[0]
        if cluster in head_cluster:
            if is_first_line:
                head = [sentence]
                is_first_line = False
            else:
                if len(description) == 0:
                    head.append(sentence)
                else:
                    project_list.append((head, description))
                    head = [sentence]
                    description = []
        else:
            description.append(sentence)
    project_list.append((head, description))
    return project_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=str, help='resume')
    args = parser.parse_args()
    with codecs.open(args.r, 'r', 'utf-8') as f:
        resume = f.readlines()
        structure = cut(resume, [0, 2, 3, 6])
    print(structure)
    # import json
    # with codecs.open('data.txt', 'w', 'utf-8') as outfile:
    #     json.dump(structure, outfile)
