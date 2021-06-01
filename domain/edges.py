class Edge:
    def __init__(self, starting_vertex, ending_vertex, cost):
        self.__starting_vertex = starting_vertex
        self.__ending_vertex = ending_vertex
        self.__cost = cost

    @property
    def starting_vertex(self):
        return self.__starting_vertex

    @property
    def ending_vertex(self):
        return self.__ending_vertex

    @property
    def cost(self):
        return self.__cost
