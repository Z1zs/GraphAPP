from Network import NodeItem, EdgeItem
import sys
from Graph import Graph, Vertex
from PyQt5.QtCore import (QEasingCurve,
                          QParallelAnimationGroup, QPointF,
                          QPropertyAnimation)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem,
                             QGraphicsScene, QGraphicsView,
                             QVBoxLayout, QWidget)

from MyAlgorithm import TopologicalSort, SplitPath


class SortColumn(QGraphicsView):
    def __init__(self, node_list):
        # 数据成员
        super().__init__()
        self.node_list = node_list
        self.topo_list = []
        self._nodes_map = {}
        self.add_animation_map = {}
        # 图形参数
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self._radius = 30
        self.space_size = 10
        # 加载成员
        if len(node_list) > 0:
            self.load_node()

    def load_node(self):
        self._scene.clear()
        self._nodes_map.clear()

        self.locate_animation = QParallelAnimationGroup()
        for i in range(len(self.node_list)):
            node = self.node_list[i]
            data = {"showif": 0}
            item = NodeItem(node.name, data)
            item.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.scene().addItem(item)
            self._nodes_map[node] = item
            # 位置动画
            x = i * (self._radius * 2 + self.space_size)
            y = 0
            anime = QPropertyAnimation(self._nodes_map[node], b"pos")
            anime.setDuration(1000)
            anime.setEndValue(QPointF(x, y))
            anime.setEasingCurve(QEasingCurve.OutExpo)
            self.locate_animation.addAnimation(anime)
        self.locate_animation.start()

    def myclear(self):
        self.topo_list.clear()
        self._scene.clear()
        self._nodes_map.clear()

    def add_node_animation(self, node: Vertex):
        self.topo_list.append(node)
        data = {"showif": 0}
        item = NodeItem(node.name, data)
        item.setProperty("opacity", 0)
        self.scene().addItem(item)
        self._nodes_map[node] = item

        add_anime = QParallelAnimationGroup()
        # 位置动画
        x = (len(self.topo_list) - 1) * (self._radius * 2 + self.space_size)
        y = 0
        add_anime1 = QPropertyAnimation(self._nodes_map[node], b"pos")
        add_anime1.setDuration(1000)
        add_anime1.setEndValue(QPointF(0, 0))
        add_anime1.setEndValue(QPointF(x, y))
        add_anime1.setEasingCurve(QEasingCurve.OutExpo)
        add_anime.addAnimation(add_anime1)
        # 复现动画（组件初始时不可见）
        add_anime2 = QPropertyAnimation(self._nodes_map[node], b"opacity")
        add_anime2.setDuration(1000)
        add_anime2.setEndValue(1)
        add_anime2.setEasingCurve(QEasingCurve.OutExpo)
        add_anime.addAnimation(add_anime2)

        self.add_animation_map[node] = add_anime
        return self.add_animation_map[node]

    def myupdate(self, new_node_list):
        self.myclear()
        self.node_list = new_node_list
        self.topo_list = []
        self._nodes_map = {}
        self.add_animation_map = {}
        # 加载成员
        if len(new_node_list) > 0:
            self.load_node()


class PathColumn(QGraphicsView):
    def __init__(self, edge_list,dist_dict):
        # 数据成员
        super().__init__()
        self.path = SplitPath(edge_list,dist_dict)
        self._nodes_map = {}
        self._edges_map = {}
        # 图形参数
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self._radius = 30
        self.space_size = 20
        # 加载路径
        if len(edge_list) > 0:
            self.load_path()

    def load_path(self):
        self.locate_animation = QParallelAnimationGroup()
        for edge in self.path:
            # 添加顶点
            node = Vertex(edge.start_vertex)
            if node not in self._nodes_map:
                data = {"showif": 0}
                item = NodeItem(node.name, data)
                item.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.scene().addItem(item)
                self._nodes_map[node] = item
            # 位置动画
            x = (len(self._nodes_map.keys()) - 1) * (self._radius * 3 + self.space_size)
            y = 0
            anime = QPropertyAnimation(self._nodes_map[node], b"pos")
            anime.setDuration(1000)
            anime.setEndValue(QPointF(x, y))
            anime.setEasingCurve(QEasingCurve.OutExpo)
            self.locate_animation.addAnimation(anime)
        # 终点特殊处理
        node = Vertex(self.path[-1].end_vertex)
        data = {"showif": 0}
        item = NodeItem(node.name, data)
        item.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.scene().addItem(item)
        self._nodes_map[node] = item
        # 位置动画
        x = (len(self._nodes_map.keys()) - 1) * (self._radius * 3 + self.space_size)
        y = 0
        anime = QPropertyAnimation(self._nodes_map[node], b"pos")
        anime.setDuration(1000)
        anime.setEndValue(QPointF(x, y))
        anime.setEasingCurve(QEasingCurve.OutExpo)
        self.locate_animation.addAnimation(anime)
        for edge in self.path:
            source = self._nodes_map[edge.start_vertex]
            dest = self._nodes_map[edge.end_vertex]

            data = {"weight": edge.weight, "showif": 0}
            edge_item = EdgeItem(source, dest, data)
            self._edges_map[edge] = edge_item
            self.scene().addItem(edge_item)
        self.locate_animation.start()

    def myclear(self):
        self._scene.clear()
        self._edges_map.clear()
        self._nodes_map.clear()

    def myupdate(self, new_edge_list,dist_dict):
        self.myclear()
        self.path = SplitPath(new_edge_list,dist_dict)
        self._nodes_map = {}
        self._edges_map = {}
        # 加载路径
        if len(new_edge_list) > 0:
            self.load_path()

