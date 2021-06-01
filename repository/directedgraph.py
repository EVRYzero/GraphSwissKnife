import copy
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