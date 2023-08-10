from PyQt5.QtCore import (QEasingCurve, QLineF,
                          QParallelAnimationGroup, QPointF,
                          QPropertyAnimation, QRectF, Qt)
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF
from PyQt5.QtWidgets import (QApplication, QGraphicsItem,
                             QGraphicsObject, QGraphicsScene, QGraphicsView,
                             QStyleOptionGraphicsItem, QVBoxLayout, QWidget)
from Graph import Graph, Vertex, Edge
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
        # 图形参数
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
        # 缓存(没什么用)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self) -> QRectF:
        # 返回边框坐标
        return self._rect

    def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF):
        # 绘制箭头
        painter.setBrush(QBrush(self._color))

        line = QLineF(end, start)
        # 计算角度
        angle = math.atan2(-line.dy(), line.dx())
        arrow_p1 = line.p1() + QPointF(
            math.sin(angle + math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi / 3) * self._arrow_size,
        )
        arrow_p2 = line.p1() + QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self._arrow_size,
            math.cos(angle + math.pi - math.pi / 3) * self._arrow_size,
        )
        # 三角形
        arrow_head = QPolygonF()
        arrow_head.clear()
        arrow_head.append(line.p1())
        arrow_head.append(arrow_p1)
        arrow_head.append(arrow_p2)
        # 箭身
        painter.drawLine(line)
        painter.drawPolygon(arrow_head)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, _widget: QWidget = None):
        # 绘制组件
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(self._color).darker(), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin, ))
        # 名称
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect1)
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self._sub_rect1, Qt.AlignCenter, self._name)
        # 补充信息
        painter.setPen(QPen(self._color.darker()))
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect2)
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self._sub_rect2, Qt.AlignCenter, str(self._in_degree))
        # 指针域
        painter.setPen(QPen(self._color.darker()))
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawRect(self._sub_rect3)
        # 指针箭头
        if self._outflag is True:
            painter.drawLine(self._line)
            self._draw_arrow(painter, self._line.p1(), self._line.p2())

    # 自定义组件性质degree，便于动画实现修改
    def _mydegree(self):
        return self._in_degree

    def setmydegree(self, new_degree):
        self._in_degree = new_degree
        self.update()

    mydegree = pyqtProperty(int, _mydegree, setmydegree)


# 邻接链表组件
class AdjiontListView(QGraphicsView):
    def __init__(self, _graph: Graph):
        # 数据成员
        super().__init__()
        self._graph = _graph
        self.show_map = {}
        # 图形参数
        self._xscale = 200
        self._yscale = self._xscale / 10 * 2
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # node/edge到对应item的map
        self._nodes_map = {}
        self.edge_map = {}
        # 初始化图形界面
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
        # 删除结点及对应出边
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

    # 调用之后必须执行，因为各ElementItem已经复原
    def recover_all_animation(self):
        # 还原所有组件的初始值
        self._load_graph()
        self.set_layout()

    def _load_graph(self):
        # 初始化,topo_graph是私有成员,深拷贝(因为需要修改其他节点的入度出度等，不如直接调用Graph写好的remove方法
        self.scene().clear()
        self._nodes_map.clear()
        self._topo_graph = copy.deepcopy(self._graph)

        for node in self._graph.adj_list.keys():
            # 遍历顶点，得到相应的悬浮信息
            outif = (len(self._graph.adj_list[node]) > 0)
            info = "Name: " + node.name + "\n" + "Out Degree: " + str(len(
                self._graph.adj_list[node])) + '\n' + "In Degree: " + str(self._graph.in_degree_dict[node])
            item = NodeElement(node.name, self._graph.in_degree_dict[node], outif, color=QColor("green").darker(),
                               hover_info=info, total_len=self._xscale)
            # 更新map和scene
            self.scene().addItem(item)
            self._nodes_map[node] = item

            for i in range(len(self._graph.adj_list[node])):
                # 添加出边，得到相应的悬浮信息
                edge = self._graph.adj_list[node][i]
                eoutif = (i != len(self._graph.adj_list[node]) - 1)
                einfo = ("End Vertex: " + edge.end_vertex.name + "\n" + "Start Vertex: " + edge.start_vertex.name + '\n'
                         + "Weight: " + str(edge.weight))
                eitem = NodeElement(edge.end_vertex.name, edge.weight, eoutif, hover_info=einfo, total_len=self._xscale)
                # 更新map和scene
                self.edge_map[edge] = eitem
                self.scene().addItem(eitem)

    def set_layout(self):
        # 调整布局
        self.locate_animations = QParallelAnimationGroup()
        row = 0
        for node in self._nodes_map.keys():
            # 计算顶点位置
            col = 0
            x = col * self._xscale
            y = row * self._yscale
            item = self._nodes_map[node]
            # 位置动画
            animation = QPropertyAnimation(item, b"pos")
            animation.setDuration(1000)
            animation.setEndValue(QPointF(x, y))
            animation.setEasingCurve(QEasingCurve.OutExpo)
            self.locate_animations.addAnimation(animation)
            for edge in self._graph.adj_list[node]:
                # 计算出边位置
                col += 1
                x = col * self._xscale
                y = row * self._yscale
                item = self.edge_map[edge]
                # 添加对应位置动画
                animation = QPropertyAnimation(item, b"pos")
                animation.setDuration(1000)
                animation.setEndValue(QPointF(x, y))
                animation.setEasingCurve(QEasingCurve.OutExpo)
                self.locate_animations.addAnimation(animation)
            row += 1
        # 调整布局动画
        self.locate_animations.start()
