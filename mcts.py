import copy
import random

class Node():
    def __init__(self, node, path, unvisited_nodes, cost):
        self.node = node
        self.path = path
        self.unvisited_nodes = unvisited_nodes
        self.cost = cost
        self.score = None
        self.policy = None
        self.expendables = copy.deepcopy(unvisited_nodes)
        random.shuffle(self.expendables)
        self.expanded = dict()



class MCTS():

    def __init__(self, network):
        self.graph = network.graph
        self.tree = Node('root', [], list(self.graph.nodes), 0)

    def expand(self, node):
        new_node = node.expendables.pop()
        new_path = copy.deepcopy(node.path)
        new_path.append(node)
        new_unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        new_unvisited_nodes.remove(new_node)
        new_cost = copy.deepcopy(node.cost)
        if node.node != 'root':
            new_cost += self.graph.edges[node.node, new_node]['weight']
        new_node_object = Node(new_node, new_path, new_unvisited_nodes, new_cost)
        node.expanded[new_node] = new_node_object
        return new_node_object



class RandomMCTS(MCTS):

    def __init__(self, network):
        MCTS.__init__(self, network)

    def run(self):
        next_node = self.expand(self.tree)
        third_node = self.expand(next_node)
        print (third_node.cost)
