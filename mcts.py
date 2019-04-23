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
        self.root = Node('root', [], list(self.graph.nodes), 0)
        for _ in range(len(self.graph.nodes)):
            self.expand(self.root)


    def expand(self, node):
        new_node = node.expendables.pop()
        new_path = copy.deepcopy(node.path)
        new_unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        new_unvisited_nodes.remove(new_node)
        new_cost = copy.deepcopy(node.cost)
        if node.node != 'root':
            new_path.append(node.node)
            new_cost += self.graph.edges[node.node, new_node]['weight']
        new_node_object = Node(new_node, new_path, new_unvisited_nodes, new_cost)
        node.expanded[new_node] = new_node_object
        return new_node_object



class RandomMCTS(MCTS):

    def __init__(self, network):
        MCTS.__init__(self, network)


    def simulate(self, node):

        # setup
        unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        random.shuffle(unvisited_nodes)
        current_node = node.node
        cost = 0

        # path finding
        while len(unvisited_nodes) > 0:
            next_node = unvisited_nodes.pop()
            cost += self.graph.edges[current_node, next_node]['weight']
            current_node = next_node

        cost += self.graph.edges[current_node, node.path[0]]['weight']

        return cost


    def run(self, num_of_expand, num_of_simulate):
        current_node = self.root.expanded[0]
        while True:
            if len(current_node.expendables) == 0:
                break
            for i in range(min(num_of_expand, len(current_node.expendables))):
                new_node = self.expand(current_node)
                costs = []
                for j in range(num_of_simulate):
                    costs.append(self.simulate(new_node))
                new_node.score = sum(costs) / num_of_simulate
