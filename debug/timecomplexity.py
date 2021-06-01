import time

from repository.directedgraph import DirectedGraph

database = DirectedGraph()
start = time.time()
database.ingress("input/graph1k.txt")
end = time.time()
print("1k Graph:", end - start, "seconds.")
print("Average:", (end - start) / 4000, "seconds/edge.")
del database
database = DirectedGraph()
start = time.time()
database.ingress("input/graph10k.txt")
end = time.time()
print("10k Graph:", end - start, "seconds.")
print("Average:", (end - start) / 40000, "seconds/edge.")
del database
database = DirectedGraph()
start = time.time()
database.ingress("input/graph100k.txt")
end = time.time()
print("100k Graph:", end - start, "seconds.")
print("Average:", (end - start) / 400000, "seconds/edge.")
del database
database = DirectedGraph()
start = time.time()
database.ingress("input/graph1m.txt")
end = time.time()
print("1m Graph:", end - start, "seconds.")
print("Average:", (end - start) / 4000000, "seconds/edge.")
del database
