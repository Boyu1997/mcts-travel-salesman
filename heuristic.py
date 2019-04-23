import random
import copy

def calculate_cost(edges):
    cost = 0
    for edge in edges:
        cost += edge[2]['weight']
    return cost

def greedy(graph):

    # setup
    g = copy.deepcopy(graph)
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
                                graph.edges[visited_edges[-1][1], visited_edges[0][1]]]))


    # calculate cost
    cost = calculate_cost(visited_edges)

    return visited_edges, cost


def two_opt(graph):

    # setup &
    g = copy.deepcopy(graph)
    path_edges = []
    unvisited_nodes = list(g.nodes)
    random.shuffle(unvisited_nodes)
    current_node = unvisited_nodes.pop()

    # generate a random path
    while len(unvisited_nodes) > 0:
        next_node = unvisited_nodes.pop()
        path_edges.append(tuple([current_node, next_node,
                                 graph.edges[current_node, next_node]]))
        current_node = next_node

    # calculate cost
    cost = calculate_cost(path_edges)

    return path_edges, cost
