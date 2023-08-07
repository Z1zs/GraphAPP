from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QFrame, QHBoxLayout, QLayout, QPushButton
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFontMetrics
from PyQt5.QtCore import (QEasingCurve, QLineF, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPointF,
                          QPropertyAnimation, QRectF, Qt)
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
from PyQt5.QtWidgets import (QApplication, QGraphicsItem,
                             QGraphicsObject, QGraphicsScene, QGraphicsView,
                             QStyleOptionGraphicsItem, QVBoxLayout, QWidget)
from graph import Graph, Vertex, Edge
from MyAlgorithm import CriticalPath, TopologicalSort
import math
import sys
import copy


# 空指针域的图形
class NodeElement(QGraphicsObject):
    def __init__(self, name: str, in_degree: str, outif: bool, color: str = "green", hover_info: str = None,
                 total_len: int = 100, parent=None):
        # 数据成员
        super().__init__(parent)
        self._name = name
        self._in_degree = in_degree
        self._outflag = outif
        self._color = QColor(color)
        self._hover_info = hover_info
        self.setToolTip(self._hover_info)
        # 图形成员
        self._len = total_len / 10
        self._rect = QRectF(0, 0, self._len * 10, self._len * 2)

        self._sub_rect1 = QRectF(0, 0, self._len * 3, self._len * 2)
        self._sub_rect2 = QRectF(self._len * 3, 0, self._len * 3, self._len * 2)
        self._sub_rect3 = QRectF(self._len * 6, 0, self._len * 2.4, self._len * 2)
        self._arrow_size = self._len / 2
        self._line = QLineF(
            QPointF(self._len * 7.8, self._len),
            QPointF(self._len * 10, self._len),
        )

        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self) -> QRectF:
        """Override from QGraphicsItem

        Returns:
            QRect: Return node bounding rect
        """
        return self._rect

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
                3,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )

        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect1)
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self._sub_rect1, Qt.AlignCenter, self._name)

        painter.setPen(QPen(self._color.darker()))
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect2)
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self._sub_rect2, Qt.AlignCenter, str(self._in_degree))

        painter.setPen(QPen(self._color.darker()))
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect3)

        if self._outflag is True:
            painter.drawLine(self._line)
            self._draw_arrow(painter, self._line.p1(), self._line.p2())

    def _myname(self):
        return self._name

    def setmyname(self, new_name):
        self._name = new_name
        self.update()

    def _mydegree(self):
        return self._in_degree

    def setmydegree(self, new_degree):
        self._in_degree = new_degree
        self.update()

    def _myout(self):
        return self._outflag

    def setmyout(self, new_flag):
        self._outflag = new_flag
        self.update()

    mydegree = pyqtProperty(int, _mydegree, setmydegree)
    myname = pyqtProperty(str, _myname, setmyname)
    myout = pyqtProperty(bool, _myout, setmyout)


