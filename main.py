from network import RandomNetwork
from heuristic import greedy, two_opt
from mcts import RandomMCTS
from plot import plot_path


network = RandomNetwork(30, 100)

# #--- Example with Plot ---#
#
# ### heuristic 1
# edges, cost = greedy(network)
# plot_path(n.graph.nodes, edges, n.positions)
#
# ### heuristic 2
# edges, cost = two_opt(network)
# plot_path(network.graph.nodes, edges, network.positions)
#
# ### mcts
# random_mcts = RandomMCTS(network)
# edges, cost = random_mcts.run(0.95, 5, 10)
# plot_path(network.graph.nodes, edges, network.positions)
# print ("mcts has cost of {:.2f}".format(cost))



#--- Small Testcase ---#

num_of_network = 5
trail_per_network = 2
results = [[], [], []]

for i in range(num_of_network):
    network = RandomNetwork(30, 100)
    for j in range(trail_per_network):
        edges, cost = greedy(network)
        results[0].append(cost)

        edges, cost = two_opt(network)
        results[1].append(cost)

        random_mcts = RandomMCTS(network)
        edges, cost = random_mcts.run(0.95, 5, 10)
        results[2].append(cost)

print ("greedy has cost of {:.2f}".format(sum(results[0])/len(results[0])))
print ("2 opt has cost of {:.2f}".format(sum(results[1])/len(results[1])))
print ("random mcts has cost of {:.2f}".format(sum(results[2])/len(results[2])))
