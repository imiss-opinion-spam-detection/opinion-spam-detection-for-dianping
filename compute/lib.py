#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib

import jieba
import pynlpir


def calc_content_similarity(text1='', text2='') -> int:
    key_word = dict()
    pynlpir.open()
    # get key_word and init the frequency
    list1 = pynlpir.segment(text1)
    list2 = pynlpir.segment(text2)
    for i in list1:
        key_word[i[0]] = [0, 0]
    for i in list2:
        key_word[i[0]] = [0, 0]
    pynlpir.close()
    # calc the frequency of key words
    for i in list1:
        key_word[i[0]][0] += 1
    for i in list2:
        key_word[i[0]][1] += 1
    # calc the similarity
    dot_product = 0
    vector_length1 = 0
    vector_length2 = 0
    for key, value in key_word.items():
        dot_product += value[0] * value[1]
        vector_length1 += value[0] ** 2
        vector_length2 += value[1] ** 2
    similarity = dot_product / ((vector_length1 ** 0.5) * (vector_length2 ** 0.5))
    return similarity


def cut_string(string=''):
    jieba.initialize()
    if __name__ == '__main__':
        print(jieba.lcut(string))
    return jieba.lcut(string)


def string_to_simhash(string='', digit=512):
    def string_to_hash(_string=''):
        return int(hashlib.sha512(_string.encode('utf-8')).hexdigest(), 16)

    word_list = cut_string(string)
    weight_add = [0] * digit
    fingerprint = [0] * digit
    for word in word_list:
        this_hash = string_to_hash(word)
        if __name__ == '__main__':
            # print(this_hash)
            print(bin(this_hash))
        this_weight = 1
        for i in range(digit):
            if (this_hash >> (digit - i - 1)) & 1:
                weight_add[i] += this_weight
            else:
                weight_add[i] -= this_weight
    for i in range(digit):
        fingerprint[i] = 1 if weight_add[i] > 0 else 0
    if __name__ == '__main__':
        print(weight_add)
        print(fingerprint)
    return fingerprint


def hamming_distance(simhash_1, simhash_2, digit=512):
    dist = 0
    for i in range(digit):
        if simhash_1[i] ^ simhash_2[i]:
            dist += 1
    return dist


def cmp_string_by_simhash(string_1='', string_2=''):
    return hamming_distance(string_to_simhash(string_1), string_to_simhash(string_2))

# if __name__ == '__main__':
#     print(cmp_string_by_simhash('我到河北省来, Google 用此算法来分析文本相似度，识别爬虫获取的网页是否与它庞大的、数以十亿计的网页库是否重复的算法。',
#                                 '我到河南省来, Google 用此算法来分析文本相似度，识别爬虫获取的网页是否与它庞大的、数以十亿计的网页库是否重复的算法。'))
#     print()
#     print(cmp_string_by_simhash('我到河北省来',
#                                 '我到河南省来'))
#     print()
#     print(cmp_string_by_simhash('我到河北省来',
#                                 'Google 用此算法来分析文本相似度，识别爬虫获取的网页是否与它庞大的、数以十亿计的网页库是否重复的算法。'))
