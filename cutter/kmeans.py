# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from cutter.bayes import data_loader
import jieba
import jieba.posseg as pseg
import pickle
import os
import numpy as np
import codecs

pos_dict = ['v', 'n', 'x', 'a', 'm']
kmeans_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './kmeans_vectors.pkl')
kmeans_classifier_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), './kmeans_cutter.pkl')

def feature_gen(line):
    feature_vector = []
    words = list(pseg.cut(line))
    feature_vector.append(len(words))
    pos_tag = [tag for w, tag in words]
    count = [0] * len(pos_dict)
    for tag in pos_tag:
        if tag[0] in pos_dict:
            count[pos_dict.index(tag[0])] += 1
    feature_vector += count

    oh_head = [0] * len(pos_dict)
    if pos_tag[0][0] in pos_dict:
        oh_head[pos_dict.index(pos_tag[0][0])] = 6
    return feature_vector


def get_classifier(train=False, new_feature=False, k=8):
    if new_feature:
        training = data_loader()
        x = [feature_gen(data) for data, _ in training]
        with open(kmeans_file_path, 'wb') as kf:
            pickle.dump(x, kf)
    else:
        with open(kmeans_file_path, 'rb') as kf:
            x = pickle.load(kf)

    if train:
        x = np.array(x)
        kmeans = KMeans(n_clusters=k).fit(x)
        with open(kmeans_classifier_path, 'wb') as kc:
            pickle.dump(kmeans, kc)
    else:
        with open(kmeans_classifier_path, 'rb') as kc:
            kmeans = pickle.load(kc)
    return kmeans


if __name__ == '__main__':
    with codecs.open('samples/5.cd.txt', 'r', 'utf-8') as test_file:
        for sentence in test_file:
            sentence = sentence.strip()
            feature = feature_gen(sentence)
            kmeans = get_classifier()
            print(kmeans.predict([feature]), sentence)


