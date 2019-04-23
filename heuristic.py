import random
import copy

def nearest_neighbor(graph):

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
    cost = 0
    for edge in visited_edges:
        cost += edge[2]['weight']

    return visited_edges, cost
