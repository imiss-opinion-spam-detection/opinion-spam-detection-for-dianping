from math import fabs

from networkx import Graph

from compute.classes import Node, User


def phi(node, i):
    return node.prior[int(i)]


# For all labels, the number 0 denotes normal(good) node, while 1 denotes suspicious(bad) one.
# Function values quoted from Tabel 1
def psi(node_i, node_j, label_i, label_j, epsilon=0.1):
    if node_i.__class__ == User().__class__ or node_j.__class__ == User().__class__:
        if label_i == label_j:
            return 1
        else:
            return 0
    else:
        if label_i == label_j:
            return 1 - epsilon
        else:
            return epsilon


def pi_ki(graph=Graph(), node_i=Node(), node_j=Node(), label=''):
    result = 1.0
    for neighbor in graph.neighbors(node_i):
        if neighbor == node_j:
            continue
        if graph[node_i][neighbor]['i'] == node_i.id_number:
            result *= graph[node_i][neighbor]['j->i:' + label]
        else:
            result *= graph[node_i][neighbor]['i->j:' + label]
        print("res" + str(result))
    if result == 0.0:
        input("dd_ki")
    return result


def pi_ji(graph=Graph(), node_i=Node(), label=''):
    result = 1.0
    for node_j in graph.neighbors(node_i):
        if graph[node_i][node_j]['i'] == node_i.id_number:
            result *= graph[node_i][node_j]['j->i:' + label]
        else:
            result *= graph[node_i][node_j]['i->j:' + label]
        print("res"+str(result))
    if result == 0.0:
        input("ded_ji")
    return result


def loopy_belief_propagation(graph=Graph(), alpha=0.9, beta=1.000, delta=1e-16):
    print("LBP is running")
    # num_nodes = g.number_of_nodes()
    # Initialization of all m_ij and id_number
    for (node_i, node_j) in graph.edges():
        graph[node_i][node_j]['i'] = node_i.id_number
        graph[node_i][node_j]['j'] = node_j.id_number
        graph[node_i][node_j]['i->j:1'] = 1.0
        graph[node_i][node_j]['j->i:1'] = 1.0
        graph[node_i][node_j]['i->j:0'] = 1.0
        graph[node_i][node_j]['j->i:0'] = 1.0
    while True:
        delta_change = 0
        for (node_i, node_j) in graph.edges():
            if node_i.id_number != graph[node_i][node_j]['i']:
                node_i, node_j = node_j, node_i
            for label_j in ['0', '1']:  # i->j
                temp = graph[node_i][node_j]['i->j:' + label_j]
                graph[node_i][node_j]['i->j:' + label_j] = alpha * (
                     phi(node_i, '0') * psi(node_i, node_j, label_j, '0') * pi_ki(graph, node_i, node_j, '0') + \
                    phi(node_i, '1') * psi(node_i, node_j, label_j, '1') * pi_ki(graph, node_i, node_j, '1'))
                delta_change += fabs(temp - graph[node_i][node_j]['i->j:' + label_j])
            for label_i in ['0', '1']:  # j->i
                temp = graph[node_i][node_j]['j->i:' + label_i]
                graph[node_i][node_j]['j->i:' + label_i] = alpha * (
                    phi(node_j, '0') * psi(node_j, node_i, label_i, '0') * pi_ki(graph, node_j, node_i, '0') + \
                    phi(node_j, '1') * psi(node_j, node_i, label_i, '1') * pi_ki(graph, node_j, node_i, '1'))
                delta_change += fabs(temp - graph[node_i][node_j]['j->i:' + label_i])
        print(delta_change)
        if delta_change < delta:
            break

    # Compute Final Belief
    for node in graph.nodes():
        for label in ['0', '1']:
            node.belief[int(label)] = beta * phi(node, label)*pi_ji(graph,node,label)

    # # Format Final Belief
    # for node in graph.nodes():
    #     node.belief[0] = node.belief[0]/(node.belief[0]+node.belief[1])
    #     node.belief[1] = 1 - node.belief[0]
