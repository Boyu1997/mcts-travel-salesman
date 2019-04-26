from heuristic import greedy, two_opt
from mcts import RandomMCTS, GreedyMCTS
from plot import plot_path
import time


# ###### Example with Plot ######
# input
# |- network: a
def single_test(network, plot=False):

    edges_set = []
    cost_set = []

    ### heuristic 1 - greedy
    start = time.time()
    edges, cost = greedy(network)
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    print ("greedy heuristic has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### heuristic 2 - two opt
    start = time.time()
    edges, cost = two_opt(network)
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    print ("two-opt heuristic has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### mcts 1 - random
    start = time.time()
    random_mcts = RandomMCTS(network)
    edges, cost = random_mcts.run(50, 10, 1000)   # run takes (number to expand, number to simulate,
                                                  ## and constant C) as input
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    print ("random mcts has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### mcts 2 - greedy
    start = time.time()
    greedy_mcts = GreedyMCTS(network, 0.2)
    edges, cost = greedy_mcts.run(50, 10, 100)   # run takes (number to expand, number to simulate,
                                                 ## and constant C) as input
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    print ("greedy mcts has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    if plot == True:
        plot_path(network.graph.nodes, edges, network.positions)

def small_test(network, plot=False):
    return


# #--- Small Testcase ---#
#
# num_of_network = 3
# trail_per_network = 2
# results = [[] for _ in range(4)]
#
# for i in range(num_of_network):
#     network = RandomNetwork(30, 100)
#     for j in range(trail_per_network):
#         edges, cost = greedy(network)
#         results[0].append(cost)
#
#         edges, cost = two_opt(network)
#         results[1].append(cost)
#
#         random_mcts = RandomMCTS(network)
#         edges, cost = random_mcts.run(50, 20, 100)
#         results[2].append(cost)
#
#         greedy_mcts = GreedyMCTS(network, 0.2)
#         edges, cost = greedy_mcts.run(50, 20, 100)
#         results[3].append(cost)
#
# print ("greedy has cost of {:.2f}".format(sum(results[0])/len(results[0])))
# print ("2 opt has cost of {:.2f}".format(sum(results[1])/len(results[1])))
# print ("random mcts has cost of {:.2f}".format(sum(results[2])/len(results[2])))
# print ("greedy mcts has cost of {:.2f}".format(sum(results[3])/len(results[3])))
