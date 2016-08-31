#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from time import time

from networkx import Graph

from compute.classes import User, Review


# import matplotlib.pyplot as plt


def phi(node, i):
    return node.prior[i]


# For all labels, the number 0 denotes normal(good) node, whereas 1 denotes suspicious(bad) one.
# Function values quoted from Tabel 1
def psi(label_i, label_j, t, epsilon1=0.1, epsilon2=0.4):
    if t == 'write':
        # 针对论文的重要改动
        result = 1 - epsilon1 if (label_i and label_j) or (not label_i and not label_j) else epsilon1
    elif t == 'belong':
        result = 1 - epsilon2 if (label_i and label_j) or (not label_i and not label_j) else epsilon2
    else:
        print('label error!')
    return result


'''
假定每一节点具有统一标号 从数据库向图里导入时给预留的.id_number赋值为统一编号
Any edge is assigned a list which contains its [索引1，2指向节点编号, m_ij(0) and m_ij(1),mji(0),mji(1)]
（索引1，2指向节点编号）值为m_ij中节点Y_j.id_number
每一节点有.belief变量保存最终计算结果
e.g.
G[u1][r1]=[-1,0,0,0,0]
以上是图中边的初始默认赋值，在从数据库导入时发生，label根据边两端节点的性质进行赋值
（索引1，2指向节点编号）默认值为任意一点的id_number 在Initialization of all m_ij and id_nummber处赋值

'''


# Total unsupervised algorithm
# Loopy Belief Propagation(LBP) function
def lbp(g=Graph(), alpha=1, delta0=0.001, beta=1):
    # num_nodes = g.number_of_nodes()
    # Initialization of all m_ij and id_number
    print('LBP is Running')
    start_time = time()
    for (n1, n2) in g.edges():
        g[n1][n2][0] = n2.id_number
        for i in range(1, 5):
            g[n1][n2][i] = 1

    # Initialization of priors
    # init_priors(g)                                                             #c!!!!!!!!!!!!

    # Main LBP algorithm
    delta = 999
    iter_times = 0
    # while True:
    while iter_times < 20:
        message_change_number = 0
        message_change_value_sum = 0
        for (n1, n2) in g.edges():  # n1->Y_i  n2->Y_j
            t_label = 'write' if ((n1.__class__, n2.__class__) == (User().__class__, Review().__class__)) or (
                (n1.__class__, n2.__class__) == (Review().__class__, User().__class__))else 'belong'

            if g[n1][n2][0] == n1.id_number:
                (n1, n2) = (n2, n1)

            temp1 = g[n1][n2][1]
            temp2 = g[n1][n2][2]
            for j in range(2):  # calculate m_i->j
                sum0 = 0
                for i in range(2):
                    product1 = 1
                    for n3 in g.neighbors_iter(n1):
                        if n3 != n2:
                            # print('g[n3][n1][i + 1]: '+str(g[n3][n1][i + 1]))
                            # print('g[n3][n1][i + 3]: '+str(g[n3][n1][i + 3]))
                            # print('n3.id_number: '+str(n3.id_number)+'  n1.id_number: '+str(n1.id_number))
                            # print('product_change: '+str(g[n3][n1][i + 1] if g[n3][n1][0] == n1.id_number else g[n3][n1][i + 3]))
                            # if (n1.id_number == 2 and n3.id_number == 6) or (n1.id_number == 6 and n3.id_number == 2):
                            #     print('\n----------------------used')
                            #     print(g[n1][n3])
                            #     print('----------------------\n')
                            product1 *= g[n3][n1][i + 1] if g[n3][n1][0] == n1.id_number else g[n3][n1][i + 3]
                    # print('product1: ' + str(product1))
                    # print('psi(i, j, t_label): ' + str(psi(i, j, t_label)))
                    # print('phi(n1, i): ' + str(phi(n1, i)))
                    # if (n1.id_number == 2 and n2.id_number == 6) or (n1.id_number == 6 and n2.id_number == 2):
                    #     print('product1: ' + str(product1))
                    #     print('psi(i, j, t_label): ' + str(psi(i, j, t_label)))
                    #     print('phi(n1, i): ' + str(phi(n1, i)))
                    sum0 += psi(i, j, t_label) * phi(n1, i) * product1
                    # print('sum0: ' + str(sum0) + '\ n')
                g[n1][n2][j + 1] = sum0 * alpha
                # if (n1.id_number == 2 and n2.id_number == 6) or (n1.id_number == 6 and n2.id_number == 2):
                # print('\n----------------------changed')
                # print(g[n1][n2])
                # print('----------------------\n')
                # print('n1.id_number: ' + str(n1.id_number) + '   n2.id_number: ' + str(n2.id_number))
                # print('j = '+str(j)+'\n\n')
            if g[n1][n2][1] + g[n1][n2][2] != 0:
                g[n1][n2][1] /= g[n1][n2][1] + g[n1][n2][2]
                g[n1][n2][2] = 1 - g[n1][n2][1]
            else:
                g[n1][n2][1] = g[n1][n2][2] = 0.5
            message_change_value_sum += abs(g[n1][n2][1] - temp1) + abs(g[n1][n2][2] - temp2)
            message_change_number += 2

            (n1, n2) = (n2, n1)

            temp3 = g[n1][n2][3]
            temp4 = g[n1][n2][4]
            for j in range(2):  # Calculate m_j->i
                sum1 = 0
                for i in range(2):
                    product1 = 1
                    for n3 in g.neighbors_iter(n1):
                        if n3 != n2:
                            product1 *= g[n3][n1][i + 1] if g[n3][n1][0] == n1.id_number else g[n3][n1][i + 3]
                    sum1 += psi(i, j, t_label) * phi(n1, i) * product1
                g[n1][n2][j + 3] = sum1 * alpha

            if g[n1][n2][3] + g[n1][n2][4] != 0:
                g[n1][n2][3] /= g[n1][n2][3] + g[n1][n2][4]
                g[n1][n2][4] = 1 - g[n1][n2][3]
            else:
                g[n1][n2][3] = g[n1][n2][4] = 0.5
            message_change_value_sum += abs(g[n1][n2][3] - temp3) + abs(g[n1][n2][4] - temp4)
            message_change_number += 2
        message_change_value = message_change_value_sum / message_change_number
        # print('!!!!!message_change_value: ' + str(message_change_value))
        if message_change_value < delta0:
            break
        iter_times += 1

    # Compute final beliefs
    for node in g.nodes():
        for i in range(2):
            product = 1
            for nj in g.neighbors_iter(node):
                # print('message: ')
                # print(g[node][nj][i + 1] if g[node][nj][0] == node.id_number else g[node][nj][i + 3])
                # print('message end')
                product *= g[node][nj][i + 1] if g[node][nj][0] == node.id_number else g[node][nj][i + 3]
            node.belief[i] = beta * phi(node, i) * product
            # print(product)
        if node.belief[0] + node.belief[1] != 0:
            node.belief[0] /= node.belief[0] + node.belief[1]
            node.belief[1] = 1 - node.belief[0]
        else:
            node.belief[1] = node.belief[0] = 0.5
    print('LBP finished')
    print('Time Spent on LBP : %f' % (time() - start_time))

