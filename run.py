#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from time import time

from networkx import Graph

from compute.data import select, build_graph, show_result, say_finish, data_to_graph
from compute.lbp import lbp
from compute.prior import set_prior


def run_compute():
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


def run_load():
    table = str(input("Please input the table's name\n>>> "))
    graph = data_to_graph(table=table)
    show_result(graph, 'cmd')


if __name__ == '__main__':
    while True:
        selection = str(input("Above all, you need to select : 1->compute from data 2->load result\n"))
        if selection == "1":
            run_compute()
            break
        elif selection == "2":
            run_load()
            break
        else:
            print("SelectionError\a")
