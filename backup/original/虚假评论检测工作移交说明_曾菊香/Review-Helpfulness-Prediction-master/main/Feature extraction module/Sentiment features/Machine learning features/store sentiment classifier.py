#! /usr/bin/env python2.7
#coding=utf-8

"""
Use positive and negative review set as corpus to train a sentiment classifier.
This module use labeled positive and negative reviews as training set, then use nltk scikit-learn api to do classification task.
Aim to train a classifier automatically identifiy review's positive or negative sentiment, and use the probability as review helpfulness feature.

"""

import textprocessing as tp
import pickle
import itertools
from random import shuffle    #通过random静态对象调用该方法random.shuffle(lst)，将序列的所有元素随机排序

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

import sklearn
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import accuracy_score


# 1. Load positive and negative review data   ##载入积极和消极评论数据
pos_review = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\pos_review.xlsx", 1, 1)
neg_review = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\neg_review.xlsx", 1, 1)

pos = pos_review  #pos为一个去除了情感停用词的评论集的多维列表
neg = neg_review


"""
# Cut positive review to make it the same number of nagtive review (optional)
## 十几级文本的数量和消极文本一样多 ##
shuffle(pos_review)
size = int(len(pos_review)/2 - 18)

pos = pos_review[:size]
neg = neg_review

"""


# 2. Feature extraction function
# 2.1 Use all words as features
## 把所有的词作为特征，返回值为字典类型
def bag_of_words(words):
    return dict([(word, True) for word in words])


# 2.2 Use bigrams as features (use chi square chose top 200 bigrams)
## 把双词搭配作为特征
def bigrams(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(bigrams)


# 2.3 Use words and bigrams as features (use chi square chose top 200 bigrams)
##  把所有词和双词搭配一起作为特征
def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):  #200可选为其他值，经过多次测试得到最优质
    bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n)  #使用卡方统计的方法，选择排名靠前的200的双词
    return bag_of_words(words + bigrams)


# 2.4 Use chi_sq to find most informative features of the review ##采用卡方统计的选择具有最丰富信息量的特征
# 2.4.1 First we should compute words or bigrams information score  ##采用卡方统计的方法计算每个词的信息量
##  计算整个语料里面每个词的信息量
def create_word_scores():
    posdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\pos_review.xlsx", 1, 1)
    negdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\neg_review.xlsx", 1, 1)
    
    posWords = list(itertools.chain(*posdata))  #把多维数组解链成一维数组
    negWords = list(itertools.chain(*negdata))

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()   #可统计积极文本中的词频和消极文本中的词频
    for word in posWords:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in negWords:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()   #积极词的数量
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
         #计算积极词的卡方统计量，这里也可以计算互信息等其它统计量
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    return word_scores    #包括了每个词和这个词的信息量

##  计算整个语料里面每双词搭配的信息量
def create_bigram_scores():
    posdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\pos_review.xlsx", 1, 1)
    negdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\neg_review.xlsx", 1, 1)
    
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))

    bigram_finder_pos = BigramCollocationFinder.from_words(posWords)
    bigram_finder_neg = BigramCollocationFinder.from_words(negWords)
    posBigrams = bigram_finder_pos.nbest(BigramAssocMeasures.chi_sq, 8000)
    negBigrams = bigram_finder_neg.nbest(BigramAssocMeasures.chi_sq, 8000)

    pos = posBigrams
    neg = negBigrams

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

# Combine words and bigrams and compute words and bigrams information scores
##  计算整个语料里面每个词和双词搭配的信息量
def create_word_bigram_scores():
    posdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\pos_review.xlsx", 1, 1)
    negdata = tp.seg_fil_senti_excel(r"C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\seniment review set\neg_review.xlsx", 1, 1)
    
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))

    bigram_finder_pos = BigramCollocationFinder.from_words(posWords)
    bigram_finder_neg = BigramCollocationFinder.from_words(negWords)
    posBigrams =  bigram_finder_pos.nbest(BigramAssocMeasures.chi_sq, 5000)
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

