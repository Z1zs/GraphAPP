from graph import Graph, Vertex, Edge
from typing import List, Dict
import copy


# 拓扑排序
def TopologicalSort(_graph: Graph):
    # 需要不断删除结点，故需要深拷贝
    tmp_graph = copy.deepcopy(_graph)
    vertex_list = []
    isdag = False

    while tmp_graph.in_degree_dict != {}:
        # 依次删除入度为0的点
        isdag = False
        for vertex in tmp_graph.in_degree_dict.keys():
            if tmp_graph.in_degree_dict[vertex] == 0:
                isdag = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        # 找不到入度为0的点，非有向无环图
        if isdag is False:
            print("Error: The graph is NOT a DAG!")
            return isdag, vertex_list
    return isdag, vertex_list


# 逆拓扑排序
def AntiTopologicalSort(_graph: Graph):
    tmp_graph = copy.deepcopy(_graph)
    vertex_list = []
    isdag = False
    while tmp_graph.adj_list != {}:
        # 依次删除出度为0的点
        isdag = False
        for vertex in tmp_graph.adj_list.keys():
            if len(tmp_graph.adj_list[vertex]) == 0:
                isdag = True
                vertex_list.append(vertex)
                tmp_graph.remove_vertex(vertex)
                break
        # 找不到出度为0的点，非有向无环图
        if isdag is False:
            print("Error: The graph is NOT a DAG!")
            return isdag, vertex_list
    return isdag, vertex_list


# 求ve
def VEPath(_graph: Graph, tplist: List[Vertex]):
    # 获得各顶点的前驱节点
    predecessor_dict = _graph.get_predecessor()
    ve_dict = {}
    # 按拓扑排序顺序
    for vertex in tplist:
        if _graph.in_degree_dict[vertex] == 0:
            ve_dict[vertex] = 0
        else:
            ve = 0
            for predecessor in predecessor_dict[vertex]:
                # 取所有前驱结点的最大值
                if ve < ve_dict[predecessor.start_vertex] + predecessor.weight:
                    ve = ve_dict[predecessor.start_vertex] + predecessor.weight
            ve_dict[vertex] = ve
    return ve_dict


# 求vl
def VLPath(_graph: Graph, vedict: Dict[Vertex, int], atplist: List[Vertex]):
    vl_dict = {}
    # 逆拓扑排序顺序
    for vertex in atplist:
        if len(_graph.adj_list[vertex]) == 0:
            vl_dict[vertex] = vedict[vertex]
        else:
            vl = 1e+10
            # 需要用到后继节点，直接利用邻接链表即可
            for successor in _graph.adj_list[vertex]:
                # 所有后继节点的最小值
                if vl > vl_dict[successor.end_vertex] - successor.weight:
                    vl = vl_dict[successor.end_vertex] - successor.weight
            vl_dict[vertex] = vl
    return vl_dict


# 求e
def EPath(_graph: Graph, vedict: Dict[Vertex, int]):
    edict = {}
    for vertex in _graph.adj_list.keys():
        for edge in _graph.adj_list[vertex]:
            edict[edge] = vedict[vertex]
    return edict


# 求l
def LPath(_graph: Graph, vldict: Dict[Vertex, int]):
    ldict = {}
    for vertex in _graph.adj_list.keys():
        for edge in _graph.adj_list[vertex]:
            ldict[edge] = vldict[edge.end_vertex] - edge.weight
    return ldict


# 求l-e
def DPath(edict: Dict[Edge, int], ldict: Dict[Edge, int]):
    ddict = {}
    for edge in edict.keys():
        ddict[edge] = ldict[edge] - edict[edge]
    return ddict


# 将关键路径拆分（即处理多条路径情况）

