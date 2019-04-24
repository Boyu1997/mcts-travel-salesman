from network import RandomNetwork
from heuristic import greedy, two_opt
from mcts import RandomMCTS, GreedyMCTS
from plot import plot_path


# #--- Example with Plot ---#
#
# network = RandomNetwork(30, 100)
#
# ### heuristic 1
# edges, cost = greedy(network)
# plot_path(network.graph.nodes, edges, network.positions)
# print ("greedy has cost of {:.2f}".format(cost))
#
# ### heuristic 2
# edges, cost = two_opt(network)
# plot_path(network.graph.nodes, edges, network.positions)
# print ("2 opt has cost of {:.2f}".format(cost))
#
# ### random mcts
# random_mcts = RandomMCTS(network)
# edges, cost = random_mcts.run(50, 20, 1000)
# plot_path(network.graph.nodes, edges, network.positions)
# print ("random mcts has cost of {:.2f}".format(cost))
#
# ### greedy mcts
# greedy_mcts = GreedyMCTS(network, 0.2)
# edges, cost = greedy_mcts.run(50, 10, 100)
# plot_path(network.graph.nodes, edges, network.positions)
# print ("greedy mcts has cost of {:.2f}".format(cost))



#--- Small Testcase ---#

num_of_network = 3
trail_per_network = 2
results = [[] for _ in range(4)]

for i in range(num_of_network):
    network = RandomNetwork(30, 100)
    for j in range(trail_per_network):
        edges, cost = greedy(network)
        results[0].append(cost)

        edges, cost = two_opt(network)
        results[1].append(cost)

        random_mcts = RandomMCTS(network)
        edges, cost = random_mcts.run(50, 20, 100)
        results[2].append(cost)

        greedy_mcts = GreedyMCTS(network, 0.2)
        edges, cost = greedy_mcts.run(50, 20, 100)
        results[3].append(cost)

print ("greedy has cost of {:.2f}".format(sum(results[0])/len(results[0])))
print ("2 opt has cost of {:.2f}".format(sum(results[1])/len(results[1])))
print ("random mcts has cost of {:.2f}".format(sum(results[2])/len(results[2])))
print ("greedy mcts has cost of {:.2f}".format(sum(results[3])/len(results[3])))
