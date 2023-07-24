from graph import Graph, Vertex, Edge


def TopologicalSort(graph):
    tmp_graph = graph
    vertex_list = []
    isDAG = False
    while (tmp_graph.in_degree_dict != {}):
        isDAG = False
        for vertex in tmp_graph.in_degree_dict.keys():
            if tmp_graph.in_degree_dict[vertex] == 0:
                isDAG = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        if isDAG is False:
            print("Error: The graph is NOT a DAG!")
            return False,vertex_list
        return True, vertex_list

def AntiTopologicalSort(graph):
    tmp_graph = graph
    vertex_list = []
    isDAG = False
    while (tmp_graph.adj_list != {}):
        isDAG = False
        for vertex in tmp_graph.adj_list.keys():
            if len(tmp_graph.adj_list[vertex]) == 0:
                isDAG = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        if isDAG is False:
            print("Error: The graph is NOT a DAG!")
            return False,vertex_list
        return True, vertex_list


def CriticalPath(graph):
    pass