def SplitPath(edge_list):
    if len(edge_list) <= 1:
        return edge_list
    path_list = []
    dist = edge_list[-1].end_vertex

    path_list.append(edge_list[0])
    tmp = edge_list[0].end_vertex
    while tmp != dist:
        for edge in edge_list:
            if edge.start_vertex == tmp:
                path_list.append(edge)
                tmp = edge.end_vertex
    return path_list


# 求关键路径
def CriticalPath(_graph: Graph):
    # 得到拓扑排序和逆拓扑排序序列
    (is_topo, tplist) = TopologicalSort(_graph)
    _, anti_tplist = AntiTopologicalSort(_graph)
    if not is_topo:
        print("Not TopoSortable!")
        return False
    # 得ve和vl
    vedict = VEPath(_graph, tplist)
    vldict = VLPath(_graph, vedict, anti_tplist)
    # 得e和l
    edict = EPath(_graph, vedict)
    ldict = LPath(_graph, vldict)
    # 求L-E
    ddict = DPath(edict, ldict)
    # L-E==0的边即位于关键路径上
    critical_path = []  # 关键路径
    for edge in ddict.keys():
        if ddict[edge] == 0:
            critical_path.append(edge)

    return critical_path, vedict, vldict, edict, ldict, ddict


# 并查集，用于检测连通分量
class DSU:
    def __init__(self, lt):
        self.root = {}
        for i in lt:
            self.root[i] = i

    def find(self, k):
        if self.root[k] == k:
            return k
        self.root[k] = self.find(self.root[k])
        return self.root[k]

    def union(self, a, b):
        x = self.find(a)
        y = self.find(b)
        if x != y:
            self.root[y] = x
        return


def CheckConnectivity(_graph: Graph):
    visited = {}
    tmp_graph = copy.deepcopy(_graph)
    # 并查集初始化
    lt = list(tmp_graph.get_vertices())
    dsu = DSU(lt)
    for i in lt:
        visited[i] = False
    visited[lt[0]] = True
    for node in tmp_graph.adj_list.keys():
        for edge in tmp_graph.adj_list[node]:
            if visited[edge.start_vertex] is True and visited[edge.end_vertex] is True:
                dsu.union(edge.start_vertex, edge.end_vertex)
                continue
            if visited[edge.start_vertex] is True and visited[edge.end_vertex] is False:
                dsu.root[edge.end_vertex] = dsu.find(edge.start_vertex)
                visited[edge.end_vertex] = True
                continue
            if visited[edge.end_vertex] is True and visited[edge.start_vertex] is False:
                dsu.root[edge.start_vertex] = dsu.find(edge.end_vertex)
                visited[edge.start_vertex] = True
                continue
            if visited[edge.end_vertex] is False and visited[edge.start_vertex] is False:
                dsu.union(edge.start_vertex, edge.end_vertex)
                visited[edge.end_vertex] = True
                visited[edge.start_vertex] = True
                continue
    # 合并并查集，只保留一个根节点
    for node in lt:
        dsu.root[node] = dsu.find(node)
    roots = set(dsu.root.values())
    if len(roots) == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    graph = Graph()
    graph.add_vertex("v1")
    graph.add_vertex("v2")
    graph.add_vertex("v3")
    graph.add_vertex("v4")
    graph.add_vertex("v5")
    graph.add_vertex("v6")
    graph.add_vertex("v7")
    graph.add_vertex("v8")
    graph.add_vertex("v9")

    graph.add_edge("v1", "v2", 6)
    graph.add_edge("v1", "v3", 4)
    graph.add_edge("v1", "v4", 5)
    graph.add_edge("v2", "v5", 1)
    graph.add_edge("v3", "v5", 1)
    graph.add_edge("v4", "v6", 2)
    graph.add_edge("v5", "v7", 9)
    graph.add_edge("v5", "v8", 7)
    graph.add_edge("v6", "v8", 4)
    graph.add_edge("v7", "v9", 2)
    graph.add_edge("v8", "v9", 4)

    graph.remove_vertex("v1")
    CheckConnectivity(graph)
