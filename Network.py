import math
import sys
import numpy as np
from graph import Graph, Vertex, Edge
from typing import Dict
from PyQt5.QtCore import (QEasingCurve, QLineF,
                          QParallelAnimationGroup, QPointF,
                          QPropertyAnimation, QRectF, Qt)
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
from PyQt5.QtWidgets import (QApplication, QGraphicsItem,
                             QGraphicsObject, QGraphicsScene, QGraphicsView,
                             QStyleOptionGraphicsItem, QVBoxLayout, QWidget)

from MyAlgorithm import CriticalPath, TopologicalSort


class NodeItem(QGraphicsObject):

    def __init__(self, name: str, data: Dict[str, int] = None, parent=None):
        super().__init__(parent)
        # 数据成员
        self._name = name
        self._edges = []
        # 图形参数
        self._color = QColor("green")
        self._radius = 30
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
        # UI参数
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

        # 悬停信息显示
        if data["showif"] == 1:
            self.vevalue = data["vevalue"]
            self.vlvalue = data["vlvalue"]
            self.setToolTip("Name: " + self._name + "\n"
                            + "VE: " + str(self.vevalue) + "\n"
                            + "VL: " + str(self.vlvalue))
        else:
            self.setToolTip("Name: " + self._name)

    def boundingRect(self) -> QRectF:
        # 返回矩形边框坐标
        return self._rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, _widget: QWidget = None):
        # paint方法实现组件绘制
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(QPen(self._color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(self._color))
        painter.drawEllipse(self.boundingRect())
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self._name)

    def add_edge(self, edge):
        # 添加边
        self._edges.append(edge)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        # 调整结点及邻边位置
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self._edges:
                edge.adjust()

        return super().itemChange(change, value)


