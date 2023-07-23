from graph import Graph

graph = Graph()
graph.add_vertex("v1")
graph.add_vertex("v2")
graph.add_vertex("v3")
graph.add_edge("v1", "v2", 2)
graph.add_edge("v2", "v1", 1)
graph.add_edge("v2", "v3", 1)
graph.add_vertex("v4")
graph.display()
graph.remove_vertex("v3")
print(graph.check_vertex())
