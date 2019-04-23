import random
import copy
import numpy as np

def calculate_cost(edges):
    cost = 0
    for edge in edges:
        cost += edge[2]['weight']
    return cost

def greedy(network):

    # setup
    g = copy.deepcopy(network.graph)
    visited_edges = []
    current_node = random.choice(list(g.nodes))

    # path finding
    while len(g.nodes) > 0:
        edges = g.edges(current_node, data=True)
        edges = sorted(edges, key = lambda x: x[2]['weight'], reverse=False)
        for edge in edges:
            if edge not in visited_edges:
                visited_edges.append(edge)
                next_node = edge[1]
                break
        g.remove_node(current_node)
        current_node = next_node

    # return to the origin node
    visited_edges.append(tuple([visited_edges[-1][1], visited_edges[0][0],
                                network.graph.edges[visited_edges[-1][1], visited_edges[0][1]]]))


    # calculate cost
    cost = calculate_cost(visited_edges)

    return visited_edges, cost


def two_opt(network):

    # setup
    g = network.graph
    path_edges = []
    unvisited_nodes = list(g.nodes)
    random.shuffle(unvisited_nodes)
    current_node = unvisited_nodes.pop()

    # generate a random path
    while len(unvisited_nodes) > 0:
        next_node = unvisited_nodes.pop()
        path_edges.append(tuple([current_node, next_node,
                                 g.edges[current_node, next_node]]))
        current_node = next_node

    path_edges.append(tuple([path_edges[-1][1], path_edges[0][0],
                                g.edges[path_edges[-1][1], path_edges[0][1]]]))
    path_edges = np.array(path_edges)


    # two opt
    counter = 0
    while counter < len(path_edges)*10:   # when path is stable, terminate
        counter += 1
        np.roll(path_edges, 1)   # roll the path so the first and last edge can be updated
        selected_edge_indexs = random.sample(range(len(path_edges)), 2)
        selected_edge_indexs = sorted(selected_edge_indexs)
        selected_edges = [path_edges[i] for i in selected_edge_indexs]
        current_cost = selected_edges[0][2]['weight'] + selected_edges[1][2]['weight']
        new_edges = [tuple([selected_edges[0][0], selected_edges[1][0],
                            g.edges[selected_edges[0][0], selected_edges[1][0]]]),
                     tuple([selected_edges[0][1], selected_edges[1][1],
                                         g.edges[selected_edges[0][1], selected_edges[1][1]]])]
        new_cost = new_edges[0][2]['weight'] + new_edges[1][2]['weight']
        if new_cost < current_cost:   # perform the switch
            # switch the two selected edges
            path_edges[selected_edge_indexs[0]] = new_edges[0]
            path_edges[selected_edge_indexs[1]] = new_edges[1]

            # reoreder the edges in between
            if abs(selected_edge_indexs[0] - selected_edge_indexs[1]) > 1:
                 path_edges[selected_edge_indexs[0]+1:selected_edge_indexs[1]] = path_edges[selected_edge_indexs[1]-1:selected_edge_indexs[0]:-1]
            for i in range(selected_edge_indexs[0] + 1, selected_edge_indexs[1]):
                path_edges[i]= tuple([path_edges[i][1], path_edges[i][0], path_edges[i][2]])
            counter = 0   # reset timeout counter

    # calculate cost
    cost = calculate_cost(path_edges)

    return path_edges, cost
