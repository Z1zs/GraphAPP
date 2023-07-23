from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QFrame, QHBoxLayout, QLayout, QGraphicsItem, \
    QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFontMetrics
from graph import Graph, Vertex


class VertexItem(QGraphicsItem):
    def __init__(self, vertex, x, y):
        super().__init__()
        self.vertex = vertex
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(x, y)

    def boundingRect(self):
        return self.rect()

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.blue))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(Qt.black, 1))
        painter.drawText(self.rect(), Qt.AlignCenter, self.vertex.name)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            x = value.x()
            y = value.y()
            self.vertex_pos_changed.emit(self, x, y)
        return super().itemChange(change, value)


class GraphItem(QGraphicsView):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.vertex_items = {}  # 用于保存顶点项和位置的字典
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.initUI()

    def initUI(self):
        for vertex in self.graph.get_vertices():
            vertex_item = VertexItem(vertex, 0, 0)  # 初始化位置为(0, 0)
            self.vertex_items[vertex] = vertex_item  # 将顶点项和位置保存到字典中
            self.scene.addItem(vertex_item)

            for neighbor in self.graph.get_neighbors(vertex):
                edge = QGraphicsItem()
                self.scene.addItem(edge)

        self.update_positions()  # 更新顶点的位置

    def update_positions(self):
        # 更新顶点的位置，使得顶点项在图形界面中呈现拓扑结构
        for vertex, vertex_item in self.vertex_items.items():
            neighbors = self.graph.get_neighbors(vertex)
            if not neighbors:
                continue

            x_sum = 0
            y_sum = 0
            for neighbor in neighbors:
                x_sum += self.vertex_items[neighbor].x()
                y_sum += self.vertex_items[neighbor].y()

            x_avg = x_sum / len(neighbors)
            y_avg = y_sum / len(neighbors)

            vertex_item.setPos(x_avg, y_avg)


if __name__ == '__main__':
    app = QApplication([])
    graph = Graph()

    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("C")

    graph.add_vertex(v1)
    graph.add_vertex(v2)
    graph.add_vertex(v3)

    graph.add_edge(v1, v2, 1)
    graph.add_edge(v2, v3, 2)

    window = GraphItem(graph)
    window.setWindowTitle("Graph Visualization")
    window.setGeometry(100, 100, 800, 600)
    window.show()

    app.exec_()