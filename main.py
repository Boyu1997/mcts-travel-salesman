from network import Network
from plot import plot_path
from test import single_test, small_test


network = Network(30, 100)
single_test(network, plot=False)
