from network import Network
from heuristic import greedy, two_opt
from mcts import RandomMCTS, GreedyMCTS
from plot import plot_path
from matplotlib import pyplot as plt
import time


# ###### Single Test ######
#
# To run each of the method once to test code is working. This function can
# also plot the path each algorithm found.
#
# Input
# |- num_of_node: number of node to visit
# |- side_length: the side length of the 2d square the all the nodes rest on
# └- plot: a boolean telling if to plot the path each algorithm came up with

def single_test(num_of_node, side_length=100, plot=False):

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



# ###### Small Test ######
#
# Run a small Monte Carlo simulation to get a quick performance summary.
#
# Input
# |- num_of_network: number of network to test on
# |- trail_per_network: number of trail to run each method on a network
# |- num_of_node: number of node to visit
# |- side_length: the side length of the 2d square the all the nodes rest on
# └- plot: a boolean telling if to plot a histogram

def small_test(num_of_network, trail_per_network, num_of_node, side_length=100, plot=False):

    results = [[] for _ in range(4)]

    for i in range(num_of_network):
        network = Network(30, 100)
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

    if plot == True:
        plt
