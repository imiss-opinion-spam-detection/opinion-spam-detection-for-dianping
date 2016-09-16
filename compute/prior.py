#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import date as date_class
from math import log as math_log
from time import time

from networkx import Graph

from compute.classes import User, Product, Review
from compute.lib import string_to_simhash, hamming_distance


# ----- Prior Calculation Func for User & Product & Review -----

# ----- Prior for User -----
# 0.prior_user_average_rating_deviation
# 1.prior_user_average_review_length
# 2.prior_user_burstiness
# 3.prior_user_content_similarity_average
# 4.prior_user_content_similarity_max
# 5.prior_user_entropy_rating_distribution
# 6.prior_user_max_number_review
# 7.prior_user_ratio_negative_review
# 8.prior_user_ratio_positive_review
# ----- Prior for Product -----
# 0.prior_product_average_rating_deviation
# 1.prior_product_average_review_length
# 2.prior_product_content_similarity_average
# 3.prior_product_content_similarity_max
# 4.prior_product_entropy_rating_distribution
# 5.prior_product_max_number_review
# 6.prior_product_ratio_negative_review
# 7.prior_product_ratio_positive_review
# ----- Prior for Review -----
# 0.prior_review_extremity_rating
# 1.prior_review_is_single_review
# 2.prior_review_rating_deviation
# 3.prior_review_ratio_of_exclamation_mark
# 4.prior_review_review_length


# ----- Prior for User -----

def prior_user_average_rating_deviation(graph=Graph(), user=User()):
    count_all = len(graph.neighbors(user))
    sum_sum_star = 0.0
    for review in graph.neighbors_iter(user):
        sum_sum_star += review.sum_star
    average = sum_sum_star / count_all
    deviation = 0.0
    for review in graph.neighbors_iter(user):
        deviation += abs(review.sum_star - average)
    average_deviation = deviation / count_all
    user.feature_value['average_rating_deviation'] = average_deviation


def prior_user_average_review_length(graph=Graph(), user=User()):
    length = 0.0
    count = len(graph.neighbors(user))
    for review in graph.neighbors_iter(user):
        length += len(review.text)
    average_length = length / count
    user.feature_value['average_review_length'] = average_length


def prior_user_burstiness(graph=Graph(), user=User()):
    max_date = date_class(year=2003, month=3, day=31)
    min_date = date_class.today()
    for review in graph.neighbors_iter(user):
        if review.date > max_date:
            max_date = review.date
        if review.date < min_date:
            min_date = review.date
    user.feature_value['burstiness'] = (max_date - min_date).days


def prior_user_content_similarity_average(graph=Graph(), user=User()):
    length = len(graph.neighbors(user))
    if length == 1:
        average_similarity = 256
    else:
        sum_similarity = 0
        for review in graph.neighbors_iter(user):
            try:
                review.text_fingerprint
            except AttributeError:
                review.text_fingerprint = string_to_simhash(review.text)
        for review_1 in graph.neighbors_iter(user):
            for review_2 in graph.neighbors_iter(user):
                if review_1 != review_2:
                    sum_similarity += hamming_distance(review_1.text_fingerprint, review_2.text_fingerprint)
        count = length * (length - 1)
        average_similarity = sum_similarity / count
    user.feature_value['content_similarity_average'] = average_similarity


def prior_user_content_similarity_max(graph=Graph(), user=User()):
    if len(graph.neighbors(user)) == 1:
        max_similarity = 256
    else:
        max_similarity = 512
        for review in graph.neighbors_iter(user):
            if not hasattr(review, "text_fingerprint")
                review.text_fingerprint = string_to_simhash(review.text)
        for review_1 in graph.neighbors_iter(user):
            for review_2 in graph.neighbors_iter(user):
                if review_1 != review_2:
                    this_similarity = hamming_distance(review_1.text_fingerprint, review_2.text_fingerprint)
                    if this_similarity < max_similarity:
                        max_similarity = this_similarity
    user.feature_value['content_similarity_max'] = max_similarity


