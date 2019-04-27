from network import Network
from heuristic import greedy, two_opt
from mcts import RandomMCTS, GreedyMCTS
from plot import plot_path
from matplotlib import pyplot as plt
import time
import numpy as np

from tqdm import tqdm
from multiprocessing import Pool
from itertools import product


# trail function defined separately for multiprocessing
def run_trail(network):

    results = []

    ### heuristic 1 - greedy
    start = time.time()
    edges, cost = greedy(network)
    run_time = time.time() - start

    results.append([cost, run_time])

    ### heuristic 2 - two opt
    start = time.time()
    edges, cost = two_opt(network)
    run_time = time.time() - start

    results.append([cost, run_time])

    ### mcts 1 - random
    start = time.time()
    random_mcts = RandomMCTS(network)
    edges, cost = random_mcts.run(50, 20, 100)
    run_time = time.time() - start

    results.append([cost, run_time])

    ### mcts 2 - greedy
    start = time.time()
    greedy_mcts = GreedyMCTS(network, 0.2)
    edges, cost = greedy_mcts.run(50, 20, 100)
    run_time = time.time() - start

    results.append([cost, run_time])

    return results



# ###### Simulation ######
#
# Run Monte Carlo simulation to get performance report.
#
# Input
# |- num_of_network: number of network to test on
# |- trail_per_network: number of trail to run each method on a network
# |- num_of_node: number of node to visit
# |- side_length: the side length of the 2d square the all the nodes rest on
# └- plot: a boolean telling if to plot a histogram

def simulation(num_of_network, trail_per_network, num_of_node, side_length=100, plot=False):

    results = np.array([])

    for i in tqdm(range(num_of_network)):

        # run trails at the same time using multiprocessing
        network = Network(num_of_node, side_length)
        networks = [network for _ in range(trail_per_network)]
        p = Pool(10)
        result = p.map(run_trail, networks)
        p.close()
        result = np.array(result)

        # add to result set
        results = np.vstack((results, result))  if results.size else result


    h_1 = results[:, 0, :]
    h_2 = results[:, 1, :]
    t_1 = results[:, 2, :]
    t_2 = results[:, 3, :]

    print ("greedy has average cost of {:.2f}".format(np.mean(h_1)))
    print ("2 opt has average cost of {:.2f}".format(np.mean(h_2)))
    print ("random mcts has average cost of {:.2f}".format(np.mean(t_1)))
    print ("greedy mcts has average cost of {:.2f}".format(np.mean(t_2)))

    if plot == True:

        ### time vs cost plot
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,8))
        ax.plot(h_1[:,1], h_1[:,0], 'r+', label='greedy heuristic')
        ax.plot(h_2[:,1], h_2[:,0], 'm+', label='two opt heuristic')
        ax.plot(t_1[:,1], t_1[:,0], 'b+', label='random mcts')
        ax.plot(t_2[:,1], t_2[:,0], 'c+', label='greedy mcts')
        ax.set_xscale('log')
        ax.set_xlabel('time (s)')
        ax.set_ylabel('cost')
        ax.set_title("Time-Cost Performance (num_of_node={:d}, side_length={:d})".format(num_of_node, side_length))

        # put legend below current axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                  fancybox=True, shadow=True, ncol=5)

        plt.show()


        ### cost histogram
        bin_start = int(np.amin(results[:, :, 0])/20) * 20
        bin_end = int(np.amax(results[:, :, 0])/20) * 20 + 21
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,8))
        ax.hist(h_1[:,0], bins=range(bin_start, bin_end, 20), density=True, alpha=0.6, color= 'r', label='greedy heuristic')
        ax.hist(h_2[:,0], bins=range(bin_start, bin_end, 20), density=True, alpha=0.6, color= 'm', label='two opt heuristic')
        ax.hist(t_1[:,0], bins=range(bin_start, bin_end, 20), density=True, alpha=0.6, color= 'b', label='random mcts')
        ax.hist(t_2[:,0], bins=range(bin_start, bin_end, 20), density=True, alpha=0.6, color= 'c', label='greedy mcts')
        ax.set_xlabel('cost')
        ax.set_ylabel('frequency')
        ax.set_title("Cost Histogram (num_of_node={:d}, side_length={:d})".format(num_of_node, side_length))

        # put legend below current axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                  fancybox=True, shadow=True, ncol=5)

        plt.show()
