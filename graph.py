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
        return hash(self.start_vertex.name + self.end_vertex.name)

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
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.in_degree_dict[vertex] = 0
        else:
            print("Error: Vertex %s already exists." % vertex.name)
            return False

    # 添加边
    def add_edge(self, start_vertex_name, end_vertex_name, weight):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        if weight <= 0:
            print("Error: Weight must be positive!")
            return False
        if start_vertex in self.adj_list:
            if end_vertex not in self.adj_list:
                print("Error: Can't find end_vertex %s" % end_vertex.name)
                return False
            edge = Edge(start_vertex, end_vertex, weight)
            self.in_degree_dict[end_vertex] = self.in_degree_dict[end_vertex] + 1
            self.adj_list[start_vertex].append(edge)

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
            print("Error: Can't find vertex %s" % vertex.name)
            return False

    # 删除边
    def remove_edge(self, start_vertex_name, end_vertex_name):
        start_vertex = Vertex(str(start_vertex_name))
        end_vertex = Vertex(str(end_vertex_name))
        if start_vertex in self.adj_list:
            self.adj_list[start_vertex] = [edge for edge in self.adj_list[start_vertex]
                                           if edge.end_vertex.name != end_vertex.name]
        self.in_degree_dict[end_vertex] = self.in_degree_dict[end_vertex] - 1

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

    # 重载str函数
    def display(self):
        for v in self.adj_list.keys():
            print(str(v) + "  :")
            print(self.adj_list[v])
        for key, value in self.in_degree_dict.items():
            print(str(key) + " : " + str(value) + ";")
