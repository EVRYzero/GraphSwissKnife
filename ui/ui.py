from service.service import Service


class UI:
    def __init__(self):
        self.__service = Service()

    @staticmethod
    def main_menu():
        print("==== Assignment One ====")
        print("")
        print("== Vertex Options ==")
        print("")
        print("1. Get the number of existing Vertices.")
        print("2. Get all existing Vertices.")
        print("3. Get the in-degree of an existing Vertex.")
        print("4. Get the out-degree of an existing Vertex.")
        print("5. Get the inbound Edges of an existing Vertex.")
        print("6. Get the outbound Edges of an existing Vertex.")
        print("7. Add a new Vertex.")
        print("8. Remove an existing Vertex.")
        print("")
        print("== Edge Options ==")
        print("")
        print("9. Add a new Edge.")
        print("10. Remove an existing Edge.")
        print("11. Modify the Edge's cost.")
        print("12. Check the Edge's existence.")
        print("")
        print("== Graph Options ==")
        print("")
        print("13. Import a template Graph.")
        print("14. Generate a random Graph.")
        print("15. Import an exported Graph.")
        print("16. Export the current Graph.")
        print("17. Copy Graph locally.")
        print("")
        print("== Exercises ==")
        print("")
        print("18. Write a program that finds the connected components of an undirected graph using a depth-first traversal of the graph. {Lab 2, Exercise 3}")
        print("19. Write a program that, given a graph with positive costs and two vertices, finds a lowest cost walk between the given vertices, using a backwards Dijkstra algorithm (Dijkstra algorithm that searches backwards, from the ending vertex). {Lab 3, Exercise 2}")
        print("20. Write a program that, given an undirected connected graph, constructs a minumal spanning tree using the Kruskal's algorithm. {Lab 4, Exercise 5} [UNCHECKED]")
        print("21. Given an undirected graph with costs, find a Hamiltonian cycle of low cost (approximate TSP) by using the heuristic of sorting the edges in increasing order of their costs and, for each edge, choose it if and only if it does not close a cycle of length lower than n. {Lab 5, Exercise 9} [UNCHECKED]")
        print("")
        print("0. Exit.")
        print("")

    def get_vertices_number(self):
        print("\nNumber of vertices:" + str(self.__service.get_vertices_number()) + "\n")

    def get_vertices(self):
        print("\nVertices:", end=" ")
        for element in self.__service.get_vertices():
            print(element, end=" ")
        print("\n")

    def check_edge(self):
        starting_vertex = input("The starting vertex of the searched edge: ")
        ending_vertex = input("The ending vertex of the searched edge: ")
        if self.__service.check_edge(starting_vertex, ending_vertex):
            print("\nEdge between " + starting_vertex + " and " + ending_vertex + " exists.\n")
        else:
            print("\nEdge between " + starting_vertex + " and " + ending_vertex + " doesn't exist.\n")

    def get_in_degree_of_vertex(self):
        vertex = input("The searched vertex to get the in-degree of: ")
        print("\nThe vertex " + vertex + " has the in-degree of " + str(
            self.__service.get_in_degree_of_vertex(vertex)) + "\n")

    def get_out_degree_of_vertex(self):
        vertex = input("The searched vertex to get the out-degree of: ")
        print("\nThe vertex " + vertex + " has the in-degree of " + str(
            self.__service.get_out_degree_of_vertex(vertex)) + "\n")

    def get_inbound_edges_of_vertex(self):
        vertex = input("The searched vertex to get the inbound edges of: ")
        result = str(self.__service.get_inbound_edges_of_vertex(vertex))
        print("\nThe inbound edges of vertex " + vertex + " are:", end=" ")
        if result == "[]":
            print("None")
        else:
            result = result[1:-1]
            result = result.split(',')
            for temporary_vertex in result:
                print("(" + temporary_vertex.strip() + ", " + vertex.strip() + ")", end=" ")
        print("\n")

    def get_outbound_edges_of_vertex(self):
        vertex = input("\nThe searched vertex to get the outbound edges of: ")
        result = str(self.__service.get_outbound_edges_of_vertex(vertex))
        print("\nThe outbound edges of vertex " + vertex + " are:", end=" ")
        if result == "[]":
            print("None")
        else:
            result = result[1:-1]
            result = result.strip().split(',')
            for temporary_vertex in result:
                print("(" + vertex.strip() + ", " + temporary_vertex.strip() + ")", end=" ")
        print("\n")

    def add_vertex(self):
        vertex = input("The vertex you want to add: ")
        self.__service.add_vertex(vertex)
        print("\nVertex added successfully.\n")

    def delete_vertex(self):
        vertex = input("The vertex you want to delete: ")
        self.__service.delete_vertex(vertex)
        print("\nVertex deleted successfully.\n")

    def add_edge(self):
        starting_vertex = input("The starting vertex of the edge you want to add: ")
        ending_vertex = input("The ending vertex of the edge you want to add: ")
        cost = input("The cost of the edge you want to add: ")
        self.__service.add_edge(starting_vertex, ending_vertex, cost)
        print("\nEdge added successfully.\n")

    def delete_edge(self):
        starting_vertex = input("The starting vertex of the edge you want to delete: ")
        ending_vertex = input("The ending vertex of the edge you want to delete: ")
        self.__service.delete_edge(starting_vertex, ending_vertex)
        print("\nEdge deleted successfully.\n")

    def modify_edge_cost(self):
        starting_vertex = input("The starting vertex of the edge you want to update: ")
        ending_vertex = input("The ending vertex of the edge you want to update: ")
        cost = input("The cost of the edge you want to update to: ")
        self.__service.modify_edge_cost(starting_vertex, ending_vertex, cost)
        print("\nEdge modified successfully.\n")

    def import_templated_graph(self):
        file_name = input("The name of the file you want to import the graph from: ")
        self.__service.import_templated_graph(file_name)
        print("\nImport successful.\n")

    def import_exported_graph(self):
        file_name = input("The name of the file you want to import the graph from: ")
        self.__service.import_exported_graph(file_name)
        print("\nImport successful.\n")

    def export_graph(self):
        file_name = input("The name of the file you want to export the graph to: ")
        self.__service.export_graph(file_name)
        print("\nExport successful.\n")

    def generate_graph(self):
        vertices = input("The number of vertices you want in the random graph: ")
        edges = input("The number of edges you want in the random graph: ")
        self.__service.generate_graph(vertices, edges)
        print("\nGeneration successful.\n")

    def copy_graph(self):
        self.__service.copy_graph()
        print("\nCopy successful.\n")

    def get_connected_components_of_graph(self):
        components = self.__service.get_connected_components_of_graph()
        print("\nConnected Components:")
        index = 1
        for component in components:
            print("Component #" + str(index) + ":")
            print("Nodes:", end=" ")
            for node in component.dictionary_in.keys():
                print(node, end="; ")
            print("")
            print("Edges:", end=" ")
            for edge in component.dictionary_costs.keys():
                print(edge, end="; ")
            print("")
            print("")
            index += 1

    def lowest_cost(self):
        starting_vertex = input("The starting vertex of the Walk you want to search for: ")
        ending_vertex = input("The ending vertex of the Walk you want to search for: ")
        found, forward, cost = self.__service.lowest_cost_walk(starting_vertex, ending_vertex)
        if found:
            print("\nPath:", end=" ")
            starting_vertex = int(starting_vertex)
            ending_vertex = int(ending_vertex)
            vertex = starting_vertex
            print(vertex, end="; ")
            while vertex != ending_vertex:
                vertex = forward[vertex]
                print(vertex, end="; ")
            print()
            print("Cost: " + str(cost) + "\n")
        else:
            print("\nSuch a walk doesn't exist.\n")

    def minimal_spanning_tree(self):
        print("In order to get the minimum spanning tree, the directed graph will be modified so that it fits the undirected graph criteria.")
        print("If two separate edges are found between two vertices, one of the edges is deleted and their costs are merged into the remaining one using ADDITION.\n")
        tree, minimum_cost = self.__service.minimal_spanning_tree()
        print("Minimum Spanning Tree:")
        for vertices, cost in tree:
            print(str(vertices[0]) + " ---" + str(cost) + "--- " + str(vertices[1]))
        print("Total Cost: " + str(minimum_cost) + "\n")

    def hamiltonian_cycle_of_low_cost(self):
        print("In order to get the hamiltonian cycle of low cost, the directed graph will be modified so that it fits the undirected graph criteria.")
        print("If two separate edges are found between two vertices, one of the edges is deleted and their costs are merged into the remaining one using ADDITION.\n")
        cycle = self.__service.hamiltonian_cycle_of_low_cost()
        if len(cycle) == 0:
            print("There is no Hamiltonian Cycle of Low Cost.")
        else:
            print("Hamiltonian Cycle of Low Cost: ")
            for vertices, cost in cycle:
                print(str(vertices[0]) + " ---" + str(cost) + "--- " + str(vertices[1]))
        print("\n")