def prior_user_entropy_rating_distribution(graph=Graph(), user=User()):
    star_list = [0, 0, 0, 0, 0]
    rating_entropy = 0
    star_number = 0
    # count the present times of each star rank from 0 to 4
    for review in graph.neighbors_iter(user):
        for star in review.star:
            star_list[star] += 1
            star_number += 1
    # calculate the entropy
    for star in star_list:
        if star != 0:
            rating_entropy += (star / star_number) * math_log(star / star_number)
    user.feature_value['entropy_rating_distribution'] = abs(rating_entropy)


def prior_user_max_number_review(graph=Graph(), user=User()):
    max_times = 0
    preview_times = dict()  # {date:times, ...}
    for review in graph.neighbors_iter(user):
        if review.date in preview_times:
            preview_times[review.date] += 1
        else:
            preview_times[review.date] = 1
    for date, times in preview_times.items():
        if times > max_times:
            max_times = times
    user.feature_value['max_number_review'] = max_times


def prior_user_ratio_positive_and_negative_review(graph=Graph(), user=User()):
    # Ratio of positive reviews (3-4 star)
    # Ratio of negative reviews (0-1 star)
    count_positive = 0.0
    count_negative = 0.0
    count_all = len(graph.neighbors(user))
    for review in graph.neighbors_iter(user):
        if review.sum_star >= 12:
            count_positive += 1.0
        if review.sum_star <= 6:
            count_negative += 1.0
    ratio_positive = count_positive / count_all
    ratio_negative = count_negative / count_all
    user.feature_value['ratio_negative_review'] = ratio_negative
    user.feature_value['ratio_positive_review'] = ratio_positive


# ----- Prior for Product -----

def prior_product_average_rating_deviation(graph=Graph(), product=Product()):
    count_all = len(graph.neighbors(product))
    sum_rating = 0.0
    for review in graph.neighbors_iter(product):
        sum_rating += review.sum_star
    average = sum_rating / count_all
    deviation = 0.0
    for review in graph.neighbors_iter(product):
        deviation += abs(review.sum_star - average)
    average_deviation = deviation / count_all
    product.feature_value['average_rating_deviation'] = average_deviation


def prior_product_average_review_length(graph=Graph(), product=Product()):
    length = 0.0
    count = len(graph.neighbors(product))
    for review in graph.neighbors_iter(product):
        length += len(review.text)
    average_length = length / count
    product.feature_value['average_review_length'] = average_length


def prior_product_content_similarity_average(graph=Graph(), product=Product()):
    length = len(graph.neighbors(product))
    if length == 1:
        average_similarity = 256
    else:
        sum_similarity = 0
        for review in graph.neighbors_iter(product):
            try:
                review.text_fingerprint
            except AttributeError:
                review.text_fingerprint = string_to_simhash(review.text)
        for review_1 in graph.neighbors_iter(product):
            for review_2 in graph.neighbors_iter(product):
                if review_1 != review_2:
                    sum_similarity += hamming_distance(review_1.text_fingerprint, review_2.text_fingerprint)
        count = length * (length - 1)
        average_similarity = sum_similarity / count
    product.feature_value['content_similarity_average'] = average_similarity


def prior_product_content_similarity_max(graph=Graph(), product=Product()):
    length = len(graph.neighbors(product))
    if length == 1:
        max_similarity = 256
    else:
        max_similarity = 512
        for review in graph.neighbors_iter(product):
            try:
                review.text_fingerprint
            except AttributeError:
                review.text_fingerprint = string_to_simhash(review.text)
        for review_1 in graph.neighbors_iter(product):
            for review_2 in graph.neighbors_iter(product):
                if review_1 != review_2:
                    this_similarity = hamming_distance(review_1.text_fingerprint, review_2.text_fingerprint)
                    if this_similarity < max_similarity:
                        max_similarity = this_similarity
    product.feature_value['content_similarity_max'] = max_similarity


def prior_product_entropy_rating_distribution(graph=Graph(), product=Product()):
    star_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    rating_entropy = 0.0
    star_number = 0.0
    # count the present times of each star rank from 0 to 4
    for review in graph.neighbors_iter(product):
        for star in review.star:
            star_list[star] += 1.0
            star_number += 1.0
    # calculate the entropy
    for star in star_list:
        if star != 0:
            rating_entropy += (star / star_number) * math_log(star / star_number)
    product.feature_value['entropy_rating_distribution'] = -rating_entropy


