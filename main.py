from MainWindow import MyMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from Graph import Graph
import sys
import os
from pathlib import Path

basedir = os.path.dirname(__file__)
try:
    from ctypes import windll

    myappid = 'Tongji.2151773霍家灏.GraphAPP'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def CreateGraph():
    _graph = Graph()
    _graph.add_vertex("v1")
    _graph.add_vertex("v2")
    _graph.add_vertex("v3")
    _graph.add_vertex("v4")
    _graph.add_vertex("v5")
    _graph.add_vertex("v6")
    _graph.add_vertex("v7")
    _graph.add_vertex("v8")
    _graph.add_vertex("v9")
    _graph.add_vertex("v10")

    _graph.add_edge("v1", "v2", 6)
    _graph.add_edge("v1", "v3", 4)
    _graph.add_edge("v1", "v4", 5)
    _graph.add_edge("v2", "v5", 1)
    _graph.add_edge("v3", "v5", 1)
    _graph.add_edge("v4", "v6", 2)
    _graph.add_edge("v5", "v7", 9)
    _graph.add_edge("v5", "v8", 7)
    _graph.add_edge("v6", "v8", 4)
    _graph.add_edge("v7", "v9", 2)
    _graph.add_edge("v8", "v9", 4)
    _graph.add_edge("v8", "v10", 100)
    return _graph


if __name__ == '__main__':
    # Create a networkx graph
    graph = CreateGraph()
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style.qss').read_text())
    app.setWindowIcon(QIcon(os.path.join(basedir, 'graph.ico')))
    widget = MyMainWindow(graph)
    widget.show()
    widget.resize(800, 600)
    app.exec()
