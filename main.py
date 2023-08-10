from MainWindow import MyMainWindow
from PyQt5.QtWidgets import QApplication
from Graph import Graph
import sys
from pathlib import Path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style.qss').read_text())
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
    graph.add_vertex("v10")

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
    graph.add_edge("v8", "v10", 100)
    widget = MyMainWindow(graph)
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())
