from network import Network
from plot import plot_path
from test import test
from simulation import simulation

# test(num_of_node, side_length=100, plot=False)
test(30, plot=True)

# simulation(num_of_network, trail_per_network, num_of_node, side_length=100, plot=False)
simulation(50, 10, 30, plot=True)