# Choose word_scores extaction methods
# word_scores = create_word_scores()
# word_scores = create_bigram_scores()
# word_scores = create_word_bigram_scores()


# 2.4.2 Second we should extact the most informative words or bigrams based on the information score
## 选择排名靠前的信息量的词，d是特征的维度，通过不断调整直至最优
def find_best_words(word_scores, d):
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:d]
    best_words = set([w for w, s in best_vals])
    return best_words

# 2.4.3 Third we could use the most informative words and bigrams as machine learning features
## 使用信息量最丰富的词和双词作为机器学习的特征
# Use chi_sq to find most informative words of the review
def best_word_features(words, d):
    word_scores = create_word_bigram_scores()
    best_words = find_best_words(word_scores, int(d))
    return dict([(word, True) for word in words if word in best_words])

# Use chi_sq to find most informative bigrams of the review
def best_word_features_bi(words, d):
    word_scores = create_word_bigram_scores()
    best_words = find_best_words(word_scores, int(d))
    return dict([(word, True) for word in nltk.bigrams(words) if word in best_words])

# Use chi_sq to find most informative words and bigrams of the review
def best_word_features_com(words, d):
    word_scores = create_word_bigram_scores()
    best_words = find_best_words(word_scores, int(d))
    d1 = dict([(word, True) for word in words if word in best_words])
    d2 = dict([(word, True) for word in nltk.bigrams(words) if word in best_words])
    d3 = dict(d1, **d2)
    return d3



# 3. Transform review to features by setting labels to words in review
##  将文本特征化后再赋予类标签
def pos_features(feature_extraction_method, d):
    posFeatures = []
    for i in pos:#pos为积极评论集
        posWords = [feature_extraction_method(i, d),'pos']
        posFeatures.append(posWords)
    return posFeatures

def neg_features(feature_extraction_method, d):
    negFeatures = []
    for j in neg:
        negWords = [feature_extraction_method(j, d),'neg']
        negFeatures.append(negWords)
    return negFeatures

"""
## 找出排名靠前的信息量的词
best_words = find_best_words(word_scores, 1500) # Set dimension and initiallize most informative words

## 选择不同的特征作为机器学习的特征
# posFeatures = pos_features(bigrams)
# negFeatures = neg_features(bigrams)

# posFeatures = pos_features(bigram_words)
# negFeatures = neg_features(bigram_words)

posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)

# posFeatures = pos_features(best_word_features_com)
# negFeatures = neg_features(best_word_features_com)

# 4. Train classifier and examing classify accuracy
## 训练分类器并检测分类器准确度
# Make the feature set ramdon
shuffle(posFeatures)
shuffle(negFeatures)

# 75% of features used as training set (in fact, it have a better way by using cross validation function)
size_pos = int(len(pos_review) * 0.75)  
size_neg = int(len(neg_review) * 0.75)
train_set = posFeatures[:size_pos] + negFeatures[:size_neg]  #把75%的特征当做训练集
test_set = posFeatures[size_pos:] + negFeatures[size_neg:]  #吧25%的特征当做开发测试集
test, tag_test = zip(*test_set)  #把开发测试集（已经经过特征化和赋予标签了）分为数据和标签

## 使用训练集训练分类器并检测分类器准确度
def clf_score(classifier):
    classifier = SklearnClassifier(classifier)  #在nltk 中使用scikit-learn 的接口
    classifier.train(train_set)  #训练分类器
    predict = classifier.batch_classify(test)  #对开发测试集的数据进行分类，给出预测的标签
    return accuracy_score(tag_test, predict)   #对比分类预测结果和人工标注的正确结果，给出分类器准确度

#检验不同分类器和不同特征选择的结果（此处选择信息量最靠前的词作为机器学习的特征）
print 'BernoulliNB`s accuracy is %f' %clf_score(BernoulliNB())
print 'GaussianNB`s accuracy is %f' %clf_score(GaussianNB())
print 'MultinomiaNB`s accuracy is %f' %clf_score(MultinomialNB())
print 'LogisticRegression`s accuracy is %f' %clf_score(LogisticRegression())
print 'SVC`s accuracy is %f' %clf_score(SVC(gamma=0.001, C=100., kernel='linear'))
print 'LinearSVC`s accuracy is %f' %clf_score(LinearSVC())
print 'NuSVC`s accuracy is %f' %clf_score(NuSVC())
"""

