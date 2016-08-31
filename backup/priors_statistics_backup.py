# -*- coding: <UTF-8> -*-

from networkx import Graph
from prior import PriorUser, PriorReview, PriorProduct

from compute.classes import User, Review, Product


# Compatible for this kind of prior processing functions:

# def max_number_review(graph= Graph(), user=User()):
#     # Max. number of reviews written in a day
#     max_times = 0
#     preview_times = {}  # {datetime:number, ...}
#     for review in graph.neighbors(user):
#         if review.date in preview_times:
#             preview_tim¬les[review.date] += 1
#         else:
#             preview_times[review.date] = 1
#     for date, times in preview_times.iteritems():
#         if times > max_times:
#             max_times = times
#     # cumulative distribution function from imagination, need to be exp.
#     # more times, more suspicious
#     user.processing_value.append(max_times)

def init_priors(graph=Graph()):
    print("Computing Priors")

    # Priors lists definition
    prior_user_avg_rating_deviation_list = []
    prior_user_ratio_positive_review_list = []
    prior_user_ratio_negative_review_list = []
    prior_user_max_number_review_list = []
    prior_user_burstiness_list = []
    prior_user_avg_review_length_list = []

    prior_product_avg_rating_deviation_list = []
    prior_product_max_number_review_list = []
    prior_product_avg_review_length_list = []
    prior_product_ratio_positive_review_list = []
    prior_product_ratio_negative_review_list = []

    prior_review_rating_deviation_list = []
    prior_review_is_single_review_list = []
    prior_review_review_length_list = []

    # Empirical cumulative distribution function generation
    for node in graph.nodes():

        node.processing_value = []
        if node.__class__ == User().__class__:

            # print('1 node.processing_value: ' + str(len(node.processing_value)))
            # print(node.processing_value)

            PriorUser.avg_rating_deviation(graph, node)
            prior_user_avg_rating_deviation_list.append(node.processing_value[-1])

            # print('2 node.processing_value: ' + str(len(node.processing_value)))

            PriorUser.ratio_positive_and_negative_review(graph, node)
            prior_user_ratio_positive_review_list.append(node.processing_value[-2])
            prior_user_ratio_negative_review_list.append(node.processing_value[-1])

            # print('3 node.processing_value: ' + str(len(node.processing_value)))

            PriorUser.max_number_review(graph, node)
            prior_user_max_number_review_list.append(node.processing_value[-1])

            PriorUser.burstiness(graph, node)
            prior_user_burstiness_list.append(node.processing_value[-1])

            PriorUser.avg_review_length(graph, node)
            prior_user_avg_review_length_list.append(node.processing_value[-1])

            # print('last node.processing_value: '+str(len(node.processing_value)))
        elif node.__class__ == Product().__class__:
            PriorProduct.avg_rating_deviation(graph, node)
            prior_product_avg_rating_deviation_list.append(node.processing_value[-1])

            PriorProduct.ratio_positive_or_negative_review(graph, node)
            prior_product_ratio_positive_review_list.append(node.processing_value[-2])
            prior_product_ratio_negative_review_list.append(node.processing_value[-1])

            PriorProduct.max_number_review(graph, node)
            prior_product_max_number_review_list.append(node.processing_value[-1])

            PriorProduct.avg_review_length(graph, node)
            prior_product_avg_review_length_list.append(node.processing_value[-1])

            PriorReview.rating_deviation(graph, node)
            for review in graph.neighbors(node):
                prior_review_rating_deviation_list.append(review.temp_rating_deviation)

        elif node.__class__ == Review().__class__:
            PriorReview.is_single_review(graph, node)
            prior_review_is_single_review_list.append(node.processing_value[-1])

            PriorReview.review_length(graph, node)
            prior_review_review_length_list.append(node.processing_value[-1])

    # Priors lists sorting

    prior_user_avg_rating_deviation_list.sort()
    prior_user_ratio_positive_review_list.sort()
    prior_user_ratio_negative_review_list.sort()
    prior_user_max_number_review_list.sort()
    prior_user_burstiness_list.sort()
    prior_user_avg_review_length_list.sort()

    prior_product_avg_rating_deviation_list.sort()
    prior_product_max_number_review_list.sort()
    prior_product_avg_review_length_list.sort()
    prior_product_ratio_positive_review_list.sort()
    prior_product_ratio_negative_review_list.sort()

    prior_review_rating_deviation_list.sort()
    prior_review_is_single_review_list.sort()
    prior_review_review_length_list.sort()

    # Priors calculation
    for node in graph.nodes():
        # node.prior is recommended to be initialized as [0,0]
        f_sum = 0
        if node.__class__ == User().__class__:
            f_sum += (1 - prior_user_avg_rating_deviation_list.index(
                node.processing_value[0]) / len(prior_user_avg_rating_deviation_list)) ** 2

            # print('list: '+str(prior_user_ratio_positive_review_list))
            # print('np: '+str(node.processing_value))

            f_sum += (1 - prior_user_ratio_positive_review_list.index(
                node.processing_value[1]) / len(prior_user_ratio_positive_review_list)) ** 2

            f_sum += (1 - prior_user_ratio_negative_review_list.index(
                node.processing_value[2]) / len(prior_user_ratio_negative_review_list)) ** 2

            f_sum += (1 - prior_user_max_number_review_list.index(
                node.processing_value[3]) / len(prior_user_max_number_review_list)) ** 2

            f_sum += (1 - prior_user_burstiness_list.index(
                node.processing_value[4]) / len(prior_user_burstiness_list)) ** 2

            f_sum += (prior_user_avg_review_length_list.index(
                node.processing_value[5]) / len(prior_user_avg_review_length_list)) ** 2

            node.prior[0] = (f_sum / 6) ** 0.5
            node.prior[1] = 1 - node.prior[0]

        elif node.__class__ == Product().__class__:
            f_sum += (1 - prior_product_avg_rating_deviation_list.index(
                node.processing_value[0]) / len(prior_product_avg_rating_deviation_list)) ** 2

            f_sum += (1 - prior_product_ratio_positive_review_list.index(
                node.processing_value[1]) / len(prior_product_ratio_positive_review_list)) ** 2

            f_sum += (1 - prior_product_ratio_negative_review_list.index(
                node.processing_value[2]) / len(prior_product_ratio_negative_review_list)) ** 2

            f_sum += (1 - prior_product_max_number_review_list.index(
                node.processing_value[3]) / len(prior_product_max_number_review_list)) ** 2

            f_sum += (prior_product_avg_review_length_list.index(
                node.processing_value[4]) / len(prior_product_avg_review_length_list)) ** 2

            node.prior[0] = (f_sum / 5) ** 0.5
            node.prior[1] = 1 - node.prior[0]

        elif node.__class__ == Review().__class__:
            f_sum += (1 - prior_review_rating_deviation_list.index(
                node.temp_rating_deviation) / len(prior_review_rating_deviation_list)) ** 2

            f_sum += (1 - prior_review_is_single_review_list.index(
                node.processing_value[0]) / len(prior_review_is_single_review_list)) ** 2

            f_sum += (prior_review_review_length_list.index(
                node.processing_value[1]) / len(prior_review_review_length_list)) ** 2

            node.prior[0] = (f_sum / 3) ** 0.5
            node.prior[1] = 1 - node.prior[0]

    print("Priors is Ready")
