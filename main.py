from network import RandomNetwork
from heuristic import greedy, two_opt
from plot import plot_path

n = RandomNetwork(20, 100)

# heuristic 1
edges, cost = greedy(n.graph)
plot_path(n.graph.nodes, edges, n.positions)

# heuristic 2
edges, cost = two_opt(n.graph)
plot_path(n.graph.nodes, edges, n.positions)
