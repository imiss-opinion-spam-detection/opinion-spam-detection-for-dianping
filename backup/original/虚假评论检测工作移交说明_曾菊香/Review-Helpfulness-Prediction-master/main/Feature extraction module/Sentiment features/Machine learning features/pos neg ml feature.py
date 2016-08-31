#! /usr/bin/env python2.7
#coding=utf-8

"""
Use a stored sentiment classifier to identifiy review positive and negative probability.
This module aim to extract review sentiment probability as review helpfulness features.

"""


import textprocessing as tp
import pickle
import itertools
from random import shuffle

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

import sklearn


# 1. Load data  ## 加载数据集
review = tp.get_excel_data(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Review set\review1.xlsx", '1', '2', "data")
sentiment_review = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Review set\review1.xlsx", '1', '2')


# 2. Feature extraction method  ## 特征提取方法
# Used for transform review to features, so it can calculate sentiment probability by classifier
##  计算整个语料里面每个词和双词搭配的信息量
def create_words_bigrams_scores():
    posdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\pos_review.xlsx", 1, 1)
    negdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\neg_review.xlsx", 1, 1)
    
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))

    bigram_finder_pos = BigramCollocationFinder.from_words(posWords)
    bigram_finder_neg = BigramCollocationFinder.from_words(negWords)
    posBigrams = bigram_finder_pos.nbest(BigramAssocMeasures.chi_sq, 5000)
    negBigrams = bigram_finder_neg.nbest(BigramAssocMeasures.chi_sq, 5000)

    pos = posWords + posBigrams
    neg = negWords + negBigrams

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()
    for word in pos:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in neg:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    return word_scores

"""   ##   根据信息量进行倒序排序，选择排名靠前的信息量的词   ###   """
def find_best_words(word_scores, number):
    #把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
    best_words = set([w for w, s in best_vals])
    return best_words

# Initiallize word's information score and extracting most informative words
word_scores = create_words_bigrams_scores()
best_words = find_best_words(word_scores, 2000) # Be aware of the dimentions 注意维数

"""--** 选择信息量丰富的词作为特征 **--"""
def best_word_features(words):
    return dict([(word, True) for word in words if word in best_words])


# 3. Function that making the reviews to a feature set
def extract_features(dataset):
    feat = []
    for i in dataset:
        feat.append(best_word_features(i))
    return feat


# 4. Load classifier
clf = pickle.load(open('C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\sentiment_classifier_ZJX0719b.pkl'))

# Testing single review
pred = clf.prob_classify_many(extract_features(sentiment_review[:])) # An object contian positive and negative probabiliy

pred2 = []
for i in pred:
    pred2.append([i.prob('pos'), i.prob('neg')])

for r in review[:]:
    print r
    print "pos probability score: %f" %pred2[review.index(r)][0]
    print "neg probability score: %f" %pred2[review.index(r)][1]
    print

    
# 5. Store review sentiment probabilty socre as review helpfulness features
def store_sentiment_prob_feature(sentiment_dataset, storepath):
	pred = clf.prob_classify_many(extract_features(sentiment_dataset))
	p_file = open(storepath, 'w')
	for i in pred:
	    p_file.write(str(i.prob('pos')) + ' ' + str(i.prob('neg')) + '\n')
	p_file.close()

