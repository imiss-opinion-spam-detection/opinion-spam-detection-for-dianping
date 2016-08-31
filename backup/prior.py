# -*- coding: <UTF-8> -*-

import networkx as nx
from data_structure import *
import math
import datetime
import pynlpir

# --- for user ---

class PriorUser(object):
    @staticmethod
    def max_number_review(graph=nx.Graph(), user=User()):
        # Max. number of reviews written in a day
        max_times = 0
        preview_times = {}  # {datetime:number, ...}
        for review in graph.neighbors(user):
            if review.date in preview_times:
                preview_times[review.date] += 1
            else:
                preview_times[review.date] = 1
        for date, times in preview_times.items():
            if times > max_times:
                max_times = times
        # cumulative distribution function from imagination, need to be exp.
        # more times, more suspicious
        user.processing_value.append(max_times)

    @staticmethod
    def ratio_positive_and_negative_review(graph=nx.Graph(), user=User()):
        # Ratio of positive reviews (4-5 star)
        # Ratio of negative reviews (1-2 star)
        count_positive = 0.0
        count_negative = 0.0
        count_all = len(graph.neighbors(user))
        for review in graph.neighbors(user):
            if review.sum_rst >= 12:
                count_positive += 1.0
            if review.sum_rst <= 6:
                count_negative += 1.0
        # larger means
        ratio_positive = (count_positive / count_all)
        ratio_negative = (count_negative / count_all)
        # optimize later
        user.processing_value.append(ratio_positive)
        user.processing_value.append(ratio_negative)

    @staticmethod
    def avg_rating_deviation(graph=nx.Graph(), user=User()):
        # Avg. rating deviation
        # ping jun cha
        count_all = len(graph.neighbors(user))
        sum_sum_rst = 0.0
        for review in graph.neighbors(user):
            sum_sum_rst += review.sum_rst
        average = sum_sum_rst / count_all
        deviation = 0.0
        for review in graph.neighbors(user):
            deviation += math.fabs(review.sum_rst - average)
        average_deviation = deviation / count_all
        user.processing_value.append(average_deviation)

    #
    # def weighted_rating_deviation(graph=nx.Graph(), user=User()):
    #     pass

    @staticmethod
    def burstiness(graph=nx.Graph(), user=User()):
        max_date = datetime.date(year=2003, month=3, day=31)
        min_date = datetime.date.today()
        for review in graph.neighbors(user):
            if review.date > max_date:
                max_date = review.date
            if review.date < min_date:
                min_date = review.date
        bst = (max_date - min_date).days
        user.processing_value.append(bst)


    @staticmethod
    def entropy_rating_distribution(graph=nx.Graph(), user=User()):
        neighbor = graph.neighbors(user)
        rst_list = [0,0,0,0,0]
        rating_entropy = 0
        rst_number = 0
        # count the present times of each rst rank from 0 to 4
        for review in neighbor:
            for rst in review.rst:
                rst_list[rst]+=1
                rst_number+=1
        # calculate the entropy
        for rst in rst_list:
            rating_entropy += (rst/rst_number)*math.log(rst/rst_number,math.e)

        user.processing_value.append(rating_entropy)


    # def entropy_temporal_gaps(graph=nx.Graph(), user=User()):
    #     pass


    @staticmethod
    def avg_review_length(graph=nx.Graph(), user=User()):
        length = 0.0
        count = len(graph.neighbors(user))
        for review in graph.neighbors(user):
            length += len(review.text)
        average_length = length / count

        user.processing_value.append(average_length)


    @staticmethod
    def calc_content_similarity(text1,text2):
        key_word = {}
        pynlpir.open()
        # get key_word and init the frequence
        list1 = pynlpir.segment(text1)
        list2 = pynlpir.segment(text2)
        for i in list1:
            key_word[i[0]] = [0,0]
        for i in list2:
            key_word[i[0]] = [0,0]
        pynlpir.close()
        # calc the frequence of key words
        for i in list1:
            key_word[i[0]][0] += 1
        for i in list2:
            key_word[i[0]][1] += 1
        # calc the similarity
        dot_product = 0
        vector_length1 = 0
        vector_length2 = 0
        for key,value in key_word.items():
            dot_product += value[0] * value[1]
            vector_length1 += value[0] ** 2
            vector_length2 += value[1] ** 2
        similarity = dot_product / ((vector_length1 ** 0.5)*(vector_length2 ** 0.5))
        return similarity


    @staticmethod
    def avg_content_similarity(self,graph=nx.Graph(), user=User()):
        review = graph.neighbors(user)
        count = len(review)
        total_review_similarity = 0
        for i in review:
            for j in review:
                total_review_similarity += self.calc_content_similarity(i.text,j.text)
        user.processing_value.append(total_review_similarity/(count**2))


    @staticmethod
    def max_content_similarity(self,graph=nx.Graph(), user=User()):
        review = graph.neighbors(user)
        max_content_similarity = -1
        for i in review:
            for j in review:
                if self.calc_content_similarity(i.text,j.text) > max_content_similarity:
                    max_content_similarity = max_content_similarity
        user.processing_value.append(max_content_similarity)

