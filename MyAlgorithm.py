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

def VEPath(graph):

def VLPath(graph,vedict):

def EPath(graph,vedict):

def LPath(graph,vldict):

def CPath(edict,ldict):

def CriticalPath(graph):
    isTopo,_=TopologicalSort(graph)
    vedict=VEPath(graph)
    vldict=VLPath(graph,vedict)

    edict=EPath(graph,vedict)
    ldict=LPath(graph,vldict)

    ddict=CPath(edict,ldict)

    critical_path=[]

    pass