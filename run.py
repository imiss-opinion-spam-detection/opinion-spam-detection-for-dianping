#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from time import time

from networkx import Graph

from compute.data import select, build_graph, show_result, say_finish
from compute.lbp import lbp
from compute.prior import set_prior


def run():
    print('-----------------------------\n'
          'Opinion Spam Detection System\n'
          '-----------------------------')
    selection = select()
    start_time = time()
    graph = Graph()
    build_graph(graph, selection)
    set_prior(graph)
    lbp(graph)
    print('All Time : %f' % (time() - start_time))
    say_finish(1)
    show_result(graph, 'cmd')


if __name__ == '__main__':
    run()
