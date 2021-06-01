class CustomException(Exception):
    pass


class EdgeException(CustomException):
    def __init__(self, edge):
        super(EdgeException, self).__init__(
            "\nEdge between " + str(edge.starting_vertex) + " and " + str(edge.ending_vertex) + " doesn't exist. \n")


class NonEdgeException(CustomException):
    def __init__(self, edge):
        super(NonEdgeException, self).__init__(
            "\nEdge between " + str(edge.starting_vertex) + " and " + str(edge.ending_vertex) + " already exists. \n")


class VertexException(CustomException):
    def __init__(self, vertex):
        super(VertexException, self).__init__("\nVertex " + str(vertex) + " doesn't exist. \n")


class NonVertexException(CustomException):
    def __init__(self, vertex):
        super(NonVertexException, self).__init__("\nVertex " + str(vertex) + " already exists. \n")


class InvalidOptionException(CustomException):
    def __init__(self):
        super(InvalidOptionException, self).__init__("\nInvalid option. \n")


class IntegerException(CustomException):
    def __init__(self, value):
        super(IntegerException, self).__init__(value + " is not a valid integer.")


class LimitSurpassedException(CustomException):
    def __init__(self, vertices, edges):
        super(LimitSurpassedException, self).__init__(
            "\n" + str(vertices) + " vertices can only have " + str(vertices * vertices) + " edges, not " + str(
                edges) + " edges. \n")


class NotFileException(CustomException):
    def __init__(self):
        super(NotFileException, self).__init__("\nFile doesn't exist.\n")