# --- for product ---

class PriorProduct(object):
    @staticmethod
    def max_number_review(graph=nx.Graph(), product=Product()):
        # Max. number of reviews written in a day
        max_times = 0
        preview_times = {}  # {datetime:number, ...}
        for review in graph.neighbors(product):
            if review.date in preview_times:
                preview_times[review.date] += 1
            else:
                preview_times[review.date] = 1
        for date, times in preview_times.items():
            if times > max_times:
                max_times = times
        # cumulative distribution function from imagination, need to be exp.
        # more times, more suspicious
        product.processing_value.append(max_times)

    @staticmethod
    def ratio_positive_or_negative_review(graph=nx.Graph(), product=Product()):
        # Ratio of positive reviews (4-5 star)
        # Ratio of negative reviews (1-2 star)
        count_positive = 0.0
        count_negative = 0.0
        count_all = len(graph.neighbors(product))
        for review in graph.neighbors(product):
            if review.sum_rst >= 9:
                count_positive += 1.0
            if review.sum_rst <= 3:
                count_negative += 1.0
        # larger means
        ratio_positive = (count_positive / count_all)
        ratio_negative = (count_negative / count_all)
        # optimize later
        product.processing_value.append(ratio_positive)
        product.processing_value.append(ratio_negative)

    @staticmethod
    def avg_rating_deviation(graph=nx.Graph(), product=Product()):
        # Avg. rating deviation
        # ping jun cha
        count_all = len(graph.neighbors(product))
        sum_rating = 0.0
        for review in graph.neighbors(product):
            sum_rating += review.sum_rst
        average = sum_rating / count_all
        deviation = 0.0
        for review in graph.neighbors(product):
            deviation += math.fabs(review.sum_rst - average)
        average_deviation = deviation / count_all
        product.processing_value.append(average_deviation)

    # def weighted_rating_deviation(graph=nx.Graph(), product=Product()):
    #     pass

    @staticmethod
    def entropy_rating_distribution(graph=nx.Graph(), product=Product()):
        neighbor = graph.neighbors(product)
        rst_list = [0.0, 0.0, 0.0, 0.0, 0.0]
        rating_entropy = 0.0
        rst_number = 0.0
        # count the present times of each rst rank from 0 to 4
        for review in neighbor:
            for rst in review.rst:
                rst_list[rst] += 1.0
                rst_number += 1.0
        # calculate the entropy
        for rst in rst_list:
            rating_entropy += (rst / rst_number) * math.log(rst / rst_number, math.e)

        product.processing_value.append(rating_entropy)

    # def entropy_temporal_gaps(graph=nx.Graph(), product=product()):
    #     pass

    @staticmethod
    def avg_review_length(graph=nx.Graph(), product=Product()):
        length = 0.0
        count = len(graph.neighbors(product))
        for review in graph.neighbors(product):
            length += len(review.text)
        average_length = length / count
        product.processing_value.append(average_length)

    @staticmethod
    def calc_content_similarity(text1, text2):
        key_word = {}
        pynlpir.open()
        # get key_word and init the frequence
        list1 = pynlpir.segment(text1)
        list2 = pynlpir.segment(text2)
        for i in list1:
            key_word[i[0]] = [0, 0]
        for i in list2:
            key_word[i[0]] = [0, 0]
        pynlpir.close()
        # calc the frequence of key words
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

    @staticmethod
    def avg_content_similarity(self, graph=nx.Graph(),  product=Product()):
        review = graph.neighbors(product)
        count = len(review)
        total_review_similarity = 0
        for i in review:
            for j in review:
                total_review_similarity += self.calc_content_similarity(i.text, j.text)
        product.processing_value.append(total_review_similarity / (count ** 2))

    @staticmethod
    def max_content_similarity(self, graph=nx.Graph(),  product=Product()):
        review = graph.neighbors(product)
        max_content_similarity = -1
        for i in review:
            for j in review:
                if self.calc_content_similarity(i.text, j.text) > max_content_similarity:
                    max_content_similarity = max_content_similarity
        product.processing_value.append(max_content_similarity)