def prior_product_max_number_review(graph=Graph(), product=Product()):
    max_times = 0
    preview_times = dict()  # {datetime:times, ...}
    for review in graph.neighbors_iter(product):
        if review.date in preview_times:
            preview_times[review.date] += 1
        else:
            preview_times[review.date] = 1
    for times in preview_times.values():
        if times > max_times:
            max_times = times
    product.feature_value['max_number_review'] = max_times


def prior_product_ratio_positive_or_negative_review(graph=Graph(), product=Product()):
    # Ratio of positive reviews (3-4 star)
    # Ratio of negative reviews (0-1 star)
    count_positive = 0.0
    count_negative = 0.0
    count_all = len(graph.neighbors(product))
    for review in graph.neighbors_iter(product):
        if review.sum_star >= 9:
            count_positive += 1.0
        elif review.sum_star <= 3:
            count_negative += 1.0
    ratio_positive = (count_positive / count_all)
    ratio_negative = (count_negative / count_all)
    product.feature_value['ratio_negative_review'] = ratio_negative
    product.feature_value['ratio_positive_review'] = ratio_positive


# ----- Prior for Review -----

def prior_review_extremity_rating(review=Review()):
    extremity_star = 0
    for star in review.star:
        if star > 2:
            extremity_star += 1
    review.feature_value['extremity_rating'] = extremity_star


def prior_review_is_single_review(graph=Graph(), review=Review()):
    for node in graph.neighbors_iter(review):
        if node.__class__ == User().__class__:
            review.feature_value['is_single_review'] = 1 if len(graph.neighbors(node)) == 1 else 0
            break


def prior_review_rating_deviation(graph=Graph(), product=Product()):
    rating_all = 0.0
    rating_count = len(graph.neighbors(product))
    for review in graph.neighbors_iter(product):
        rating_all += review.sum_star
    average_rating = rating_all / rating_count
    for review in graph.neighbors_iter(product):
        review.feature_value['rating_deviation'] = abs(average_rating - review.sum_star)


def prior_review_ratio_exclamation_mark(review=Review()):
    exclamation_mark_number = 0.0
    exclamation_mark_number += review.text.count('!')  # For English
    exclamation_mark_number += review.text.count('！')  # For Chinese
    if len(review.text) != 0:
        review.feature_value['ratio_exclamation_mark'] = exclamation_mark_number / len(review.text)
    else:
        print('This review is strange:')
        print(review)
        review.feature_value['ratio_exclamation_mark'] = 0


def prior_review_review_length(review=Review()):
    review.feature_value['review_length'] = len(review.text)


# ----- Calculate Class Prior Probability for whole Graph -----

