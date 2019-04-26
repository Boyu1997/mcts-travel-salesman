import networkx as nx
from matplotlib import pyplot as plt

def plot_path(ax, model_name, cost, time, nodes, edges, positions):
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    nx.draw(graph, positions, ax=ax, node_size=50, edge_color='0.2')
    ax.set_title('{:s} model\ncost={:.2f} time={:.4f}s'.format(model_name, cost, time))
