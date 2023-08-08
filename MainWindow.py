from Network import NodeItem, EdgeItem
import sys
from graph import Graph, Vertex,Edge
from PyQt5.QtCore import (QEasingCurve, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPointF,
                          QPropertyAnimation)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QToolBar, QAction, QStatusBar, QMainWindow,
                             QGraphicsScene, QGraphicsView,
                             QVBoxLayout, QWidget, QHBoxLayout)
from AdjointListVisualization import AdjiontListView
from ColumnItem import PathColumn, SortColumn
from Network import GraphView
from MyAlgorithm import TopologicalSort, SplitPath, CriticalPath


class MainWindow(QMainWindow):
    def __init__(self, _graph: Graph):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Awesome App")

        self._graph = _graph
        self.adjoint_widget = AdjiontListView(self._graph)
        self.graph_widget = GraphView(self._graph)
        self.show_critical_path_flag=False

        self.ifdag, self.sort_node_list = TopologicalSort(self._graph)
        self.path_list, _, _, _, _, _ = CriticalPath(self._graph)
        self.sort_column = SortColumn(self.sort_node_list)
        self.path_column = PathColumn(self.path_list)

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.sort_column, 1)
        self.left_layout.addWidget(self.path_column, 1)
        self.left_layout.addWidget(self.adjoint_widget, 5)

        self._layout = QHBoxLayout()
        self._layout.addLayout(self.left_layout, 1)
        self._layout.addWidget(self.graph_widget, 1)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self._layout)
        self.setCentralWidget(self.central_widget)
        self.setBaseSize(2000, 2000)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action1 = QAction("Topo", self)
        button_action1.setStatusTip("Topo Sort")
        button_action1.triggered.connect(self.topo_sort)
        toolbar.addAction(button_action1)

        button_action2 = QAction("Recover", self)
        button_action2.setStatusTip("Recover All")
        button_action2.triggered.connect(self.recover_all)
        toolbar.addAction(button_action2)

        button_action3 = QAction("Critical Path", self)
        button_action3.setStatusTip("Show Path")
        button_action3.triggered.connect(self.show_critical_path)
        toolbar.addAction(button_action3)

        button_action4 = QAction("Add Node", self)
        button_action4.setStatusTip("Add Node")
        button_action4.triggered.connect(self.add_node)
        toolbar.addAction(button_action4)

        button_action5 = QAction("Add Edge", self)
        button_action5.setStatusTip("Add Edge")
        button_action5.triggered.connect(self.add_edge)
        toolbar.addAction(button_action5)

        self.setStatusBar(QStatusBar(self))

    def add_node(self):
        node = Vertex("v100")
        if self._graph.add_vertex(node):
            self.graph_widget.add_node(node)
            self.adjoint_widget.add_node(node)

            self.ifdag, self.sort_node_list = TopologicalSort(self._graph)
            self.path_list, _, _, _, _, _ = CriticalPath(self._graph)
            self.sort_column.myupdate(self.sort_node_list)
            self.path_column.myupdate(self.path_list)

    def add_edge(self):
        edge=Edge("v9","v100",3)
        if self._graph.add_edge(edge.start_vertex,edge.end_vertex,edge.weight):
            self.graph_widget.add_edge(edge)
            self.adjoint_widget.add_edge(edge)
            self.ifdag, self.sort_node_list = TopologicalSort(self._graph)
            self.path_list, _, _, _, _, _ = CriticalPath(self._graph)
            self.sort_column.myupdate(self.sort_node_list)
            self.path_column.myupdate(self.path_list)

    def topo_sort(self):
        self.topo_animation_map = {}

        self.sort_column.myclear()
        for node in self.sort_node_list:
            node_anime = QParallelAnimationGroup()
            anime1 = self.adjoint_widget.hidden_node_animation(node)
            anime2 = self.graph_widget.hidden_node_animation(node)
            anime3 = self.sort_column.add_node_animation(node)
            node_anime.addAnimation(anime1)
            node_anime.addAnimation(anime2)
            node_anime.addAnimation(anime3)
            self.topo_animation_map[node] = node_anime

        self.topo_animation = QSequentialAnimationGroup()
        for node in self.sort_node_list:
            self.topo_animation.addAnimation(self.topo_animation_map[node])
        self.topo_animation.start()

    def recover_all(self):
        self.recover_animation = QParallelAnimationGroup()
        anime1 = self.adjoint_widget.recover_all_animation()
        anime2 = self.graph_widget.recover_all_animation()
        self.recover_animation.addAnimation(anime1)
        self.recover_animation.addAnimation(anime2)

        self.recover_animation.start()

    def show_critical_path(self):
        self.show_critical_path_flag=~self.show_critical_path_flag
        if self.show_critical_path_flag:
            self.graph_widget._load_critical_path()
        else:
            self.graph_widget._load_graph()


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
