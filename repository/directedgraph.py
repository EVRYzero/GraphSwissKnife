import copy
import math
from pathlib import Path
import random

from debug.checks import Checks, NonVertexException
from domain.edges import Edge


class DirectedGraph:
    def __init__(self, vertices=0, edges=0, dictionary_in=None, dictionary_out=None, dictionary_costs=None):
        if dictionary_in is None:
            dictionary_in = {}
        if dictionary_out is None:
            dictionary_out = {}
        if dictionary_costs is None:
            dictionary_costs = {}
        self.__vertices = vertices
        self.__edges = edges
        self.__dictionary_in = copy.deepcopy(dictionary_in)
        self.__dictionary_out = copy.deepcopy(dictionary_out)
        self.__dictionary_costs = copy.deepcopy(dictionary_costs)

    def generate(self, vertices, edges):
        Checks().EdgesLimitCheck(vertices, edges)
        self.__clear()
        for vertex in range(0, vertices):
            self.add_vertex(vertex)
        potential_starting_vertex_candidates = [element for element in range(0, vertices)]
        while self.__edges < edges:
            if not potential_starting_vertex_candidates:
                break
            random_starting_vertex = random.choice(potential_starting_vertex_candidates)
            potential_ending_vertex_candidates = [element for element in range(0, vertices) if
                                                  element not in self.__dictionary_out[random_starting_vertex]]
            if not potential_ending_vertex_candidates:
                potential_starting_vertex_candidates.remove(random_starting_vertex)
                continue
            random_ending_vertex = random.choice(potential_ending_vertex_candidates)
            self.add_edge(Edge(random_starting_vertex, random_ending_vertex, random.randint(1, 20)))

    def ingress(self, file_name):
        location = file_name.split('/')
        path = Path(__file__).parent.parent / file_name
        Checks().FileExistence(path)
        self.__clear()
        file = open(path, 'rt')
        structure = file.readline()
        structure = structure[:-1].split(' ')
        lines = file.readlines()
        if location[0] == "templates":
            while self.__vertices < int(structure[0]):
                self.add_vertex(self.__vertices)
            for line in lines:
                if line[-1] == '\n':
                    line = line[:-1]
                line = line.split(' ')
                if self.__edges < int(structure[1]):
                    self.add_edge(Edge(int(line[0]), int(line[1]), int(line[2])))
        else:
            for line in lines:
                if line[-1] == '\n':
                    line = line[:-1]
                line = line.split(' ')
                if len(line) == 1:
                    try:
                        if self.__vertices < int(structure[0]):
                            self.add_vertex(int(line[0]))
                    except NonVertexException:
                        pass
                else:
                    try:
                        if self.__vertices < int(structure[0]):
                            self.add_vertex(int(line[0]))
                    except NonVertexException:
                        pass
                    try:
                        if self.__vertices < int(structure[0]):
                            self.add_vertex(int(line[1]))
                    except NonVertexException:
                        pass
                    if self.__edges < int(structure[1]):
                        self.add_edge(Edge(int(line[0]), int(line[1]), int(line[2])))
        file.close()

    def egress(self, file_name):
        path = Path(__file__).parent.parent / file_name
        file = open(path, 'wt')
        line = str(self.__vertices) + " " + str(self.__edges) + "\n"
        file.write(line)
        for starting_vertex in self.__dictionary_out.keys():
            if not self.__dictionary_out[starting_vertex]:
                line = str(starting_vertex) + "\n"
                file.write(line)
            else:
                for ending_vertex in self.__dictionary_out[starting_vertex]:
                    cost = self.__dictionary_costs[(starting_vertex, ending_vertex)]
                    line = str(starting_vertex) + " " + str(ending_vertex) + " " + str(cost) + "\n"
                    file.write(line)
        file.close()

    def __clear(self):
        self.__vertices = 0
        self.__edges = 0
        self.__dictionary_in.clear()
        self.__dictionary_out.clear()
        self.__dictionary_costs.clear()

    @property
    def dictionary_in(self):
        return self.__dictionary_in

    @property
    def dictionary_out(self):
        return self.__dictionary_out

    @property
    def dictionary_costs(self):
        return self.__dictionary_costs

    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    def add_vertex(self, vertex):
        Checks().InboundVertexNonExistence(self, vertex)
        Checks().OutboundVertexNonExistence(self, vertex)
        self.__dictionary_in[vertex] = []
        self.__dictionary_out[vertex] = []
        self.__vertices += 1

    def remove_vertex(self, vertex):
        Checks().InboundVertexExistence(self, vertex)
        Checks().OutboundVertexExistence(self, vertex)
        first_result = self.search_inbound_edges_bounded_by_vertex(vertex)
        second_result = self.search_outbound_edges_bounded_by_vertex(vertex)
        for bounded_vertex in first_result:
            self.__dictionary_costs.pop((bounded_vertex, vertex))
            self.__dictionary_out[bounded_vertex].remove(vertex)
            self.__edges -= 1
        for bounded_vertex in second_result:
            if self.__dictionary_costs.get((vertex, bounded_vertex), False) is not False:
                self.__dictionary_costs.pop((vertex, bounded_vertex))
                self.__dictionary_in[bounded_vertex].remove(vertex)
                self.__edges -= 1
        self.__dictionary_in.pop(vertex)
        self.__dictionary_out.pop(vertex)
        self.__vertices -= 1

    def add_edge(self, edge):
        Checks().OutboundVertexExistence(self, edge.starting_vertex)
        Checks().InboundVertexExistence(self, edge.ending_vertex)
        Checks().EdgeNonExistence(self, edge)

        if edge.ending_vertex not in self.__dictionary_out[edge.starting_vertex]:
            self.__dictionary_out[edge.starting_vertex].append(edge.ending_vertex)

        if edge.starting_vertex not in self.__dictionary_in[edge.ending_vertex]:
            self.__dictionary_in[edge.ending_vertex].append(edge.starting_vertex)

        if self.__dictionary_costs.get((edge.starting_vertex, edge.ending_vertex), False) is False:
            self.__dictionary_costs[(edge.starting_vertex, edge.ending_vertex)] = edge.cost
            self.__edges += 1

    def remove_edge(self, edge):
        Checks().OutboundVertexExistence(self, edge.starting_vertex)
        Checks().InboundVertexExistence(self, edge.ending_vertex)
        Checks().EdgeExistence(self, edge)

        try:
            self.__dictionary_out[edge.starting_vertex].remove(edge.ending_vertex)
        except ValueError:
            pass

        try:
            self.__dictionary_in[edge.ending_vertex].remove(edge.starting_vertex)
        except ValueError:
            pass

        self.__dictionary_costs.pop((edge.starting_vertex, edge.ending_vertex))
        self.__edges -= 1

    def update_edge(self, edge):
        Checks().OutboundVertexExistence(self, edge.starting_vertex)
        Checks().InboundVertexExistence(self, edge.ending_vertex)
        Checks().EdgeExistence(self, edge)
        self.__dictionary_costs[(edge.starting_vertex, edge.ending_vertex)] = edge.cost

    def search_inbound_edges_bounded_by_vertex(self, vertex):
        Checks().InboundVertexExistence(self, vertex)
        return self.__dictionary_in[vertex]

    def search_outbound_edges_bounded_by_vertex(self, vertex):
        Checks().OutboundVertexExistence(self, vertex)
        return self.__dictionary_out[vertex]

    def check_edge_bounded_by_vertices(self, edge):
        Checks().OutboundVertexExistence(self, edge.starting_vertex)
        Checks().InboundVertexExistence(self, edge.ending_vertex)
        if self.__dictionary_costs.get((edge.starting_vertex, edge.ending_vertex), False) is not False:
            return True
        return False

    def get_in_degree_of_vertex(self, vertex):
        Checks().InboundVertexExistence(self, vertex)
        return len(self.__dictionary_in[vertex])

    def get_out_degree_of_vertex(self, vertex):
        Checks().OutboundVertexExistence(self, vertex)
        return len(self.__dictionary_out[vertex])

    def merge_all_edges_of_vertex(self, vertex):
        Checks().InboundVertexExistence(self, vertex)
        Checks().OutboundVertexExistence(self, vertex)
        edges = []
        for neighbor in self.__dictionary_in[vertex]:
            edges.append(neighbor)
        for neighbor in self.__dictionary_out[vertex]:
            if neighbor not in edges:
                edges.append(neighbor)
        return edges

    def get_component_with_depth_first_transversal(self, vertex):
        Checks().InboundVertexExistence(self, vertex)
        Checks().OutboundVertexExistence(self, vertex)
        # Checks to see if the Vertex exists.
        stack = [vertex]
        # Automatically adds it to the stack.
        visited = set()
        # Starts with no nodes visited.
        while len(stack) != 0:
            # Once the stack is cleared, the process stops.
            node = stack.pop()
            # Pops the top of the stack, so that the search can start.
            visited.add(node)
            # Adds it to the visited (for obvious reasons).
            for neighbor in self.merge_all_edges_of_vertex(node):
                # Gets all neighbors of the given node (inbound AND outbound).
                if neighbor not in visited:
                    # Checks if the neighbor was not previously visited.
                    stack.append(node)
                    stack.append(neighbor)
                    # Appends both the searched node (so that we can get back to it), and the neighbor (to continue the search process depth-first).
                    break
                    # Stops the search process.
        return visited

    def backwards_Dijkstra(self, starting_vertex, ending_vertex):
        Checks().OutboundVertexExistence(self, starting_vertex)
        Checks().InboundVertexExistence(self, ending_vertex)
        # Checks to see if the Vertices exist.
        queue = list()
        queue.append((ending_vertex, 0))
        # Instantiates the queue.
        forward = dict()
        # Used to get the nodes between the starting vertex and the ending vertex.
        distance = dict()
        distance[ending_vertex] = 0
        # Instantiates the distance with the ending vertex as the origin point.
        found = False
        while not len(queue) == 0 and not found:
            # Once the queue is empty or the walk was found, the process stops.
            min_queued_element = queue[0]
            for queued_element in queue:
                if min_queued_element[1] > queued_element[1]:
                    min_queued_element = queued_element
            queue.remove(min_queued_element)
            queued_node = min_queued_element[0]
            # Gets the node with the lowest cost, so that the algorithm can start.
            for neighbor in self.__dictionary_in[queued_node]:
                # Gets all inbound nodes of the given node.
                if neighbor not in distance.keys() or distance[queued_node] + self.__dictionary_costs[(neighbor, queued_node)] < distance[neighbor]:
                    # Checks to see if the neighbor has never had its distance calculated or if the distance of the neighbor is larger than the new distance of the node.
                    distance[neighbor] = distance[queued_node] + self.__dictionary_costs[(neighbor, queued_node)]
                    # Calculates the distance of the neighbor.
                    queue.append((neighbor, distance[neighbor]))
                    # Puts the new neighbor in the queue for possible future calculations.
                    forward[neighbor] = queued_node
                    # Saves the next node for the walk.
            if queued_node == starting_vertex:
                found = True
                # Found the walk.
        return found, forward, distance[starting_vertex] if distance.get(starting_vertex, False) else 0

    def merge_all_edges(self):
        edges = list(self.__dictionary_costs.keys())
        for edge in edges:
            if self.__dictionary_costs.get(edge, False) is not False and self.__dictionary_costs.get((edge[1], edge[0]), False) is not False:
                self.__dictionary_costs[(edge[1], edge[0])] += self.__dictionary_costs[edge]
                self.remove_edge(Edge(*edge, 0))

    def union(self, parent, rank, first_vertex, second_vertex):
        first_root = self.find(parent, first_vertex)
        second_root = self.find(parent, second_vertex)

        if rank[first_root] < rank[second_root]:
            parent[first_root] = second_root
        elif rank[first_root] > rank[second_root]:
            parent[second_root] = first_root
        # We attach the tree with the smaller rank under the root of the tree with the higher rank (Union by Rank)

        else:
            parent[second_root] = first_root
            rank[first_root] += 1
        # If the ranks of both roots are the same, then we make one as the root and increment the other's rank by one

    def find(self, parent, node):
        if parent[node] == node:
            return node
        return self.find(parent, parent[node])

    def kruskal(self):
        result = list()
        # We initialize the list in which we will store all of the edges tied to the Minimal Spanning Tree

        sorted_edges_index = 0
        result_index = 0
        # We initialize the indexes we will use in our upcoming computations

        self.merge_all_edges()
        # We convert the Directed Graph into an Undirected Graph. If the Graph is already Undirected, this function won't modify our Graph.

        sorted_edges = sorted(self.__dictionary_costs.items(), key=lambda edge: edge[1])
        # We sort all of our edges in a non-decreasing order based on their weight. [Complexity of O(E * logE)]

        parent = {}
        rank = {}

        for vertex in self.__dictionary_out.keys():
            parent[vertex] = vertex
            rank[vertex] = 0
        # We create self.vertices subsets with single elements (they are "their own parents").

        while result_index < self.vertices - 1:
            # Number of edges that would belong to the result is equal to self.vertices - 1.
            vertices, cost = sorted_edges[sorted_edges_index]
            # We pick the smallest edge existing in our Graph.
            sorted_edges_index += 1
            # We increment the index for the next iteration.
            parent_starting_vertex = self.find(parent, vertices[0])
            parent_ending_vertex = self.find(parent, vertices[1])
            # We search for the root of our starting vertex and our ending vertex.

            if parent_starting_vertex != parent_ending_vertex:
                # We make sure that including this edge does not cause a cycle by comparing the roots of both vertices belonging to the edge.
                result_index += 1
                # We increment the index of result for our next edge.
                result.append((vertices, cost))
                # We include our edge into our result.
                self.union(parent, rank, parent_starting_vertex, parent_ending_vertex)
                # We apply the union-find algorithm, so that we join the two subsets formed by the two vertices into one.

        minimum_cost = 0
        for vertices, cost in result:
            minimum_cost += cost

        return result, minimum_cost

    def sorted_edges_algorithm(self):
        result = list()
        # We initialize the list in which we will store all of the edges tied to the Hamiltonian Cycle of Low Cost.
        self.merge_all_edges()
        # We convert the Directed Graph into an Undirected Graph. If the Graph is already Undirected, this function won't modify our Graph.
        sorted_edges = sorted(self.__dictionary_costs.items(), key=lambda edge: edge[1])
        # We sort all of our edges in an increasing order based on their weight. [Complexity of O(E * logE)]
        for sorted_edge in sorted_edges:
            result.append(sorted_edge)
            # We add the edge to our result in order to check if a Hamiltonian Cycle is formed with it.
            length = 0
            # We initialize the length of the possible Cycle. This variable will only be used if the result forms a Hamiltonian Cycle.
            color = {}
            # We initialize the dictionary of Colors. We will use 3 colors in order to check the state of each vertex:
            #   GRAY = Has a Degree of One.
            #   WHITE = Has a Degree of Two.
            #   BLACK = Has a Degree of Three or More.
            # Obs: A Hamiltonian Cycle is a closed loop in which every vertex is only passed once (each node inside of the Cycle has a degree of Two).
            for edge in result:
                color[edge[0][0]] = "NONE"
                color[edge[0][1]] = "NONE"
                # We add every single node from Result inside of the Color dictionary with the value "NONE".
                length += 1
                # We also count the length of the possible Cycle.
            for edge in result:
                if color[edge[0][0]] == "NONE":
                    color[edge[0][0]] = "GRAY"
                    # Starting Node has a degree of One.
                elif color[edge[0][0]] == "GRAY":
                    color[edge[0][0]] = "WHITE"
                    # Starting Node has a degree of Two.
                elif color[edge[0][0]] == "WHITE":
                    color[edge[0][0]] = "BLACK"
                    # Starting Node has a degree of Three or More.
                if color[edge[0][1]] == "NONE":
                    color[edge[0][1]] = "GRAY"
                    # Ending Node has a degree of One.
                elif color[edge[0][1]] == "GRAY":
                    color[edge[0][1]] = "WHITE"
                    # Ending Node has a degree of Two.
                elif color[edge[0][1]] == "WHITE":
                    color[edge[0][1]] = "BLACK"
                    # Ending Node has a degree of Three or More.
            if all(element == "WHITE" for element in color.values()) is True:
                # We check if the Result is a Hamiltonian Cycle.
                if length == self.__vertices:
                    # We check if its length is equal to the number of vertices / if it goes through every node inside of the Groph.
                    return result
                    # We found the Hamiltonian Cycle of Low Cost.
                else:
                    # We know that the length of the cycle is smaller than the number of vertices.
                    result.pop(-1)
                    # We remove the recently added edge to destroy the Cycle and continue the search.
            elif any(element == "BLACK" for element in color.values()) is True:
                # We know that the result has been compromised and can no longer be a Hamiltonian Cycle.
                result.pop(-1)
                # We remove the recently added edge to revert its compromised state and continue the search.
        return []
        # The Graph contains no Hamiltonian Cycle of Low Cost.