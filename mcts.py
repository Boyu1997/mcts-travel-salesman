import copy
import random
import numpy as np

class Node():
    def __init__(self, parent, node, path, unvisited_nodes, cost):
        self.parent = parent
        self.node = node
        self.path = path
        self.unvisited_nodes = unvisited_nodes
        self.cost = cost
        self.score = None
        self.policy = None
        self.expendables = copy.deepcopy(unvisited_nodes)
        random.shuffle(self.expendables)
        self.expended = {}



class MCTS():

    def __init__(self, network):
        self.graph = network.graph
        self.root = Node(None, 'root', [], list(self.graph.nodes), 0)


    def expand(self, node):
        new_node = node.expendables.pop()
        new_path = copy.deepcopy(node.path)
        new_path.append(new_node)
        new_unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        new_unvisited_nodes.remove(new_node)
        new_cost = copy.deepcopy(node.cost)
        if node.node != 'root':
            new_cost += self.graph.edges[node.node, new_node]['weight']
        new_node_object = Node(node, new_node, new_path, new_unvisited_nodes, new_cost)
        node.expended[new_node] = new_node_object
        return new_node_object


    def run(self, num_of_expand, num_of_simulate):
        current_node = self.root
        while True:
            # reach the end, break condition
            if len(current_node.expendables) == 0:
                break

            # expand and simulate
            for i in range(min(num_of_expand, len(current_node.expendables))):
                new_node = self.expand(current_node)
                costs = []
                for j in range(num_of_simulate):
                    costs.append(self.simulate(new_node))
                new_node.score = sum(costs) / num_of_simulate

            # back up the score and update policy
            self.backpropagate(current_node)


    def backpropagate(self, node):
        scores = [[key, n.score] for key, n in node.expended.items()]
        scores = np.array(scores)
        node.score = sum(scores[:, 1]) / len(scores)
        node.policy = scores[np.argmin(scores[:, 1])][0]
        if node.parent != None:
            self.backpropagate(node.parent)


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
