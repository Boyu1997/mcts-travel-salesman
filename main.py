from network import RandomNetwork
from heuristic import nearest_neighbor

n = RandomNetwork(20, 100)
visited_edges, cost = nearest_neighbor(n.graph)
print (visited_edges, cost)