class EdgeItem(QGraphicsObject):
    def __init__(self, source: NodeItem, dest: NodeItem, data: Dict[str, int] = None, color: QColor = QColor("green"),
                 parent: QGraphicsItem = None):
        # 数据成员
        super().__init__(parent)
        self._source = source
        self._dest = dest
        self._weight = data["weight"]

        # 悬停信息显示
        if data["showif"] == 1:
            self.setAcceptHoverEvents(True)
            self._evalue = data["evalue"]
            self._lvalue = data["lvalue"]
            self._dvalue = data["dvalue"]
            self.setToolTip("Direction: " + self._source._name + " -> " + self._dest._name + "\n"
                            + "Weight: " + str(self._weight) + "\n"
                            + "E: " + str(self._evalue) + "  ||  "
                            + "L: " + str(self._lvalue) + "\n"
                            + "D(L-E): " + str(self._dvalue))
        else:
            self.setToolTip("weight: " + str(self._weight))

        # 绘图设置
        self._tickness = 2
        self._color = color
        self._arrow_size = 20
        self._line = QLineF()
        self.setZValue(-1)
        # 结点添加对应边
        self._source.add_edge(self)
        self._dest.add_edge(self)
        self.adjust()

    def boundingRect(self) -> QRectF:
        # 返回矩形边框坐标
        return (
            QRectF(self._line.p1(), self._line.p2())
            .normalized()
            .adjusted(
                -self._tickness - self._arrow_size,
                -self._tickness - self._arrow_size,
                self._tickness + self._arrow_size,
                self._tickness + self._arrow_size,
            )
        )

    def adjust(self):
        # 拖拽调整
        self.prepareGeometryChange()
        self._line = QLineF(
            self._source.pos() + self._source.boundingRect().center(),
            self._dest.pos() + self._dest.boundingRect().center(),
        )

    def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF):
        # 画箭头，允许倾斜
        painter.setBrush(QBrush(self._color))
        # 箭头所在线段
        line = QLineF(end, start)
        # 计算倾斜角度
        angle = math.atan2(-line.dy(), line.dx())
        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi / 3) * self._arrow_size,
        )
        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
        )
        # 箭头三角部分
        arrow_head = QPolygonF()
        arrow_head.clear()
        arrow_head.append(line.p1())
        arrow_head.append(arrow_p1)
        arrow_head.append(arrow_p2)
        # 箭身
        painter.drawLine(line)
        painter.drawPolygon(arrow_head)

    def _arrow_target(self) -> QPointF:
        # 计算箭头坐标，考虑终点node尺寸
        target = self._line.p1()
        center = self._line.p2()
        radius = self._dest._radius
        vector = target - center
        length = math.sqrt(vector.x() ** 2 + vector.y() ** 2)
        if length == 0:
            return target
        normal = vector / length
        target = QPointF(center.x() + (normal.x() * radius), center.y() + (normal.y() * radius))

        return target

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, _widget=None):
        # 绘图函数

        if self._source and self._dest:
            painter.setRenderHints(QPainter.Antialiasing)
            # 权重
            painter.setPen(QPen(QColor(self._color), self._tickness / 2))
            painter.drawText(self.boundingRect(), Qt.AlignCenter, str(self._weight))
            # 箭头
            painter.setPen(QPen(QColor(self._color), self._tickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self._line)
            self._draw_arrow(painter, self._line.p1(), self._arrow_target())


class GraphView(QGraphicsView):
    def __init__(self, _graph: Graph):
        # 数据成员及画板
        super().__init__()
        self._graph = _graph
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # 图形参数
        self._graph_xscale = 10
        self._graph_yscale = 20

        # 从node/edge到item的map
        self._nodes_map = {}
        self.edge_map = {}
        # 从node/edge到对应动画，topo排序用
        self.hidden_animation_map = {}
        # 载入组件
        self._load_graph()

    def topo_layout(self):
        (is_topo, tplist) = TopologicalSort(self._graph)
        # 非拓扑序列补齐
        if is_topo is False:
            for nd in self._graph.get_vertices():
                if nd not in tplist:
                    tplist.append(nd)

        # 返回坐标值
        pos_dict = {}
        for i in range(len(tplist)):
            x = (i + 1) * 10 + np.random.randn()
            y = np.random.randn() * 10
            pos_dict[tplist[i]] = [x, y]
        return pos_dict

    def add_node(self, node: Vertex):
        # 创建实例
        data = {"showif": 0}
        item = NodeItem(node.name, data)
        self.scene().addItem(item)
        self._nodes_map[node] = item
        # 调整坐标
        x = (len(self._graph.get_vertices()) + 1) * 10 + np.random.randn()
        y = np.random.randn() * 10
        x *= self._graph_xscale
        y *= self._graph_yscale
        item = self._nodes_map[node]
        # 动画显示
        self.add_animation = QPropertyAnimation(item, b"pos")
        self.add_animation.setDuration(1000)
        self.add_animation.setEndValue(QPointF(x, y))
        self.add_animation.setEasingCurve(QEasingCurve.OutExpo)
        self.add_animation.start()

    def remove_node(self, node: Vertex):
        # 不推荐使用，代价较高
        # 删除结点
        if node in self._nodes_map:
            item = self._nodes_map[node]
            self._nodes_map.pop(node)
            self.scene().removeItem(item)
        # 删除边
        edge_del_list = []
        for edge in self.edge_map.keys():
            if edge.end_vertex == node or edge.start_vertex == node:
                item = self.edge_map[edge]
                edge_del_list.append(edge)
                self.scene().removeItem(item)
        for edge in edge_del_list:
            self.edge_map.pop(edge)

    def remove_edge(self, edge: Edge):
        # 删除边
        if edge in self.edge_map:
            item = self.edge_map[edge]
            self.edge_map.pop(edge)
            self.scene().removeItem(item)

    def add_edge(self, edge: Edge):
        # 添加边
        source = self._nodes_map[edge.start_vertex]
        dest = self._nodes_map[edge.end_vertex]

        data = {"weight": edge.weight, "showif": 0}
        edge_item = EdgeItem(source, dest, data)
        self.edge_map[edge] = edge_item
        self.scene().addItem(edge_item)

    def set_layout(self):
        # 计算各节点坐标
        self.positions = self.topo_layout()
        # 动画调整位置
        self.locate_animations = QParallelAnimationGroup()
        for node, pos in self.positions.items():
            x, y = pos
            x *= self._graph_xscale
            y *= self._graph_yscale
            item = self._nodes_map[node]

            animation = QPropertyAnimation(item, b"pos")
            animation.setDuration(1000)
            animation.setEndValue(QPointF(x, y))
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.locate_animations.addAnimation(animation)

        self.locate_animations.start()

    def _load_graph(self):
        # 初始化
        self.scene().clear()
        self._nodes_map.clear()

        # 添加节点
        for node in self._graph.adj_list.keys():
            data = {"showif": 0}
            item = NodeItem(node.name, data)
            self.scene().addItem(item)
            self._nodes_map[node] = item

        for node in self._graph.adj_list.keys():
            # 添加边
            for edge in self._graph.adj_list[node]:
                source = self._nodes_map[edge.start_vertex]
                dest = self._nodes_map[edge.end_vertex]

                data = {"weight": edge.weight, "showif": 0}
                edge_item = EdgeItem(source, dest, data)
                self.edge_map[edge] = edge_item
                self.scene().addItem(edge_item)
        self.set_layout()

    def hidden_node_animation(self, node):
        hidden_anime = QParallelAnimationGroup()
        # 节点消失动画
        animation = QPropertyAnimation(self._nodes_map[node], b"opacity")
        animation.setDuration(1000)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.OutExpo)
        hidden_anime.addAnimation(animation)

        # 出边消失动画
        for edge in self._graph.adj_list[node]:
            animation = QPropertyAnimation(self.edge_map[edge], b"opacity")
            animation.setDuration(1000)
            animation.setStartValue(1)
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            hidden_anime.addAnimation(animation)
        self.hidden_animation_map[node] = hidden_anime
        return self.hidden_animation_map[node]

    def recover_all_animation(self):
        self.recover_animation = QParallelAnimationGroup()
        for node in self._nodes_map.keys():
            # 各节点重现动画
            animation = QPropertyAnimation(self._nodes_map[node], b"opacity")
            animation.setDuration(1000)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.recover_animation.addAnimation(animation)
        for edge in self.edge_map.keys():
            # 各边重现动画
            animation = QPropertyAnimation(self.edge_map[edge], b"opacity")
            animation.setDuration(1000)
            animation.setStartValue(0)
            animation.setEndValue(1)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.recover_animation.addAnimation(animation)
        return self.recover_animation

    def _load_critical_path(self):
        # 初始化
        self.scene().clear()
        self._nodes_map.clear()
        self.cpath, self.vedict, self.vldict, self.edict, self.ldict, self.ddict = CriticalPath(self._graph)
        # 添加顶点
        for node in self._graph.adj_list.keys():
            data = {"showif": 0, "vevalue": self.vedict[node], "vlvalue": self.vldict[node]}
            item = NodeItem(node.name, data)
            self.scene().addItem(item)
            self._nodes_map[node] = item
        for node in self._graph.adj_list.keys():
            # 添加边
            for edge in self._graph.adj_list[node]:
                source = self._nodes_map[edge.start_vertex]
                dest = self._nodes_map[edge.end_vertex]

                data = {"showif": 1, "weight": edge.weight, "evalue": self.edict[edge], "lvalue": self.ldict[edge],
                        "dvalue": self.ddict[edge]}
                # 标注关键路径，用cyan区分颜色
                if edge in self.cpath:
                    item = EdgeItem(source, dest, data, QColor("cyan"))
                else:
                    item = EdgeItem(source, dest, data)
                self.scene().addItem(item)
                self.edge_map[edge] = item
        self.set_layout()


class MainWindow(QWidget):
    def __init__(self, _graph):
        super().__init__()

        self.graph = _graph
        self.view = GraphView(self.graph)
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a networkx graph
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
    widget = MainWindow(graph)
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())