# 邻接链表组件
class AdjiontListView(QGraphicsView):
    def __init__(self, graph: Graph):
        """GraphView constructor

        This widget can display a directed graph

        Args:
            graph (nx.DiGraph): a networkx directed graph
        """
        super().__init__()
        self._graph = graph
        self.show_map = {}
        # 图形界面
        self._xscale = 200
        self._yscale = self._xscale / 10 * 2
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # Map node/edge name to Node/Edge object {str=>Node}
        self._nodes_map = {}
        self.edge_map = {}

        self._load_graph()
        self.set_layout()

    def add_node(self, node: Vertex):
        # 一个一个检查然后重排太麻烦了，直接大洗牌
        self._load_graph()
        self.set_layout()

    def remove_node(self, node: Vertex):
        # 一个一个检查然后重排太麻烦了，直接大洗牌
        self._load_graph()
        self.set_layout()

    def add_edge(self, edge: Edge):
        # 一个一个检查然后改写太麻烦了，直接大洗牌
        self._load_graph()
        self.set_layout()

    def remove_edge(self, edge: Edge):
        # 一个一个检查然后改写太麻烦了，直接大洗牌
        self._load_graph()
        self.set_layout()

    # 只返回对应隐藏动画，但并不执行，不过一旦调用，返回的动画对象必须执行，因为topo_graph的值已经改变
    def hidden_node_animation(self, node):
        if node not in self._topo_graph.adj_list.keys():
            return False
        self._topo_graph.remove_vertex(node)
        self.hidden_anime = QParallelAnimationGroup()
        # 隐去结点
        animation = QPropertyAnimation(self._nodes_map[node], b"opacity")
        animation.setDuration(1000)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.OutExpo)
        self.hidden_anime.addAnimation(animation)
        # 隐去边
        print(self._graph.adj_list.keys())
        for edge in self._graph.adj_list[node]:
            animation = QPropertyAnimation(self.edge_map[edge], b"opacity")
            animation.setDuration(1000)
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.hidden_anime.addAnimation(animation)
        # 修改入度
        for other_node in self._topo_graph.adj_list.keys():
            animation = QPropertyAnimation(self._nodes_map[other_node], b"mydegree")
            animation.setDuration(1000)
            s = str(self._topo_graph.in_degree_dict[other_node])
            animation.setEndValue(s)
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.hidden_anime.addAnimation(animation)
        return self.hidden_anime

    # 调用之后必须执行，因为elementitem已经复原
    def recover_all_animation(self):
        self.recover_animation = QParallelAnimationGroup()
        for node in self._graph.adj_list.keys():
            if node not in self._topo_graph.adj_list.keys():
                # 可视化
                animation = QPropertyAnimation(self._nodes_map[node], b"opacity")
                animation.setDuration(1000)
                animation.setEndValue(1)
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.recover_animation.addAnimation(animation)
                # 对应入度
                animation = QPropertyAnimation(self._nodes_map[node], b"mydegree")
                animation.setDuration(1000)
                animation.setEndValue(str(self._graph.in_degree_dict[node]))
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.recover_animation.addAnimation(animation)
                for edge in self._graph.adj_list[node]:
                    # 可视化
                    animation = QPropertyAnimation(self.edge_map[edge], b"opacity")
                    animation.setDuration(1000)
                    animation.setEndValue(1)
                    animation.setEasingCurve(QEasingCurve.OutExpo)
                    self.recover_animation.addAnimation(animation)
            else:
                # 修改入度
                animation = QPropertyAnimation(self._nodes_map[node], b"mydegree")
                animation.setDuration(1000)
                animation.setEndValue(str(self._graph.in_degree_dict[node]))
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.recover_animation.addAnimation(animation)
        return self.recover_animation

    def _load_graph(self):

        self.scene().clear()
        self._nodes_map.clear()
        self._topo_graph = copy.deepcopy(graph)
        for node in self._graph.adj_list.keys():
            outif = (len(self._graph.adj_list[node]) > 0)
            info = "Name: " + node.name + "\n" + "Out Degree: " + str(len(
                self._graph.adj_list[node])) + '\n' + "In Degree: " + str(self._graph.in_degree_dict[node])
            item = NodeElement(node.name, self._graph.in_degree_dict[node], outif, color=QColor("green").darker(),
                               hover_info=info,
                               total_len=self._xscale)
            self.scene().addItem(item)
            self._nodes_map[node] = item
            # Add edges
            for i in range(len(self._graph.adj_list[node])):
                edge = self._graph.adj_list[node][i]
                eoutif = (i != len(self._graph.adj_list[node]) - 1)
                einfo = "End Vertex: " + edge.end_vertex.name + "\n" + "Start Vertex: " + edge.start_vertex.name + '\n' + "Weight: " + str(
                    edge.weight)
                eitem = NodeElement(edge.end_vertex.name, edge.weight, eoutif, hover_info=einfo, total_len=self._xscale)
                self.edge_map[edge] = eitem
                self.scene().addItem(eitem)

    def set_layout(self):
        # Change position of all nodes using an animation
        self.locate_animations = QParallelAnimationGroup()
        row = 0
        for node in self._nodes_map.keys():
            col = 0
            x = col * self._xscale
            y = row * self._yscale
            item = self._nodes_map[node]

            animation = QPropertyAnimation(item, b"pos")
            animation.setDuration(1000)
            animation.setEndValue(QPointF(x, y))
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.locate_animations.addAnimation(animation)
            for edge in self._graph.adj_list[node]:
                col += 1
                x = col * self._xscale
                y = row * self._yscale
                item = self.edge_map[edge]

                animation = QPropertyAnimation(item, b"pos")
                animation.setDuration(1000)
                animation.setEndValue(QPointF(x, y))
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.locate_animations.addAnimation(animation)
            row += 1

        self.locate_animations.start()


class MainWindow(QWidget):
    def __init__(self, graph):
        super().__init__()

        self.graph = graph
        self.view = AdjiontListView(self.graph)
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
