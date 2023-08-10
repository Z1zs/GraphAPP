class Vertex:
    def __init__(self, name):
        self.name = str(name)

    # 重载hash函数和eq函数用于键值比较
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == str(other)

    # 重载str函数
    def __str__(self):
        return str(self.name)

    # 重载repr
    def __repr__(self):
        return str(self.name)


class Edge:
    def __init__(self, start_vertex_name, end_vertex_name, weight):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.weight = weight

    # 重载str函数
    def __str__(self):
        return "（" + self.start_vertex.name + "," + self.end_vertex.name + ")"

    # 重载repr
    def __repr__(self):
        return "（" + self.start_vertex.name + "," + self.end_vertex.name + ")"

    def __hash__(self):
        return hash(self.start_vertex.name + "|" + self.end_vertex.name)

    def __eq__(self, other):
        return self.start_vertex.name == other.start_vertex.name and self.end_vertex.name == other.end_vertex.name


class Graph:
    # 初始化
    def __init__(self):
        self.adj_list = {}
        self.in_degree_dict = {}  # 保存各顶点入度

    # 添加独立顶点
    def add_vertex(self, vertex_name):
        vertex = Vertex(str(vertex_name))
        wronginfo = ""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.in_degree_dict[vertex] = 0
        else:
            wronginfo = "Error: Vertex " + vertex.name + " already exists."
            print("Error: Vertex %s already exists." % vertex.name)
            return False, wronginfo
        return True, wronginfo

    # 添加边
    def add_edge(self, start_vertex_name: str, end_vertex_name: str, weight: float):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        wronginfo = ""
        if weight <= 0:
            wronginfo = "Error: Weight must be positive!"
            print("Error: Weight must be positive!")
            return False, wronginfo
        if start_vertex in self.adj_list:
            if end_vertex not in self.adj_list:
                wronginfo = "Error: Can't find end_vertex " + end_vertex.name
                print("Error: Can't find end_vertex %s" % end_vertex.name)
                return False, wronginfo
            elif self.has_edge(start_vertex, end_vertex):
                wronginfo = "Error: Edge already exist!"
                print("Error: Edge already exist!")
                return False, wronginfo
            edge = Edge(start_vertex, end_vertex, weight)
            self.in_degree_dict[end_vertex] = self.in_degree_dict[end_vertex] + 1
            self.adj_list[start_vertex].append(edge)
        else:
            wronginfo = "Error: Can't find end_vertex " + start_vertex.name
            print("Error: Can't find end_vertex %s" % start_vertex.name)
            return False, wronginfo
        return True, wronginfo

    # 删除顶点
    def remove_vertex(self, vertex_name):
        vertex = Vertex(str(vertex_name))
        if vertex in self.adj_list:

            # 删除出边
            out_edge = self.adj_list[vertex]
            for og in out_edge:
                self.in_degree_dict[og.end_vertex.name] = self.in_degree_dict[og.end_vertex.name] - 1
            # 删除顶点
            del self.adj_list[vertex]
            del self.in_degree_dict[vertex]
            # 删除入边
            for adj_vertices in self.adj_list.values():
                adj_vertices[:] = [edge for edge in adj_vertices if edge.end_vertex.name != vertex.name]
        else:
            wronginfo = "Error: Can't find vertex " + vertex.name
            print("Error: Can't find vertex %s" % vertex.name)
            return False, wronginfo
        return True, ""

    # 删除边
    def remove_edge(self, start_vertex_name: str, end_vertex_name: str):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        wronginfo = ""
        if not self.has_edge(start_vertex_name, end_vertex_name):
            wronginfo = "Error: Can't find edge from " + start_vertex_name + " to " + end_vertex_name
            print(wronginfo)
            return False, wronginfo
        if start_vertex in self.adj_list:
            self.adj_list[start_vertex] = [edge for edge in self.adj_list[start_vertex]
                                           if edge.end_vertex.name != end_vertex.name]
        self.in_degree_dict[end_vertex] = self.in_degree_dict[end_vertex] - 1
        return True, wronginfo

    # 查找边
    def has_edge(self, start_vertex_name, end_vertex_name):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        if start_vertex in self.adj_list:
            # 遍历出边
            for edge in self.adj_list[start_vertex]:
                if edge.end_vertex.name == end_vertex.name:
                    return True
        return False

    # 获取邻接顶点
    def get_neighbors(self, vertex_name):
        vertex = Vertex(str(vertex_name))
        if vertex in self.adj_list:
            return [edge.end_vertex for edge in self.adj_list[vertex]]
        return []

    # 获取全部顶点
    def get_vertices(self):
        return list(self.adj_list.keys())

    # 获取顶点出度
    def get_out_degree(self, vertex_name):
        vertex = Vertex(str(vertex_name))
        if vertex not in self.adj_list:
            print("Error: Can't find vertex %s" % vertex.name)
            return False
        else:
            return len(self.adj_list[vertex])

    # 获取顶点入度
    def get_in_degree(self, vertex_name):
        vertex = Vertex(str(vertex_name))
        if vertex not in self.adj_list:
            print("Error: Can't find vertex %s" % vertex.name)
            return False
        else:
            return self.in_degree_dict[vertex]

    # 获取前驱节点
    def get_predecessor(self):
        predecessor_dict = {}
        for start_vertex in self.adj_list.keys():
            predecessor_dict[start_vertex] = []
        for start_vertex in self.adj_list.keys():
            for edge in self.adj_list[start_vertex]:
                # 遍历所有边结点
                if edge.end_vertex not in predecessor_dict:
                    predecessor_dict[edge.end_vertex].append(edge)
                else:
                    predecessor_dict[edge.end_vertex].append(edge)
        return predecessor_dict

    # 检查错误
    def check_vertex(self):
        adj_vertex = list(self.adj_list.keys())
        in_degree_vertex = list(self.in_degree_dict.keys())
        res1 = [k for k in adj_vertex if k not in in_degree_vertex]
        res2 = [k for k in in_degree_vertex if k not in adj_vertex]
        if len(res1) == 0 and len(res2) == 0:
            return True
        else:
            return False

    # 获取所有出度为0的点
    def get_dist(self):
        dist_list = []
        for node in self.in_degree_dict.keys():
            if len(self.adj_list[node]) == 0:
                dist_list.append(node)
        return dist_list

    # 打印各顶点与边信息，方便debug
    def display(self):
        for v in self.adj_list.keys():
            print(str(v) + "  :")
            print(self.adj_list[v])
        for key, value in self.in_degree_dict.items():
            print(str(key) + " : " + str(value) + ";")