def set_prior(graph=Graph()):
    start_time = time()
    print('Computing Prior')

    # Generate Statistics Lists for empirical cumulative distribution function

    prior_user_statistic = dict()
    prior_user_statistic['average_rating_deviation'] = list()
    prior_user_statistic['average_review_length'] = list()
    prior_user_statistic['burstiness'] = list()
    prior_user_statistic['content_similarity_average'] = list()
    prior_user_statistic['content_similarity_max'] = list()
    prior_user_statistic['entropy_rating_distribution'] = list()
    prior_user_statistic['max_number_review'] = list()
    prior_user_statistic['ratio_negative_review'] = list()
    prior_user_statistic['ratio_positive_review'] = list()

    prior_product_statistic = dict()
    prior_product_statistic['average_rating_deviation'] = list()
    prior_product_statistic['average_review_length'] = list()
    prior_product_statistic['content_similarity_average'] = list()
    prior_product_statistic['content_similarity_max'] = list()
    prior_product_statistic['entropy_rating_distribution'] = list()
    prior_product_statistic['max_number_review'] = list()
    prior_product_statistic['ratio_positive_review'] = list()
    prior_product_statistic['ratio_negative_review'] = list()

    prior_review_statistic = dict()
    prior_review_statistic['extremity_rating'] = list()
    prior_review_statistic['is_single_review'] = list()
    prior_review_statistic['rating_deviation'] = list()
    prior_review_statistic['ratio_exclamation_mark'] = list()
    prior_review_statistic['review_length'] = list()

    prior_statistic = [prior_user_statistic, prior_product_statistic, prior_review_statistic]

    # Calculate Feature Values

    for node in graph.nodes_iter():
        if isinstance(node, User):
            prior_user_average_rating_deviation(graph, node)
            prior_user_statistic['average_rating_deviation'].append(node.feature_value['average_rating_deviation'])

            prior_user_average_review_length(graph, node)
            prior_user_statistic['average_review_length'].append(node.feature_value['average_review_length'])

            prior_user_burstiness(graph, node)
            prior_user_statistic['burstiness'].append(node.feature_value['burstiness'])

            prior_user_content_similarity_average(graph, node)
            prior_user_statistic['content_similarity_average'].append(node.feature_value['content_similarity_average'])

            prior_user_content_similarity_max(graph, node)
            prior_user_statistic['content_similarity_max'].append(node.feature_value['content_similarity_max'])

            prior_user_entropy_rating_distribution(graph, node)
            prior_user_statistic['entropy_rating_distribution'].append(
                node.feature_value['entropy_rating_distribution'])

            prior_user_max_number_review(graph, node)
            prior_user_statistic['max_number_review'].append(node.feature_value['max_number_review'])

            prior_user_ratio_positive_and_negative_review(graph, node)
            prior_user_statistic['ratio_negative_review'].append(node.feature_value['ratio_negative_review'])
            prior_user_statistic['ratio_positive_review'].append(node.feature_value['ratio_positive_review'])

        elif isinstance(node, Product):
            prior_product_average_rating_deviation(graph, node)
            prior_product_statistic['average_rating_deviation'].append(node.feature_value['average_rating_deviation'])

            prior_product_average_review_length(graph, node)
            prior_product_statistic['average_review_length'].append(node.feature_value['average_review_length'])

            prior_product_content_similarity_average(graph, node)
            prior_product_statistic['content_similarity_average'].append(
                node.feature_value['content_similarity_average'])

            prior_product_content_similarity_max(graph, node)
            prior_product_statistic['content_similarity_max'].append(node.feature_value['content_similarity_max'])

            prior_product_entropy_rating_distribution(graph, node)
            prior_product_statistic['entropy_rating_distribution'].append(
                node.feature_value['entropy_rating_distribution'])

            prior_product_max_number_review(graph, node)
            prior_product_statistic['max_number_review'].append(node.feature_value['max_number_review'])

            prior_product_ratio_positive_or_negative_review(graph, node)
            prior_product_statistic['ratio_positive_review'].append(node.feature_value['ratio_positive_review'])
            prior_product_statistic['ratio_negative_review'].append(node.feature_value['ratio_negative_review'])

            prior_review_rating_deviation(graph, node)
            for review in graph.neighbors_iter(node):
                prior_review_statistic['rating_deviation'].append(review.feature_value['rating_deviation'])

        elif isinstance(node, Review):
            prior_review_extremity_rating(node)
            prior_review_statistic['extremity_rating'].append(node.feature_value['extremity_rating'])

            prior_review_is_single_review(graph, node)
            prior_review_statistic['is_single_review'].append(node.feature_value['is_single_review'])

            prior_review_ratio_exclamation_mark(node)
            prior_review_statistic['ratio_exclamation_mark'].append(node.feature_value['ratio_exclamation_mark'])

            prior_review_review_length(node)
            prior_review_statistic['review_length'].append(node.feature_value['review_length'])

        else:
            raise NameError

    for statistic_dict in prior_statistic:
        for statistic_list in statistic_dict.values():
            statistic_list.sort()

    # Calculate Prior
    for node in graph.nodes_iter():
        if isinstance(node, User):
            sum_f = 0
            sum_f += (1 - prior_user_statistic['average_rating_deviation'].index(
                node.feature_value['average_rating_deviation']) /
                      len(prior_user_statistic['average_rating_deviation'])) ** 2
            sum_f += (prior_user_statistic['average_review_length'].index(
                node.feature_value['average_review_length']) /
                      len(prior_user_statistic['average_review_length'])) ** 2
            sum_f += (1 - prior_user_statistic['burstiness'].index(
                node.feature_value['burstiness']) /
                      len(prior_user_statistic['burstiness'])) ** 2
            sum_f += (prior_user_statistic['content_similarity_average'].index(
                node.feature_value['content_similarity_average']) /
                      len(prior_user_statistic['content_similarity_average'])) ** 2
            sum_f += (prior_user_statistic['content_similarity_max'].index(
                node.feature_value['content_similarity_max']) /
                      len(prior_user_statistic['content_similarity_max'])) ** 2
            sum_f += (prior_user_statistic['entropy_rating_distribution'].index(
                node.feature_value['entropy_rating_distribution']) /
                      len(prior_user_statistic['entropy_rating_distribution'])) ** 2
            sum_f += (1 - prior_user_statistic['max_number_review'].index(
                node.feature_value['max_number_review']) /
                      len(prior_user_statistic['max_number_review'])) ** 2
            sum_f += (1 - prior_user_statistic['ratio_negative_review'].index(
                node.feature_value['ratio_negative_review']) /
                      len(prior_user_statistic['ratio_negative_review'])) ** 2
            sum_f += (1 - prior_user_statistic['ratio_positive_review'].index(
                node.feature_value['ratio_positive_review']) /
                      len(prior_user_statistic['ratio_positive_review'])) ** 2
            node.prior[0] = (sum_f / 9) ** 0.5
            node.prior[1] = 1 - node.prior[0]

        elif isinstance(node, Product):
            sum_f = 0
            sum_f += (1 - prior_product_statistic['average_rating_deviation'].index(
                node.feature_value['average_rating_deviation']) /
                      len(prior_product_statistic['average_rating_deviation'])) ** 2
            sum_f += (prior_product_statistic['average_review_length'].index(
                node.feature_value['average_review_length']) /
                      len(prior_product_statistic['average_review_length'])) ** 2
            sum_f += (prior_product_statistic['content_similarity_average'].index(
                node.feature_value['content_similarity_average']) /
                      len(prior_product_statistic['content_similarity_average'])) ** 2
            sum_f += (prior_product_statistic['content_similarity_max'].index(
                node.feature_value['content_similarity_max']) /
                      len(prior_product_statistic['content_similarity_max'])) ** 2
            sum_f += (prior_product_statistic['entropy_rating_distribution'].index(
                node.feature_value['entropy_rating_distribution']) /
                      len(prior_product_statistic['entropy_rating_distribution'])) ** 2
            sum_f += (1 - prior_product_statistic['max_number_review'].index(
                node.feature_value['max_number_review']) /
                      len(prior_product_statistic['max_number_review'])) ** 2
            sum_f += (1 - prior_product_statistic['ratio_negative_review'].index(
                node.feature_value['ratio_negative_review']) /
                      len(prior_product_statistic['ratio_negative_review'])) ** 2
            sum_f += (1 - prior_product_statistic['ratio_positive_review'].index(
                node.feature_value['ratio_positive_review']) /
                      len(prior_product_statistic['ratio_positive_review'])) ** 2
            node.prior[0] = (sum_f / 8) ** 0.5
            node.prior[1] = 1 - node.prior[0]

        elif isinstance(node, Review):
            sum_f = 0
            sum_f += (1 - prior_review_statistic['extremity_rating'].index(
                node.feature_value['extremity_rating']) /
                      len(prior_review_statistic['extremity_rating'])) ** 2
            sum_f += (1 - prior_review_statistic['is_single_review'].index(
                node.feature_value['is_single_review']) /
                      len(prior_review_statistic['is_single_review'])) ** 2
            sum_f += (1 - prior_review_statistic['rating_deviation'].index(
                node.feature_value['rating_deviation']) /
                      len(prior_review_statistic['rating_deviation'])) ** 2
            sum_f += (1 - prior_review_statistic['ratio_exclamation_mark'].index(
                node.feature_value['ratio_exclamation_mark']) /
                      len(prior_review_statistic['ratio_exclamation_mark'])) ** 2
            sum_f += (prior_review_statistic['review_length'].index(
                node.feature_value['review_length']) /
                      len(prior_review_statistic['review_length'])) ** 2
            node.prior[0] = (sum_f / 5) ** 0.5
            node.prior[1] = 1 - node.prior[0]

    print('Priors is Ready')
    print('Time Spent on Computing Prior : %f' % (time() - start_time))
