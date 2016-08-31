#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from datetime import date as date_class


class Node(object):
    def __init__(self, id_number=0):
        self.id_number = id_number
        self.feature_value = dict()
        self.prior = [0.0, 0.0]
        self.belief = [0.0, 0.0]


class User(Node):
    def __init__(self, id_number=0, name_id='', name=''):
        Node.__init__(self, id_number)
        self.name_id = name_id
        self.name = name

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.name == other.name and \
               self.name_id == other.name_id

    def __hash__(self):
        return hash((self.__class__, self.name_id, self.name))

    def __str__(self):
        return 'User:\n' \
               'id_number:%d\n' \
               'name_id:%s\n' \
               'name:%s\n' \
               'feature value:%s\n' \
               'prior:%s\n' \
               'belief:%s\n\n' \
               % (self.id_number,
                  self.name_id,
                  self.name,
                  self.feature_value,
                  self.prior,
                  self.belief)


class Review(Node):
    def __init__(self, id_number=0, text='', date=date_class(year=2016, month=6, day=6), rst1=0, rst2=0, rst3=0):
        Node.__init__(self, id_number)
        self.text = text
        self.date = date
        self.star = [rst1, rst2, rst3]
        self.sum_star = self.star[0] + self.star[1] + self.star[2]

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.id_number == other.id_number

    def __hash__(self):
        return hash((self.__class__, self.text, self.date, self.sum_star, self.id_number))

    def __str__(self):
        return 'Review:\n' \
               'id_number:%d\n' \
               'date:%s\n' \
               'text:%s\n' \
               'star:%s\n' \
               'feature value:%s\n' \
               'prior:%s\n' \
               'belief:%s\n\n' \
               % (self.id_number,
                  self.date,
                  self.text,
                  self.star,
                  self.feature_value,
                  self.prior,
                  self.belief)


class Product(Node):
    def __init__(self, id_number=0, name=''):
        Node.__init__(self, id_number)
        self.name = name

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.name == other.name

    def __hash__(self):
        return hash((self.__class__, self.name))

    def __str__(self):
        return 'Product:\n' \
               'id_number:%d\n' \
               'name:%s\n' \
               'feature value:%s\n' \
               'prior:%s\n' \
               'belief:%s\n\n' \
               % (self.id_number,
                  self.name,
                  self.feature_value,
                  self.prior,
                  self.belief)
