from graph import Graph, Vertex, Edge
from typing import List, Dict


def TopologicalSort(graph: Graph):
    tmp_graph = graph
    vertex_list = []
    isDAG = False
    while tmp_graph.in_degree_dict != {}:
        isDAG = False
        for vertex in tmp_graph.in_degree_dict.keys():
            if tmp_graph.in_degree_dict[vertex] == 0:
                isDAG = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        if isDAG is False:
            print("Error: The graph is NOT a DAG!")
            return False, vertex_list
    return True, vertex_list


def AntiTopologicalSort(graph: Graph):
    tmp_graph = graph
    vertex_list = []
    isDAG = False
    while tmp_graph.adj_list != {}:
        isDAG = False
        for vertex in tmp_graph.adj_list.keys():
            if len(tmp_graph.adj_list[vertex]) == 0:
                isDAG = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        if isDAG is False:
            print("Error: The graph is NOT a DAG!")
            return False, vertex_list
    return True, vertex_list


def VEPath(graph: Graph, tplist: List[Vertex]):
    predecessor_dict = graph.get_predecessor()
    print(predecessor_dict)
    ve_dict = {}
    for vertex in tplist:
        if graph.in_degree_dict[vertex] == 0:
            ve_dict[vertex] = 0
        else:
            ve = 0
            for predecessor in predecessor_dict[vertex]:
                # 取所有前驱结点的最大值
                if ve < ve_dict[predecessor.start_vertex] + predecessor.weight:
                    ve = ve_dict[predecessor.start_vertex] + predecessor.weight
            ve_dict[vertex] = ve
    return ve_dict


def VLPath(graph: Graph, vedict: Dict[Vertex, int], atplist: List[Vertex]):
    vl_dict = {}
    for vertex in atplist:
        if len(graph.adj_list[vertex]) == 0:
            vl_dict[vertex] = vedict[vertex]
        else:
            vl = 1e+10
            for successor in graph.adj_list[vertex]:
                # 所有后继节点的最小值
                if vl > vl_dict[successor.end_vertex] - successor.weight:
                    vl = vl_dict[successor.end_vertex] - successor.weight
            vl_dict[vertex] = vl
    return vl_dict


def EPath(graph: Graph, vedict: Dict[Vertex, int]):
    edict = {}
    for vertex in graph.adj_list.keys():
        for edge in graph.adj_list[vertex]:
            edict[edge] = vedict[vertex]
    return edict


def LPath(graph: Graph, vldict: Dict[Vertex, int]):
    ldict = {}
    for vertex in graph.adj_list.keys():
        for edge in graph.adj_list[vertex]:
            ldict[edge] = vldict[edge.end_vertex] - edge.weight
    return ldict


def DPath(edict: Dict[Edge, int], ldict: Dict[Edge, int]):
    ddict = {}
    for edge in edict.keys():
        ddict[edge] = ldict[edge] - edict[edge]
    return ddict


def CriticalPath(graph: Graph):
    # 得到拓扑排序和逆拓扑排序序列
    isTopo, TPlist = TopologicalSort(graph)
    _, ATPlist = AntiTopologicalSort(graph)
    # 得ve和vl
    vedict = VEPath(graph, TPlist)
    vldict = VLPath(graph, vedict, ATPlist)
    # 得e和l
    edict = EPath(graph, vedict)
    ldict = LPath(graph, vldict)

    ddict = DPath(edict, ldict)

    critical_path = [edge for edge in ddict.keys() if ddict[edge] == 0]  # 关键路径
    return critical_path, vedict, vldict, edict, ldict, ddict
