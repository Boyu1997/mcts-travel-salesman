from network import RandomNetwork
from heuristic import greedy, two_opt
from mcts import RandomMCTS
from plot import plot_path

network = RandomNetwork(20, 100)

### heuristic 1
edges, cost = greedy(network)
# plot_path(n.graph.nodes, edges, n.positions)

### heuristic 2
edges, cost = two_opt(network)
# plot_path(network.graph.nodes, edges, network.positions)

### mcts
random_mcts = RandomMCTS(network)
random_mcts.run(5, 100)
