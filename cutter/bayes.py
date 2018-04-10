# -*- coding: utf-8 -*-

import nltk.classify.naivebayes as nb
import nltk
import codecs
import random
import jieba
import os
import pickle

my_path = os.path.abspath(os.path.dirname(__file__))
cls_path = os.path.join(my_path, './bayes_classifier.pkl')


def features_gen(line):
    features = {}
    features['length'] = len(line)
    features['length>6'] = len(line) > 6
    for num, letter in enumerate(line):
        features['letter({})'.format(num)] = letter
        features['hasletter({})'.format(letter)] = True
    words = jieba.lcut(line)
    features['word-length'] = len(words)
    for num, word in enumerate(words):
        features['letter({})'.format(num)] = word
        features['letter_reverse({})'.format(features['word-length']-num-1)] = word
        features['hasword({})'.format(word)] = True
    return features

def data_loader():
    is_title = []
    not_title = []
    my_path = os.path.abspath(os.path.dirname(__file__))
    is_path = os.path.join(my_path, './training/is_subsection.txt')
    with codecs.open(is_path, 'r', 'utf-8') as f:
        for line in f:
            is_title.append((line.strip(), 'title'))
    ns_path = os.path.join(my_path, './training/not_subsection.txt')
    with codecs.open(ns_path, 'r', 'utf-8') as f:
        for line in f:
            not_title.append((line.strip(), 'not_title'))
    training = is_title + not_title
    return training

def get_classifier():
    training = data_loader()
    random.shuffle(training)
    featureset = [(features_gen(n), label) for (n, label) in training]
    classifier = nb.NaiveBayesClassifier.train(featureset)
    return classifier, featureset

if __name__ == '__main__':
    classifier, training_data = get_classifier()
    with open(cls_path, 'wb') as f:
        pickle.dump(classifier, f)
    print(classifier.show_most_informative_features(10))
