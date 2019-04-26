from network import Network
from heuristic import greedy, two_opt
from mcts import RandomMCTS, GreedyMCTS
from plot import plot_path
from matplotlib import pyplot as plt
import time


# ###### Test ######
#
# To run each of the method once to test code is working. This function can
# also plot the path each algorithm found.
#
# Input
# |- num_of_node: number of node to visit
# |- side_length: the side length of the 2d square the all the nodes rest on
# └- plot: a boolean telling if to plot the path each algorithm came up with

def test(num_of_node, side_length=100, plot=False):

    network = Network(num_of_node, side_length)
    edges_set = []
    cost_set = []
    run_time_set = []

    ### heuristic 1 - greedy
    start = time.time()
    edges, cost = greedy(network)
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    run_time_set.append(run_time)
    print ("greedy heuristic has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### heuristic 2 - two opt
    start = time.time()
    edges, cost = two_opt(network)
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    run_time_set.append(run_time)
    print ("two-opt heuristic has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### mcts 1 - random
    start = time.time()
    random_mcts = RandomMCTS(network)
    edges, cost = random_mcts.run(50, 10, 1000)   # run takes (number to expand, number to simulate,
                                                  ## and constant C) as input
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    run_time_set.append(run_time)
    print ("random mcts has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    ### mcts 2 - greedy
    start = time.time()
    greedy_mcts = GreedyMCTS(network, 0.2)
    edges, cost = greedy_mcts.run(50, 10, 100)   # run takes (number to expand, number to simulate,
                                                 ## and constant C) as input
    run_time = time.time() - start

    edges_set.append(edges)
    cost_set.append(cost)
    run_time_set.append(run_time)
    print ("greedy mcts has cost of {:.2f} using {:.4f}s".format(cost, run_time))


    if plot == True:
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8,8))
        fig.suptitle("Path Found by Different Models (num_of_node={:d}, side_length={:d})".format(num_of_node, side_length))
        model_names = ['greedy heuristic', '2-opt heuristic', 'random mcts', 'greedy mcts']
        for i in range(4):
            plot_path(axs[int(i/2),i%2], model_names[i], cost_set[i], run_time_set[i],
                      network.graph.nodes, edges_set[i], network.positions)
        plt.show()
