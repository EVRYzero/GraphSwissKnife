from debug.exceptions import *


class Checks:

    @staticmethod
    def EdgeNonExistence(graph, edge):
        if graph.dictionary_in.get((edge.starting_vertex, edge.ending_vertex)) is not None:
            raise NonEdgeException(edge)

    @staticmethod
    def EdgeExistence(graph, edge):
        if graph.dictionary_in.get((edge.starting_vertex, edge.ending_vertex)) is None:
            raise EdgeException(edge)

    @staticmethod
    def InboundVertexNonExistence(graph, vertex):
        if graph.dictionary_in.get(vertex) is not None:
            raise NonVertexException(vertex)

    @staticmethod
    def InboundVertexExistence(graph, vertex):
        if graph.dictionary_in.get(vertex) is None:
            raise VertexException(vertex)

    @staticmethod
    def OutboundVertexNonExistence(graph, vertex):
        if graph.dictionary_out.get(vertex) is not None:
            raise NonVertexException(vertex)

    @staticmethod
    def OutboundVertexExistence(graph, vertex):
        if graph.dictionary_out.get(vertex) is None:
            raise VertexException(vertex)

    @staticmethod
    def ValueValidity(value):
        try:
            value = int(value)
        except ValueError:
            raise IntegerException(value)

    @staticmethod
    def EdgesLimitCheck(vertices, edges):
        if edges > vertices * vertices:
            raise LimitSurpassedException(vertices, edges)

    @staticmethod
    def FileExistence(path):
        if not path.is_file():
            raise NotFileException()
