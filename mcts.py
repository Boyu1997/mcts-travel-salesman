import copy
import random
import numpy as np

### Node Object ###
class Node():
    def __init__(self, parent, node, path, unvisited_nodes, cost):
        self.parent = parent
        self.node = node
        self.path = path
        self.unvisited_nodes = unvisited_nodes
        self.cost = cost
        self.num_of_visit = 1
        self.estimate = None
        self.score = None
        self.policy = None
        self.expandables = copy.deepcopy(unvisited_nodes)
        random.shuffle(self.expandables)
        self.expanded = {}

    def calculate_score(self, C=1):
        self.score = self.estimate + C * (np.log(self.parent.num_of_visit) / self.num_of_visit)**0.5



class MCTS():

    def __init__(self, network):
        self.num_of_node = network.num_of_node
        self.graph = network.graph
        self.root = Node(None, 'root', [], list(self.graph.nodes), 0)


    def select(self, node):
        if node.policy == None:
            return node
        else:
            return self.select(node.policy)


    def expand(self, node):
        new_node = node.expandables.pop()
        new_path = copy.deepcopy(node.path)
        new_path.append(new_node)
        new_unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        new_unvisited_nodes.remove(new_node)
        new_cost = copy.deepcopy(node.cost)
        if node.node != 'root':
            new_cost += self.graph.edges[node.node, new_node]['weight']
        new_node_object = Node(node, new_node, new_path, new_unvisited_nodes, new_cost)
        node.expanded[new_node] = new_node_object
        return new_node_object


    def backpropagate(self, node):

        # decide policy for this node
        scores = []
        for key, n in node.expanded.items():
            if node.node != 'root':
                scores.append([key, n.score + self.graph.edges[node.node, n.node]['weight']])
            else:
                scores.append([key, n.score])
        scores = np.array(scores)
        node.score = sum(scores[:, 1]) / len(scores)
        node.policy = node.expanded[scores[np.argmin(scores[:, 1])][0]]

        if node.node != 'root':

            # evaluate how good this node is as a child
            estimates = []
            for key, n in node.expanded.items():
                estimates.append([key, n.estimate + self.graph.edges[node.node, n.node]['weight']])
            estimates = np.array(estimates)
            node.estimate = sum(estimates[:, 1]) / len(estimates)
            node.calculate_score()

            # keep going until root node
            self.backpropagate(node.parent)


    def calculate_path_edges(self, path):
        path_edges = []
        cost = 0
        current_node = path.pop()
        while len(path) > 0:
            next_node = path.pop()
            path_edges.append(tuple([current_node, next_node,
                                     self.graph.edges[current_node, next_node]]))
            cost += path_edges[-1][2]['weight']
            current_node = next_node
        path_edges.append(tuple([path_edges[-1][1], path_edges[0][0],
                                 self.graph.edges[path_edges[-1][1], path_edges[0][1]]]))
        cost += path_edges[-1][2]['weight']
        return path_edges, cost


    def run(self, num_of_expand, num_of_simulate, C):
        while True:
            current_node = self.select(self.root)

            # reach the end, break condition
            if len(current_node.path) == self.num_of_node:
                break

            # expand and simulate
            for i in range(min(num_of_expand, len(current_node.expandables))):
                new_node = self.expand(current_node)
                costs = []
                for j in range(num_of_simulate):
                    costs.append(self.simulate(new_node))
                new_node.estimate = sum(costs) / num_of_simulate
                new_node.calculate_score()


            # back up the estimate, calculate score, and update policy
            self.backpropagate(current_node)

        return self.calculate_path_edges(current_node.path)



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



class GreedyMCTS(MCTS):

    def __init__(self, network, prob_greedy):
        MCTS.__init__(self, network)
        self.prob_greedy = prob_greedy


    def simulate(self, node):

        # setup
        unvisited_nodes = copy.deepcopy(node.unvisited_nodes)
        random.shuffle(unvisited_nodes)
        current_node = node.node
        cost = 0

        # greedy path finding
        while len(unvisited_nodes) > 0:
            if random.random() < self.prob_greedy:
                edges = []
                for n in unvisited_nodes:
                    edges.append(tuple([current_node, n, self.graph.edges[current_node, n]]))
                edges = sorted(edges, key = lambda x: x[2]['weight'], reverse=False)
                unvisited_nodes.remove(edges[0][1])
                cost += edges[0][2]['weight']
                current_node = edges[0][1]
            else:
                next_node = unvisited_nodes.pop()
                cost += self.graph.edges[current_node, next_node]['weight']
                current_node = next_node

        cost += self.graph.edges[current_node, node.path[0]]['weight']

        return cost
