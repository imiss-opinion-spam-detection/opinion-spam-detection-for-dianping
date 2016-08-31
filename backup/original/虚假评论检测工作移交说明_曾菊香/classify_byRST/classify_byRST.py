#! /usr/bin/env python2.7
#coding=utf-8

import codecs

from backup.original.虚假评论检测工作移交说明_曾菊香.分词判断 import textprocessing as tp

" 将有rst和没有rst的评论进行分离，同时对具有rst的评论直接利用rst进行情感极性判断"
# loading data
review = tp.get_excel_data(r"C:\JXZeng\summer_2016\sentiment\review_TEST_22o\review.xlsx", 1, 1, "data")
rst1 = tp.get_excel_data(r"C:\JXZeng\summer_2016\sentiment\review_TEST_22o\review.xlsx", 1, 2, "data")
rst2 = tp.get_excel_data(r"C:\JXZeng\summer_2016\sentiment\review_TEST_22o\review.xlsx", 1, 3, "data")
rst3 = tp.get_excel_data(r"C:\JXZeng\summer_2016\sentiment\review_TEST_22o\review.xlsx", 1, 4, "data")

size = int(len(review))
f_noneRst = codecs.open("noneRstReview.xlsx", 'w', 'utf-8')
f_RstPos = codecs.open("RstReviewPos.xlsx", 'w', 'utf-8')
f_RstNeg = codecs.open("RstReviewNeg.xlsx", 'w', 'utf-8')
f_Rst = codecs.open("RstReview.xlsx", 'w', 'utf-8')
for i in range(0, size):
    if type(rst3[i]) !=  unicode:
        avg = "{:.3f}".format((float(rst1[i])+float(rst2[i])+float(rst3[i]))/3.0)
        f_Rst.write(review[i]+'\t'+str(rst1[i])+'\t'+str(rst2[i])+'\t'+str(rst3[i])+'\t'+str(avg)+'\n')
        if float(avg) >= 2.0:
            f_RstPos.write(review[i] + '\t' + str(rst1[i]) + '\t' + str(rst2[i]) + '\t' + str(rst3[i]) + '\t' + str(avg) + '\n')
        else:
            f_RstNeg.write(review[i] + '\t' + str(rst1[i]) + '\t' + str(rst2[i]) + '\t' + str(rst3[i]) + '\t' + str(avg) + '\n')
    else:
        f_noneRst.write(review[i] + '\n')
f_Rst.flush()
f_Rst.close()
f_RstPos.flush()
f_RstPos.close()
f_RstNeg.flush()
f_RstNeg.close()
f_noneRst.flush()
f_noneRst.close()