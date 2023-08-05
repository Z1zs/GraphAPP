import math
import sys
import numpy as np
from graph import Graph, Vertex
from typing import Dict
from PyQt5.QtCore import (QEasingCurve, QLineF, QSequentialAnimationGroup,
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
        self._name = name
        self._edges = []
        self._color = "#5AD469"
        self._radius = 30
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
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
        """Override from QGraphicsItem

        Returns:
            QRect: Return node bounding rect
        """
        return self._rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """Override from QGraphicsItem

        Draw node

        Args:
            painter (QPainter)
            option (QStyleOptionGraphicsItem)
        """
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(
            QPen(
                QColor(self._color).darker(),
                2,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawEllipse(self.boundingRect())
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self._name)

    def add_edge(self, edge):
        """Add an edge to this node

        Args:
            edge (EdgeItem)
        """
        self._edges.append(edge)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        """Override from QGraphicsItem

        Args:
            change (QGraphicsItem.GraphicsItemChange)
            value (Any)

        Returns:
            Any
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self._edges:
                edge.adjust()

        return super().itemChange(change, value)


class EdgeItem(QGraphicsObject):
    def __init__(self, source: NodeItem, dest: NodeItem, data: Dict[str, int] = None, color: QColor = QColor("green"),
                 parent: QGraphicsItem = None):
        """Edge constructor

        Args:
            source (NodeItem): source node
            dest (NodeItem): destination node
        """
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

        self._source.add_edge(self)
        self._dest.add_edge(self)

        self._line = QLineF()
        self.setZValue(-1)
        self.adjust()

    def boundingRect(self) -> QRectF:
        """Override from QGraphicsItem

        Returns:
            QRect: Return node bounding rect
        """
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
        """
        Update edge position from source and destination node.
        This method is called from Node::itemChange
        """
        self.prepareGeometryChange()
        self._line = QLineF(
            self._source.pos() + self._source.boundingRect().center(),
            self._dest.pos() + self._dest.boundingRect().center(),
        )

    def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF):
        """Draw arrow from start point to end point.

        Args:
            painter (QPainter)
            start (QPointF): start position
            end (QPointF): end position
        """
        painter.setBrush(QBrush(self._color))

        line = QLineF(end, start)

        angle = math.atan2(-line.dy(), line.dx())
        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi / 3) * self._arrow_size,
        )
        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
        )

        arrow_head = QPolygonF()
        arrow_head.clear()
        arrow_head.append(line.p1())
        arrow_head.append(arrow_p1)
        arrow_head.append(arrow_p2)
        painter.drawLine(line)
        painter.drawPolygon(arrow_head)

    def _arrow_target(self) -> QPointF:
        """Calculate the position of the arrow taking into account the size of the destination node

        Returns:
            QPointF
        """
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

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        """Override from QGraphicsItem

        Draw Edge. This method is called from Edge.adjust()

        Args:
            painter (QPainter)
            option (QStyleOptionGraphicsItem)
        """

        if self._source and self._dest:
            painter.setRenderHints(QPainter.Antialiasing)

            painter.setPen(
                QPen(
                    QColor(self._color),
                    self._tickness / 2
                )
            )
            painter.drawText(self.boundingRect(), Qt.AlignCenter, str(self._weight))

            painter.setPen(
                QPen(
                    QColor(self._color),
                    self._tickness,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self._line)
            self._draw_arrow(painter, self._line.p1(), self._arrow_target())
            self._arrow_target()


class GraphView(QGraphicsView):
    def __init__(self, graph: Graph, show_cpath=False, parent=None):
        """GraphView constructor

        This widget can display a directed graph

        Args:
            graph (nx.DiGraph): a networkx directed graph
        """
        super().__init__()
        self._graph = graph
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # Used to add space between nodes
        self._graph_xscale = 10
        self._graph_yscale = 20

        # Map node/edge name to Node/Edge object {str=>Node}
        self._nodes_map = {}
        self.edge_map = {}

        # map node to animation
        self.topo_anime_map = {}
        self.topo_animation = QSequentialAnimationGroup()

        if show_cpath is False:
            self._load_graph()
        else:
            self.cpath, self.vedict, self.vldict, self.edict, self.ldict, self.ddict = CriticalPath(self._graph)
            self._load_critical_path()
        self.load_topo_animation()
        self.set_layout()

    def spring_layout(self):
        isTopo, TPlist = TopologicalSort(self._graph)
        # 非拓扑序列补齐
        if isTopo is False:
            for nd in self._graph.get_vertices():
                if nd not in TPlist:
                    TPlist.append(nd)

        # 返回坐标值
        pos_dict = {}
        for i in range(len(TPlist)):
            x = (i + 1) * 10 + np.random.randn()
            y = np.random.randn() * 10
            pos_dict[TPlist[i]] = [x, y]
        return pos_dict

    def set_layout(self):
        # Compute node position from layout function
        positions = self.spring_layout()
        print(positions)
        # Change position of all nodes using an animation
        self.locate_animations = QParallelAnimationGroup()
        for node, pos in positions.items():
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

        self.scene().clear()
        self._nodes_map.clear()

        # Add nodes
        for node in self._graph.adj_list.keys():
            data = {"showif": 0}
            item = NodeItem(node.name, data)
            self.scene().addItem(item)
            self._nodes_map[node] = item

        for node in self._graph.adj_list.keys():
            # Add edges
            for edge in self._graph.adj_list[node]:
                source = self._nodes_map[edge.start_vertex]
                dest = self._nodes_map[edge.end_vertex]

                data = {"weight": edge.weight, "showif": 0}
                edge_item = EdgeItem(source, dest, data)
                self.edge_map[edge] = edge_item
                self.scene().addItem(edge_item)

    def load_topo_animation(self):
        for node in self._graph.adj_list.keys():
            panime = QParallelAnimationGroup()
            # 动画
            animation = QPropertyAnimation(self._nodes_map[node], b"visible")
            animation.setDuration(1000)
            animation.setStartValue(1)
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            panime.addAnimation(animation)

            # Add edges
            for edge in self._graph.adj_list[node]:
                animation = QPropertyAnimation(self.edge_map[edge], b"visible")
                animation.setDuration(1000)
                animation.setStartValue(1)
                animation.setEndValue(0)
                animation.setEasingCurve(QEasingCurve.OutExpo)
                panime.addAnimation(animation)
            self.topo_anime_map[node] = panime

    def run_topo_animation(self):
        istp, tplist = TopologicalSort(self._graph)
        if istp is False:
            return False
        for node in tplist:
            # print(node)
            # print(self.topo_anime_map.keys())
            self.topo_animation.addAnimation(self.topo_anime_map[node])
        self.topo_animation.start()

    def _load_critical_path(self):

        self.scene().clear()
        self._nodes_map.clear()

        # Add nodes
        for node in self._graph.adj_list.keys():
            data = {"showif": 0, "vevalue": self.vedict[node], "vlvalue": self.vldict[node]}
            item = NodeItem(node.name, data)
            self.scene().addItem(item)
            self._nodes_map[node] = item
        for node in self._graph.adj_list.keys():
            # Add edges
            for edge in self._graph.adj_list[node]:
                source = self._nodes_map[edge.start_vertex]
                dest = self._nodes_map[edge.end_vertex]

                data = {"showif": 1, "weight": edge.weight, "evalue": self.edict[edge], "lvalue": self.ldict[edge],
                        "dvalue": self.ddict[edge]}
                item = None
                if edge in self.cpath:
                    item = EdgeItem(source, dest, data, QColor("cyan"))
                else:
                    item = EdgeItem(source, dest, data)
                self.scene().addItem(item)
                self.edge_map[edge] = item


class MainWindow(QWidget):
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.view = GraphView(self.graph, True)
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
