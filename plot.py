import networkx as nx
from matplotlib import pyplot as plt

def plot_path(nodes, edges, positions):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    nx.draw(graph, positions, node_size=50, edge_color='0.2')
    plt.show()
