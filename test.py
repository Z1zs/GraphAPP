from graph import Graph
from MyAlgorithm import AntiTopologicalSort

graph = Graph()
graph.add_vertex("v1")
graph.add_vertex("v2")
graph.add_vertex("v3")
graph.add_edge("v1", "v2", 2)
graph.add_edge("v2", "v1", 1)
graph.add_edge("v2", "v3", 1)
graph.add_vertex("v4")
flag, vlist = AntiTopologicalSort(graph)
print(flag)
print(vlist)
