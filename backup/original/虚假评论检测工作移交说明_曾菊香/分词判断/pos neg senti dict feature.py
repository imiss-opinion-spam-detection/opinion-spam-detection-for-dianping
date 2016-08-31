#! /usr/bin/env python2.7
#coding=utf-8

"""
Compute a review's positive and negative score, their average score and standard deviation.
This module aim to extract review positive/negative score, average score and standard deviation features (all 6 features).
Sentiment analysis based on sentiment dictionary.

"""
from xlutils.copy import copy
import xlrd
import xlwt
import numpy as np
import textprocessing as tp
from textprocessing import extract



# 1. Load dictionary and dataset
# Load sentiment dictionary
posdict = tp.get_txt_data(r'C:\Python27\positiveandnegativedictionary\posdict.txt','lines')
negdict = tp.get_txt_data(r'C:\Python27\positiveandnegativedictionary\negdict.txt','lines')

# Load adverbs of degree dictionary
mostdict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\most.txt', 'lines')
verydict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\very.txt', 'lines')
moredict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\more.txt', 'lines')
ishdict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\ish.txt', 'lines')
insufficientdict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\insufficiently.txt', 'lines')
inversedict = tp.get_txt_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\sentiment dictionary\adverbs of degree dictionary\inverse.txt', 'lines')

# Load dataset
extract(r'C:\Python27\a.txt')
review = tp.get_excel_data(r'C:\Python27\review.xlsx', "1", "1", "data")
#review = tp.get_excel_data(r'C:\Python27\Review-Helpfulness-Prediction-master\main\Reviewset\review1.xlsx', "1", "2", "data")


# 2. Sentiment dictionary analysis basic function
# Function of matching adverbs of degree and set weights 设置不同词库的词语进行加权处理
def match(word, sentiment_value):#输入词语以及情感类型特征（poscount or negcount）
	if word in mostdict:
		sentiment_value *= 2.0
	elif word in verydict:
	    sentiment_value *= 1.5
	elif word in moredict:
	    sentiment_value *= 1.25
	elif word in ishdict:
	    sentiment_value *= 0.5
	elif word in insufficientdict:
	    sentiment_value *= 0.25
	elif word in inversedict:
	    sentiment_value *= -1
	return sentiment_value

# Function of transforming negative score to positive score 积极与消极分数的变换
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
    pos_count = 0
    neg_count = 0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return [pos_count, neg_count]


# 3.1 Single review's positive and negative score
# Function of calculating review's every sentence sentiment score 计算每个句子的得分
def sumup_sentence_sentiment_score(score_list):
	score_array = np.array(score_list) # Change list to a numpy array 生成numpy数组列表
	Pos = np.sum(score_array[:,0]) # Compute positive score
	Neg = np.sum(score_array[:,1])
	AvgPos = np.mean(score_array[:,0]) # Compute review positive average score, average score = score/sentence number
	AvgNeg = np.mean(score_array[:,1])
	StdPos = np.std(score_array[:,0]) # Compute review positive standard deviation score
	StdNeg = np.std(score_array[:,1])

	return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]

def single_review_sentiment_score(review):
	single_review_senti_score = []
	cuted_review = tp.cut_sentence_2(review)

	for sent in cuted_review:
		seg_sent = tp.segmentation(sent, 'list') # 进行分词
		i = 0 # word position counter
		s = 0 # sentiment word position
		poscount = 0 # count a positive word
		negcount = 0 # count a negative word

		for word in seg_sent:
		    if word in posdict:
		        poscount += 1
		        for w in seg_sent[s:i]:
		           poscount = match(w, poscount) # 取得初始积极分数
		        a = i + 1

		    elif word in negdict:
		        negcount += 1
		        for w in seg_sent[s:i]:
		        	negcount = match(w, negcount) # 取得初始消极分数
		        a = i + 1

		    # Match "!" in the review, every "!" has a weight of +2
		    elif word == "！".decode('utf8') or word == "!".decode('utf8'):
		        for w2 in seg_sent[::-1]:
		            if w2 in posdict:
		            	poscount += 2
		            	break
		            elif w2 in negdict:
		                negcount += 2
		                break                    
		    i += 1

		single_review_senti_score.append(transform_to_positive_num(poscount, negcount))
		review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)

	return review_sentiment_score

# Testing
# print single_review_sentiment_score(review[0])



# 3.2 All review dataset's sentiment score 对于所有数据集的情感分数计算
def sentence_sentiment_score(dataset):
    cuted_review = [] # 建立空数组
    for cell in dataset:
        cuted_review.append(tp.cut_sentence_2(cell)) # 进行句子切割算法 将sents放入数组

    single_review_count = []
    all_review_count = []
    for review in cuted_review:
        for sent in review:
            seg_sent = tp.segmentation(sent, 'list') # 进行分词
            i = 0 #word position counter
            a = 0 #sentiment word position
            poscount = 0 #count a pos word
            negcount = 0
            for word in seg_sent:
                if word in posdict:
                    poscount += 1                
                    for w in seg_sent[a:i]:
                        poscount = match(w, poscount)
                    a = i + 1

                elif word in negdict:
                    negcount += 1
                    for w in seg_sent[a:i]:
                        negcount = match(w, negcount)
                    a = i + 1

                elif word == '！'.decode('utf8') or word == '!'.decode('utf8'):
                    for w2 in seg_sent[::-1]:
                        if w2 in posdict:
                        	poscount += 2
                        	break
                        elif w2 in negdict:
                            negcount += 2
                            break                    
                i += 1
                
            single_review_count.append(transform_to_positive_num(poscount, negcount)) #[[s1_score], [s2_score], ...]
        all_review_count.append(single_review_count) # [[[s11_score], [s12_score], ...], [[s21_score], [s22_score], ...], ...]
        single_review_count = []    

    return all_review_count

# Compute a single review's sentiment score
def all_review_sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        score_array = np.array(review) # 创建数组
        Pos = np.sum(score_array[:,0]) # 第零列为对于每一个词的积极分数
        Neg = np.sum(score_array[:,1]) # 第一列为对于每一个词的消极分数
        AvgPos = np.mean(score_array[:,0])
        AvgPos = round(AvgPos,2)
        AvgNeg = np.mean(score_array[:,1])
        AvgNeg = round(AvgNeg,2)
        StdPos = np.std(score_array[:,0])
        StdPos = round(StdPos,2)
        StdNeg = np.std(score_array[:,1])
        StdNeg = round(StdNeg,2)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
    return score

# Testing
#for i in all_review_sentiment_score(sentence_sentiment_score(review)):
#	print i



# 4. Store sentiment dictionary features
def store_sentiment_dictionary_score(review_set, storepath):
	sentiment_score = all_review_sentiment_score(sentence_sentiment_score(review_set))
	table = xlrd.open_workbook(storepath)
	table = copy(table)
	sheet = table.get_sheet(0)
	j=0
	for i in sentiment_score:
	    sheet.write(j,1,str(i[0]))
	    sheet.write(j,2,str(i[1]))
	    sheet.write(j,3,str(i[2]))
	    sheet.write(j,4,str(i[3]))
	    sheet.write(j,5,str(i[4]))
	    sheet.write(j,6,str(i[5]))
	    j+=1
	table.save('review2.xlsx')
#store_sentiment_dictionary_score(review,r'C:\Python27\Review-Helpfulness-Prediction-master\main\Reviewset\review1.xlsx')
store_sentiment_dictionary_score(review,r'C:\Python27\Review-Helpfulness-Prediction-master\main\Feature extraction module\Sentiment features\Sentiment dictionary features\review.xlsx')
