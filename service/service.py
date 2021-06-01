import math

from debug.checks import Checks
from domain.edges import Edge
from repository.directedgraph import DirectedGraph


class Service:
    def __init__(self):
        self.__database = DirectedGraph()
        self.__database_copy = None

    def get_vertices_number(self):
        return self.__database.vertices

    def get_vertices(self):
        return self.__database.dictionary_in.keys()

    def check_edge(self, starting_vertex, ending_vertex):
        Checks().ValueValidity(starting_vertex)
        Checks().ValueValidity(ending_vertex)
        starting_vertex = int(starting_vertex)
        ending_vertex = int(ending_vertex)
        return self.__database.check_edge_bounded_by_vertices(Edge(starting_vertex, ending_vertex, None))

    def get_in_degree_of_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        return self.__database.get_in_degree_of_vertex(vertex)

    def get_out_degree_of_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        return self.__database.get_out_degree_of_vertex(vertex)

    def get_inbound_edges_of_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        return self.__database.search_inbound_edges_bounded_by_vertex(vertex)

    def get_outbound_edges_of_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        return self.__database.search_outbound_edges_bounded_by_vertex(vertex)

    def add_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        self.__database.add_vertex(vertex)

    def delete_vertex(self, vertex):
        Checks().ValueValidity(vertex)
        vertex = int(vertex)
        self.__database.remove_vertex(vertex)

    def add_edge(self, starting_vertex, ending_vertex, cost):
        Checks().ValueValidity(starting_vertex)
        Checks().ValueValidity(ending_vertex)
        Checks().ValueValidity(cost)
        starting_vertex = int(starting_vertex)
        ending_vertex = int(ending_vertex)
        cost = int(cost)
        self.__database.add_edge(Edge(starting_vertex, ending_vertex, cost))

    def delete_edge(self, starting_vertex, ending_vertex):
        Checks().ValueValidity(starting_vertex)
        Checks().ValueValidity(ending_vertex)
        starting_vertex = int(starting_vertex)
        ending_vertex = int(ending_vertex)
        self.__database.remove_edge(Edge(starting_vertex, ending_vertex, None))

    def modify_edge_cost(self, starting_vertex, ending_vertex, cost):
        Checks().ValueValidity(starting_vertex)
        Checks().ValueValidity(ending_vertex)
        Checks().ValueValidity(cost)
        starting_vertex = int(starting_vertex)
        ending_vertex = int(ending_vertex)
        cost = int(cost)
        self.__database.update_edge(Edge(starting_vertex, ending_vertex, cost))

    def import_templated_graph(self, file_name):
        self.__database.ingress("templates/" + file_name)

    def import_exported_graph(self, file_name):
        self.__database.ingress("output/" + file_name)

    def export_graph(self, file_name):
        self.__database.egress("output/" + file_name)

    def generate_graph(self, vertices, edges):
        Checks().ValueValidity(vertices)
        Checks().ValueValidity(edges)
        vertices = int(vertices)
        edges = int(edges)
        self.__database.generate(vertices, edges)

    def copy_graph(self):
        self.__database_copy = DirectedGraph(self.__database.vertices,
                                             self.__database.edges,
                                             self.__database.dictionary_in,
                                             self.__database.dictionary_out,
                                             self.__database.dictionary_costs)

    def get_connected_components_of_graph(self):
        connected_components = [DirectedGraph(self.__database.vertices,
                                              self.__database.edges,
                                              self.__database.dictionary_in,
                                              self.__database.dictionary_out,
                                              self.__database.dictionary_costs)]
        while True:
            base = DirectedGraph(connected_components[len(connected_components) - 1].vertices,
                                 connected_components[len(connected_components) - 1].edges,
                                 connected_components[len(connected_components) - 1].dictionary_in,
                                 connected_components[len(connected_components) - 1].dictionary_out,
                                 connected_components[len(connected_components) - 1].dictionary_costs)
            remains = DirectedGraph(connected_components[len(connected_components) - 1].vertices,
                                    connected_components[len(connected_components) - 1].edges,
                                    connected_components[len(connected_components) - 1].dictionary_in,
                                    connected_components[len(connected_components) - 1].dictionary_out,
                                    connected_components[len(connected_components) - 1].dictionary_costs)
            vertices = list(base.dictionary_in.keys())
            connected_component = base.get_component_with_depth_first_transversal(vertices[0])
            for node in connected_component:
                remains.remove_vertex(node)
            for node in vertices:
                if node not in connected_component:
                    base.remove_vertex(node)
            if remains.vertices > 0:
                connected_components.pop(len(connected_components) - 1)
                connected_components.append(DirectedGraph(base.vertices,
                                                          base.edges,
                                                          base.dictionary_in,
                                                          base.dictionary_out,
                                                          base.dictionary_costs))
                connected_components.append(DirectedGraph(remains.vertices,
                                                          remains.edges,
                                                          remains.dictionary_in,
                                                          remains.dictionary_out,
                                                          remains.dictionary_costs))
            else:
                break
        return connected_components

    def lowest_cost_walk(self, starting_vertex, ending_vertex):
        Checks().ValueValidity(starting_vertex)
        Checks().ValueValidity(ending_vertex)
        starting_vertex = int(starting_vertex)
        ending_vertex = int(ending_vertex)
        return self.__database.backwards_Dijkstra(starting_vertex, ending_vertex)

    def minimal_spanning_tree(self):
        return self.__database.kruskal()

    def hamiltonian_cycle_of_low_cost(self):
        return self.__database.sorted_edges_algorithm()