# 5. After finding the best classifier, then check different dimension classification accuracy
def score(classifier):
    classifier = SklearnClassifier(classifier)
    classifier.train(trainset)
    pred = classifier.classify_many(test)
    return accuracy_score(tag_test, pred)

#dimention = ['500','1000','1500','2000','2500','3000']

#for d in dimention:
"""    d = '1500'
    word_scores = create_word_bigram_scores()
    best_words = find_best_words(word_scores, int(d))

    posFeatures = pos_features(best_word_features_com)
    negFeatures = neg_features(best_word_features_com)

    # Make the feature set ramdon
    shuffle(posFeatures)
    shuffle(negFeatures)

    # 75% of features used as training set (in fact, it have a better way by using cross validation function)
    size_pos = int(len(pos_review) * 0.75)
    size_neg = int(len(neg_review) * 0.75)

    trainset = posFeatures[:size_pos] + negFeatures[:size_neg]
    testset = posFeatures[size_pos:] + negFeatures[size_neg:]
    

    test, tag_test = zip(*testset)
    print 'Feature Dimention', d
    print 'BernoulliNB`s accuracy is %f' %score(BernoulliNB())
#  print 'GaussianNB`s accuracy is %f' %score(GaussianNB())
    print 'MultinomiaNB`s accuracy is %f' %score(MultinomialNB())
    print 'LogisticRegression`s accuracy is %f' %score(LogisticRegression())
    print 'SVC`s accuracy is %f' %score(SVC())
    print 'LinearSVC`s accuracy is %f' %score(LinearSVC())
    print 'NuSVC`s accuracy is %f' %score(NuSVC())
    print '\n'
    store_classifier(BernoulliNB(), trainset, "C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\sentiment_classifier_ZJX.pkl") 
"""

# 6. Store the best classifier under best dimension
def store_classifier(clf, trainset, filepath):
    classifier = SklearnClassifier(clf)
    classifier.train(trainset)
    # use pickle to store classifier
    pickle.dump(classifier, open(filepath,'w'))


"""
以下为测试运行代码
"""
d = '1500'#d是特征的维数
posFeatures = pos_features(best_word_features_com, int(d))
print d
negFeatures = neg_features(best_word_features_com, int(d))

    # Make the feature set ramdon
shuffle(posFeatures)
shuffle(negFeatures)

    # 75% of features used as training set (in fact, it have a better way by using cross validation function)
size_pos = int(len(pos_review) * 0.75)
size_neg = int(len(neg_review) * 0.75)
size_pos_train = int(len(pos_review))
size_neg_train = int(len(neg_review))

trainset = posFeatures[:size_pos_train] + negFeatures[:size_neg_train]
testset = posFeatures[size_pos:] + negFeatures[size_neg:]

test, tag_test = zip(*testset)
print 'Feature Dimention', d
print 'BernoulliNB`s accuracy is %f' %score(BernoulliNB())
#  print 'GaussianNB`s accuracy is %f' %score(GaussianNB())
print 'MultinomiaNB`s accuracy is %f' %score(MultinomialNB())
print 'LogisticRegression`s accuracy is %f' %score(LogisticRegression())
print 'SVC`s accuracy is %f' %score(SVC())
print 'LinearSVC`s accuracy is %f' %score(LinearSVC())
print 'NuSVC`s accuracy is %f' %score(NuSVC())
print '\n'
store_classifier(BernoulliNB(), trainset, "C:\JXZeng\summer_2016\sentiment\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Machine learning features\sentiment_classifier_ZJX0713.pkl")


