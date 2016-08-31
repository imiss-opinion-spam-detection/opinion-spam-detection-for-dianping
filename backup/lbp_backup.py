from networkx import Graph

from compute.classes import User, Review


def phi(node, i):
    return node.prior[i]


# For all labels, the number 0 denotes normal(good) node, while 1 denotes suspicious(bad) one.
# Function values quoted from Tabel 1
def psi(label_i, label_j, t, epsilon=0.1):
    if t == 'write':
        result = 1 if (label_i and label_j) or (not label_i and not label_j) else 0
    elif t == 'belong':
        result = 1 - epsilon if (label_i and label_j) or (not label_i and not label_j) else epsilon
    else:
        result = -1
        print('label error!')
    return result


# Total unsupervised algorithm
# Loopy Belief Propagation(LBP) function
def loopy_belief_propagation(g=Graph(), alpha=1, delta0=0.0000001, beta=1):
    """
    假定每一节点具有统一标号 从数据库向图里导入时给预留的.id_number赋值为统一编号
    Any edge is assigned a list which contains its [索引1，2指向节点编号, m_ij(0) and m_ij(1),mji(0),mji(1)]
    （索引1，2指向节点编号）值为m_ij中节点Y_j.id_number
    每一节点有.belief变量保存最终计算结果
    e.g.
    G[u1][r1]=[-1,0,0,0,0]
    以上是图中边的初始默认赋值，在从数据库导入时发生，label根据边两端节点的性质进行赋值
    （索引1，2指向节点编号）默认值为任意一点的id_number 在Initialization of all m_ij and id_nummber处赋值
    """

    print("LBP is running")
    # num_nodes = g.number_of_nodes()
    # Initialization of all m_ij and id_number
    for (n1, n2) in g.edges():
        g[n1][n2][0] = n2.id_number
        for i in range(1, 5):
            g[n1][n2][i] = 1

    # Main LBP algorithm
    delta = 999
    while True:
        for (n1, n2) in g.edges():  # n1->Y_i  n2->Y_j
            t_label = 'write' if (n1.__class__, n2.__class__) == (User().__class__, Review().__class__) \
                                 or (Review().__class__, User().__class__) else 'belong'

            if g[n1][n2][0] == n1.id_number:
                (n1, n2) = (n2, n1)
            for j in range(2):  # calculate m_i->j
                sum0 = 0
                for i in range(2):
                    for n3 in g.neighbors(n1):
                        if n3 != n2:
                            sum0 *= g[n3][n1][i + 1]
                    sum0 += psi(i, j, t_label) * phi(n1, i)
                g[n1][n2][j + 1] = sum0 * alpha

            (n1, n2) = (n2, n1)

            for j in range(2):  # Calculate m_j->i
                sum1 = 0
                for i in range(2):
                    for n3 in g.neighbors(n1):
                        if n3 != n2:
                            sum1 *= g[n3][n1][i + 3]
                    sum1 += psi(i, j, t_label) * phi(n1, i)
                temp = g[n1][n2][j + 3]
                g[n1][n2][j + 3] = sum1 * alpha
                delta = g[n1][n2][j + 3] - temp

        if delta < delta0:
            break

    # Compute final beliefs
    for node in g.nodes():
        for i in range(2):
            product = 1
            for nj in g.neighbors(node):
                product *= g[node][nj][i + 1] if g[node][nj][0] == node.id_number else g[node][nj][i + 3]
            node.belief[i] = beta * phi(node, i) * product
    print("LBP Finish\n\n\n")

# # Test code
#
# graph =  Graph()
#
# n1 = ds.User(1, '123', 'a')
# n2 = ds.User(2, '234', 'b')
#
# n3 = ds.Review(3, 'asdasdaddddddddddddddddfsd')
# n4 = ds.Review(4, 'pptp')
# n5 = ds.Review(5, 'qqfffdddddddddddfffffq')
# n6 = ds.Review(6, '==fffffffff=')
#
# n7 = ds.Product(7, 'ZZZ')
# n8 = ds.Product(8, 'zxc')
#
# graph.add_edge(n1, n3)
# graph.add_edge(n8, n3)
#
# graph.add_edge(n1, n4)
# graph.add_edge(n7, n4)
#
# graph.add_edge(n2, n5)
# graph.add_edge(n7, n5)
#
# graph.add_edge(n2, n6)
# graph.add_edge(n8, n6)
#
# # for node in graph:
# #     print(str(node.belief))
#
# LBP(graph)
# print('LBP finished')
# for node in graph:
#     print(str(node.id_number) + str(node.belief) + str(node.__class__))