# # Test code
# if __name__ == '__main__':
#     graph = Graph()
#
#     n1 = User(1, '123', 'a')
#     n2 = User(2, '234', 'b')
#
#     n3 = Review(3, 'asdasdaddddddddddddddddfsd')
#     n4 = Review(4, 'pptp')
#     n5 = Review(5, 'qqfffdddddddddddfffffq')
#     n6 = Review(6, '==fffffffff=')
#
#     n7 = Product(7, 'ZZZ')
#     n8 = Product(8, 'ZZZ')
#
#     n9 = User(9, 'fake', 'aaa')
#
#     n10 = Review(10, 'pptp')
#
#     n11 = Product(11, 'zxsssc')
#
#     n12 = Review(12, 'fff=sssss=fffffffff=')
#
#     # graph.add_edge(n1, n3)
#     # graph.add_edge(n8, n3)
#
#     graph.add_edge(n1, n4)
#     graph.add_edge(n7, n4)
#
#     # graph.add_edge(n2, n5)
#     # graph.add_edge(n7, n5)
#
#     graph.add_edge(n2, n6)
#     graph.add_edge(n8, n6)
#
#     graph.add_edge(n9, n10)
#     graph.add_edge(n10, n11)
#
#     graph.add_edge(n9, n12)
#     graph.add_edge(n12, n8)
#
#     print(graph.has_node(n10))
#     print('\n')
#     for node in graph:
#         print(str(node.id_number) + str(node.belief) + str(node.__class__) + str((phi(node, 0), phi(node, 1))))
#
#     # for node in graph:
#     #     print(str(node.belief))
#     set_prior(graph)
#     # n1.prior=[0.1,0.9]
#     # n3.prior=[0.2,0.8]
#     # n8.prior=[0.3,0.7]
#     n9.prior = [0.2, 0.8]
#     n10.prior = [0.3, 0.7]
#     n11.prior = [0.25, 0.75]
#     n12.prior = [0.5, 0.5]
#     # print(nx.is_bipartite(graph))
#     #
#     # pos = nx.circular_layout(graph)
#     # nx.draw(graph, pos=pos)
#     #
#     # plt.show()
#     lbp(graph)
#
#     for node in graph:
#         print('Id: %d' % (node.id_number) + ' Probability: [%.3f, %.3f]' % (node.belief[0], node.belief[1]) \
#               + ' Prior: [%.3f, %.3f] ' % (phi(node, 0), phi(node, 1)) + str(node.__class__))
#
#         # for (n1,n2) in graph.edges():
#         #     print(str(n1.id_number)+' '+str(n2.id_number)+' edge: '+str(graph[n1][n2][0]))
#
#
#         # print(str(n10.id_number) + '%.3f'%(n10.belief[0])+ str(n10.__class__) + str((phi(n10, 0), phi(n10, 1))))
#     for n in graph.neighbors(n4):
#         n.printf()
#     print('------------------------------------------------------------')
#     for n in graph.neighbors(n6):
#         n.printf()
#
#     print(graph.number_of_nodes())
#
#     print(graph.adjacency_list())
