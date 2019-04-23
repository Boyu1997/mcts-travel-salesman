from network import RandomNetwork
from heuristic import nearest_neighbor
from plot import plot_path

n = RandomNetwork(20, 100)
visited_edges, cost = nearest_neighbor(n.graph)

plot_path(n.graph.nodes, visited_edges, n.positions)