# ----- for review -----

class PriorReview(object):
    # def rank_order(graph=nx.Graph(), review=Review()):
    #     pass

    @staticmethod
    def rating_deviation(graph=nx.Graph(), product=Product()):
        rating_all = 0.0
        rating_count = len(graph.neighbors(product))
        for review in graph.neighbors(product):
            rating_all += review.sum_rst
        avg_rating = rating_all / rating_count
        for review in graph.neighbors(product):
            review.temp_rating_deviation = math.fabs(avg_rating - review.sum_rst)

    @staticmethod
    def extremity_rating(graph=nx.Graph(), review=Review()):
        extremity_rst = 0
        for rst in review.rst:
            if rst > 2:
                extremity_rst += 1
        review.processing_value.append(extremity_rst)


    # def thresholded_rating_deviation(graph=nx.Graph(), review=Review()):
    #     pass
    # def early_time_frame(graph=nx.Graph()):
    #     early = 100
    #     earliest_date = datetime.date.today()

    @staticmethod
    def is_single_review(graph=nx.Graph(), review=Review()):
        # can be better defined
        for node in graph.neighbors(review):
            if node.__class__ == User().__class__:
                if len(graph.neighbors(node)) == 1:
                    review.processing_value.append(1)
                else:
                    review.processing_value.append(0)
                break

    @staticmethod
    def review_length(graph=nx.Graph(), review=Review()):
        length = len(review.text)
        review.processing_value.append(length)


    @staticmethod
    def ratio_of_exclamation_mark (graph=nx.Graph(), review=Review()):
        Exclamation_Mark_Number = 0
        Exclamation_Mark_Number += review.text.count('!') # For English
        Exclamation_Mark_Number += review.text.count('！')# For Chinese
        review.processing_value.append(Exclamation_Mark_Number)

# --- now we compute class prior probability ---

# def set_prior_class_probabilities(graph=nx.Graph()):
#     for node in graph.nodes():
#         if node.__class__ == User().__class__:
#             PriorUser.max_number_review(graph, node)
#             PriorUser.ratio_positive_and_negative_review(graph, node)
#             PriorUser.avg_rating_deviation(graph, node)
#             PriorUser.burstiness(graph, node)
#             PriorUser.avg_review_length(graph, node)
#         elif node.__class__ == Product().__class__:
#             PriorProduct.max_number_review(graph, node)
#             PriorProduct.ratio_positive_or_negative_review(graph, node)
#             PriorProduct.avg_rating_deviation(graph, node)
#             PriorProduct.avg_review_length(graph, node)
#             PriorReview.rating_deviation(graph, node)
#         elif node.__class__ == Review().__class__:
#             PriorReview.is_single_review(graph, node)
#             PriorReview.review_length(graph, node)
#     n_prior = {User().__class__: 5, Product().__class__: 4, Review().__class__: 3}
#     for node in graph.nodes():
#         node.prior[1] = 1 - node.prior[1] / n_prior[node.__class__]
#         node.prior[0] = 1 - node.prior[1]
