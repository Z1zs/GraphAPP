from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QFrame, QHBoxLayout, QLayout
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFontMetrics
from graph import Graph

WDHeight = 50
WDWidth = 70
LBWidth = 70


# 空指针域的图形
class RectWithUp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WDWidth, WDHeight)

    def paintEvent(self, e):
        painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor('white'))
        brush.setStyle(Qt.SolidPattern)
        # 背景
        width = painter.device().width()
        height = painter.device().height()
        painter.setBackgroundMode(Qt.TransparentMode)
        # 代表指针域的矩形
        pen = QPen()
        pen.setColor(QColor('black'))
        pen.setWidth(2)
        sub_rect = QRectF(0, 0, width * 0.6, height)
        painter.setPen(pen)
        painter.drawRect(sub_rect)
        # 代表空值的上升箭头
        point1 = QPointF(width * 0.1, height * 0.65)
        point2 = QPointF(width * 0.5, height * 0.65)
        point3 = QPointF(width * 0.3, height * 0.35)
        line1 = QLineF(point1, point3)
        line2 = QLineF(point2, point3)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.drawLine(line1)
        painter.drawLine(line2)

        painter.end()


# 带箭头的指针域
class RectWithArrow(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(WDWidth, WDHeight)

    def paintEvent(self, e):
        # 绘画工具
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('white'))
        brush.setStyle(Qt.SolidPattern)

        # 背景
        width = painter.device().width()
        height = painter.device().height()
        painter.setBackgroundMode(Qt.TransparentMode)

        # 代表指针域的矩形
        pen = QPen()
        pen.setColor(QColor('black'))
        pen.setWidth(2)
        sub_rect = QRectF(0, 0, width * 0.6, height)
        painter.setPen(pen)
        painter.drawRect(sub_rect)

        # 箭头的线条
        start_point = QPointF(width * 0.3, height * 0.5)
        end_point = QPointF(width * 0.95, height * 0.5)
        line = QLineF(start_point, end_point)
        painter.drawLine(line)

        # 箭头的三角
        point1 = QPointF(width * 0.95, height * 0.45)
        point2 = QPointF(width * 0.95, height * 0.55)
        point3 = QPointF(width, height * 0.5)
        # #填充
        pen.setJoinStyle(Qt.MiterJoin)
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawPolygon(point1, point2, point3)

        painter.end()


# 顶点组件
class VertexListItem(QWidget):
    def __init__(self, vertex, in_degree, out_degree, outif):
        super().__init__()
        # 整体布局
        layout = QHBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        # 顶点名称
        self.name_label = QLabel(vertex.name)
        # #边框与尺寸
        self.name_label.setFrameStyle(QFrame.Box)
        self.name_label.setFixedSize(LBWidth, WDHeight)
        # #字体显示
        metrics = QFontMetrics(self.name_label.font())
        new_name = metrics.elidedText(vertex.name, Qt.ElideRight, self.name_label.width())
        self.name_label.setText(new_name)
        layout.addWidget(self.name_label)

        # 顶点入度
        self.indegree_label = QLabel(str(in_degree))
        self.indegree_label.setWordWrap(True)
        self.indegree_label.setFrameStyle(QFrame.Box)
        self.indegree_label.setFixedSize(int(LBWidth / 2), WDHeight)
        layout.addWidget(self.indegree_label)

        # 顶点出度
        self.outdegree_label = QLabel(str(out_degree))
        self.outdegree_label.setWordWrap(True)
        self.outdegree_label.setFrameStyle(QFrame.Box)
        self.outdegree_label.setFixedSize(int(LBWidth / 2), WDHeight)
        layout.addWidget(self.outdegree_label)

        # 顶点指针
        if outif is True:
            self.pointer_label = RectWithArrow()
        else:
            self.pointer_label = RectWithUp()
        layout.addWidget(self.pointer_label)
        layout.setSpacing(0)
        self.setLayout(layout)


# 边结点组件
class EdgeListItem(QWidget):
    def __init__(self, edge, endif):
        super().__init__()
        self.edge = edge
        self.endif = endif
        # 整体布局
        layout = QHBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)

        # end_vertex_label
        self.end_vertex_label = QLabel(self.edge.end_vertex.name)
        # #边框和尺寸
        self.end_vertex_label.setFrameStyle(QFrame.Box)
        self.end_vertex_label.setFixedSize(LBWidth, WDHeight)
        # #字体显示
        metrics = QFontMetrics(self.end_vertex_label.font())
        new_name = metrics.elidedText(self.edge.end_vertex.name, Qt.ElideRight, self.end_vertex_label.width())
        self.end_vertex_label.setText(new_name)
        layout.addWidget(self.end_vertex_label)

        # 权重标签
        self.weight_label = QLabel(str(self.edge.weight))
        self.weight_label.setWordWrap(True)
        self.weight_label.setFrameStyle(QFrame.Box)
        self.weight_label.setFixedSize(LBWidth, WDHeight)
        layout.addWidget(self.weight_label)

        # 指针
        if endif is True:
            self.pointer_label = RectWithArrow()
        else:
            self.pointer_label = RectWithUp()
        layout.addWidget(self.pointer_label)
        layout.setSpacing(0)
        self.setLayout(layout)


# 邻接链表组件
class AdjointListItem(QWidget):
    def __init__(self, _graph):
        super().__init__()
        self.graph = _graph
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setSizeConstraint(QGridLayout.SetFixedSize)
        self.setLayout(self.layout)
        self.update_ui()

    def update_ui(self):
        # 清空当前布局
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget)
            widget.setParent(None)

        row = 0
        for vertex in self.graph.adj_list.keys():
            vertex_item = VertexListItem(vertex, self.graph.in_degree_dict[vertex], len(self.graph.adj_list[vertex]),
                                         len(self.graph.adj_list[vertex]) > 0)
            self.layout.addWidget(vertex_item, row, 0)

            col = 1
            for edge in self.graph.adj_list[vertex]:
                edge_item = EdgeListItem(edge, col != len(self.graph.adj_list[vertex]))
                self.layout.addWidget(edge_item, row, col)
                col += 1
            row += 1

        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)

    def set_graph(self, new_graph):
        self.graph = new_graph
        self.update_ui()




app = QApplication([])
graph = Graph()
graph.add_vertex("v1")
graph.add_vertex("v2")
graph.add_vertex("v3")
graph.add_edge("v1", "v2", 2)
graph.add_edge("v2", "v1", 1)
graph.add_edge("v2", "v3", 1)
graph.add_vertex("v4")
v = AdjointListItem(graph)
graph.add_vertex("v5")
v.set_graph(graph)
v.graph.display()
v.show()
app.exec_()
