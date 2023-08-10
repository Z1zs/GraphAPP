from Graph import Graph, Vertex, Edge
from PyQt5.QtCore import (QSequentialAnimationGroup, QParallelAnimationGroup, QAbstractAnimation)
from PyQt5.QtWidgets import (QDoubleSpinBox, QDialogButtonBox, QDialog, QLabel, QLineEdit, QVBoxLayout,
                             QWidget, QHBoxLayout, QMessageBox, QMainWindow, QAction)
from AdjointListVisualization import AdjiontListView
from ColumnItem import PathColumn, SortColumn
from Network import GraphView
from MyAlgorithm import TopologicalSort, CriticalPath, CheckConnectivity


class AddNodeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setWindowTitle("Add Vertex")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self._accept)
        self.buttonBox.rejected.connect(self.reject)

        self.message = QLabel("Please input the vertex name:")
        self.nameedit = QLineEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.nameedit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def _accept(self):
        if self.nameedit.text() is not None and self.nameedit.text() != "":
            new_node = Vertex(self.nameedit.text())
            success_flag, wronginfo = self._parent._graph.add_vertex(new_node)
            if success_flag:
                self._parent.add_node(new_node)
                self.close()
                return True
            else:
                WrongDialog = QMessageBox(self)
                WrongDialog.setWindowTitle("Warning")
                WrongDialog.setText(wronginfo)
                WrongDialog.exec()
                return False
        else:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Node name can't be empty!")
            WrongDialog.exec()
            return False


class DeleteNodeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setWindowTitle("Delete Vertex")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self._accept)
        self.buttonBox.rejected.connect(self.reject)

        self.message = QLabel("Please input the name of vertex to be deleted:")
        self.name_edit = QLineEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def _accept(self):
        if self.name_edit.text() is not None and self.name_edit.text() != "":
            node = Vertex(self.name_edit.text())
            success_flag, wronginfo = self._parent._graph.remove_vertex(node)
            if success_flag:
                self._parent.delete_node(node)
                self.close()
                return True
            else:
                WrongDialog = QMessageBox(self)
                WrongDialog.setWindowTitle("Warning")
                WrongDialog.setText(wronginfo)
                WrongDialog.exec()
                return False
        else:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Node name can't be empty!")
            WrongDialog.exec()
            return False


class DeleteEdgeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setWindowTitle("Delete Edge")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self._accept)
        self.buttonBox.rejected.connect(self.reject)

        self.message1 = QLabel("Please input the start vertex of the edge:")
        self.start_edit = QLineEdit()

        self.message2 = QLabel("Please input the end vertex of the edge:")
        self.end_edit = QLineEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message1)
        self.layout.addWidget(self.start_edit)
        self.layout.addWidget(self.message2)
        self.layout.addWidget(self.end_edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def _accept(self):
        if self.start_edit.text() is None or self.start_edit.text() == "":
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Start vertex can't be empty!")
            WrongDialog.exec()
            return False
        if self.end_edit.text() is None or self.end_edit.text() == "":
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("End vertex can't be empty!")
            WrongDialog.exec()
            return False
        edge = Edge(self.start_edit.text(), self.end_edit.text(), 1)
        success_flag, wronginfo = self._parent._graph.remove_edge(edge.start_vertex, edge.end_vertex)
        if success_flag:
            self._parent.delete_edge(edge)
            self.close()
            return True
        else:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText(wronginfo)
            WrongDialog.exec()
            return False


class AddEdgeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.setWindowTitle("Add Edge")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self._accept)
        self.buttonBox.rejected.connect(self.reject)

        self.message1 = QLabel("Please input the start vertex:")
        self.start_edit = QLineEdit()

        self.message2 = QLabel("Please input the end vertex:")
        self.end_edit = QLineEdit()

        self.message3 = QLabel("Please input the weight:")
        self.weight_edit = QDoubleSpinBox()
        self.weight_edit.setRange(0, 1e+9)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message1)
        self.layout.addWidget(self.start_edit)
        self.layout.addWidget(self.message2)
        self.layout.addWidget(self.end_edit)
        self.layout.addWidget(self.message3)
        self.layout.addWidget(self.weight_edit)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def _accept(self):
        if self.start_edit.text() is None or self.start_edit.text() == "":
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Start vertex can't be empty!")
            WrongDialog.exec()
            return False
        if self.end_edit.text() is None or self.end_edit.text() == "":
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("End vertex can't be empty!")
            WrongDialog.exec()
            return False
        edge = Edge(self.start_edit.text(), self.end_edit.text(), self.weight_edit.value())
        success_flag, wronginfo = self._parent._graph.add_edge(edge.start_vertex, edge.end_vertex, edge.weight)
        if success_flag:
            self._parent.add_edge(edge)
            self.close()
            return True
        else:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText(wronginfo)
            WrongDialog.exec()
            return False


class MyMainWindow(QMainWindow):
    def __init__(self, _graph: Graph):
        super(MyMainWindow, self).__init__()
        self.setWindowTitle("Graph APP")

        self._graph = _graph
        # 动画运行中不能被干扰
        self.topo_animation_map = {}
        self.anime_running_flag = False
        # 添加组件
        self.list_label = QLabel("The adjoint list of graph:")
        self.adjoint_widget = AdjiontListView(self._graph)
        self.network_label = QLabel("The network view of graph:")
        self.graph_widget = GraphView(self._graph)
        self.show_critical_path_flag = False

        self.sort_label = QLabel("Click [Update] to show the topo sequential of nodes:")
        self.sort_column = SortColumn([])
        self.path_label = QLabel("Click [Update] to show (one of) the critical path of the graph:")
        self.path_column = PathColumn([], [])

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.sort_label, 1)
        self.left_layout.addWidget(self.sort_column, 1)
        self.left_layout.addWidget(self.path_label, 1)
        self.left_layout.addWidget(self.path_column, 1)
        self.left_layout.addWidget(self.list_label, 1)
        self.left_layout.addWidget(self.adjoint_widget, 9)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.network_label, 1)
        self.right_layout.addWidget(self.graph_widget, 13)

        self._layout = QHBoxLayout()
        self._layout.addLayout(self.left_layout, 1)
        self._layout.addLayout(self.right_layout, 1)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self._layout)
        self.setCentralWidget(self.central_widget)
        self._load_menu()
        self.setMinimumSize(1800, 900)

    def run_tutorial_box(self):
        self.tutorial_box = QMessageBox(self)
        self.tutorial_box.setWindowTitle("功能详解")
        self.tutorial_info = ("功能说明(关闭后点击菜单栏[Help->Function]可再次查看):\n\n" +
                              "1.[show]-显示拓扑序列及关键路径：\n" +
                              "  1.1>[Topo]-显示拓扑排序过程\n" +
                              "    1.1.1>>[Topo->Play]-展示拓扑排序动画\n" +
                              "    1.1.2>>[Topo->Recover]-重新显示之前隐藏的组件\n" +
                              "  1.2>[Critical Path]-点击显示关键路径，再次点击可清除显示\n" +
                              "    >>被选定时,鼠标悬停Network可查看结点和边的详细信息,如VE,VL,E,L,L-E\n\n"
                              "2.[Edit]-对有向图进行编辑：\n" +
                              "  2.1>[Add]-添加顶点或边\n" +
                              "    2.1.1>>[Add Node]-添加新顶点\n" +
                              "    2.1.2>>[Add Edge]-在已有的两顶点之间添加新的边\n" +
                              "  2.2>[Delete]-删除顶点或边\n" +
                              "    2.2.1>>[Delete Node]-删除有向图的顶点\n" +
                              "    2.2.2>>[Delete Edge]-删除有向图的边\n\n" +
                              "3.[Update]-更新拓扑排序序列和关键路径\n\n" +
                              "4.[Help]-帮助\n" +
                              "  4.1>[Function]显示本使用说明\n" +
                              "  4.2>[Layout]介绍各组件信息\n\n"
                              "******************************************\n" +
                              "1和3均要求有向图非空,连通且无环\n" +
                              "******************************************\n" +
                              "##拓扑序列框和关键路径框不会随Edit操作刷新，点击Update更新信息栏\n" +
                              "##由于邻接表的高耦合性,Delete操作将重绘邻接链表组件\n" +
                              "##Show->Critical Path操作会对Network重新布局以突出拓扑结构\n"
                              )
        self.tutorial_box.setText(self.tutorial_info)
        self.tutorial_box.exec()

    def run_layout_box(self):
        self.layout_box = QMessageBox(self)
        self.layout_box.setWindowTitle("布局与组件")
        self.layout_info = ("组件说明\n\n" +
                            "1.拓扑序列栏Topo Sequential\n" +
                            "位置：左上角第一栏\n" +
                            "功能：显示拓扑序列结果\n" +
                            "注意事项: 首次运行需点击Update才会显示，之后每次Edit后通过Update刷新\n" +
                            "Update前自动检查有向图是否为空，是否连通，是否有环\n\n" +
                            "2.关键路径栏Critical Path\n" +
                            "位置：左上角第二栏\n" +
                            "功能：显示关键路径\n" +
                            "注意事项: 同上\n\n" +
                            "3.邻接链表视图Adjoint List\n" +
                            "位置：左下角\n" +
                            "功能：显示有向图的邻接链表\n" +
                            "说明: 深色矩形代表邻接表的顶点,第1栏为顶点名称，第2栏为顶点入度\n" +
                            "浅色矩形代表顶点的出边,第一栏为边的终点名称，第2栏为边的权重\n" +
                            "注意事项: 顶点出度和边的起点缺省显示,\n鼠标悬停可查看结点/边的具体信息\n" +
                            "播放拓扑排序动画时实时显示顶点入度变化\n\n" +
                            "3.有向图可视化Network View\n" +
                            "位置：右侧\n" +
                            "功能：有向图的拓扑结构可视化\n" +
                            "说明: 圆形组件为各顶点,箭头代表边的方向,数字代表边的权重\n" +
                            "[Show->Critical Path]被选中后,显示关键路径,位于关键路径上的边变为蓝色\n" +
                            "注意事项: [Show->Critical Path]被选中后，鼠标悬停可查看顶点的VE,VL和边的E,L,L-E等信息\n"
                            )
        self.layout_box.setText(self.layout_info)
        self.layout_box.exec()

    def _load_menu(self):
        menu = self.menuBar()
        # 菜单第一栏，展示栏
        show_menu = menu.addMenu("show")
        #  拓扑排序子菜单  #
        show_topo_menu = show_menu.addMenu("Topo Sort")
        #   播放拓扑排序动画   #
        play_topo_animation_action = QAction("Play/Pause", self)
        play_topo_animation_action.setStatusTip("Play Topo Sort Animation")
        play_topo_animation_action.triggered.connect(self.topo_sort)
        show_topo_menu.addAction(play_topo_animation_action)
        #   恢复动画效果   #
        recover_action = QAction("Recover", self)
        recover_action.setStatusTip("Recover All After The Topo Animation")
        recover_action.triggered.connect(self.recover_all)
        show_topo_menu.addAction(recover_action)
        #  显示关键路径  #
        self.show_critical_path_action = QAction("Critical Path", self)
        self.show_critical_path_action.setStatusTip("Show Critical Path in Network")
        self.show_critical_path_action.triggered.connect(self.show_critical_path)
        self.show_critical_path_action.setCheckable(True)
        show_menu.addAction(self.show_critical_path_action)

        # 菜单第二栏，编辑栏
        edit_menu = menu.addMenu("Edit")
        #  添加功能子菜单 #
        #   添加顶点   #
        edit_add_menu = edit_menu.addMenu("Add")
        add_node_action = QAction("Add Node", self)
        add_node_action.setStatusTip("Add New Node")
        add_node_action.triggered.connect(self.run_add_node_dialog)
        edit_add_menu.addAction(add_node_action)
        #   添加边   #
        add_edge_action = QAction("Add Edge", self)
        add_edge_action.setStatusTip("Add One Directed Edge")
        add_edge_action.triggered.connect(self.run_add_edge_dialog)
        edit_add_menu.addAction(add_edge_action)
        #  删除功能子菜单 #
        #   删除顶点   #
        edit_delete_menu = edit_menu.addMenu("Delete")
        delete_node_action = QAction("Delete Node", self)
        delete_node_action.setStatusTip("Delete One Node")
        delete_node_action.triggered.connect(self.run_delete_node_dialog)
        edit_delete_menu.addAction(delete_node_action)
        #   删除边   #
        delete_edge_action = QAction("Delete Edge", self)
        delete_edge_action.setStatusTip("Delete One Directed Edge")
        delete_edge_action.triggered.connect(self.run_delete_edge_dialog)
        edit_delete_menu.addAction(delete_edge_action)

        # 菜单第三栏，更新栏
        update_menu = menu.addMenu("Update")
        update_action = QAction("Update", self)
        update_action.setStatusTip("Update Topo Sequential and Critical Path")
        update_action.triggered.connect(self._update_dialog)
        update_menu.addAction(update_action)

        # 菜单第四栏，帮助栏
        help_menu = menu.addMenu("Help")
        #  功能说明  #
        show_tutorial_action = QAction("Function", self)
        show_tutorial_action.setStatusTip("Show user tutorial")
        show_tutorial_action.triggered.connect(self.run_tutorial_box)
        help_menu.addAction(show_tutorial_action)
        #  组件介绍  #
        show_layout_action = QAction("Layout", self)
        show_layout_action.setStatusTip("Introduction the layout")
        show_layout_action.triggered.connect(self.run_layout_box)
        help_menu.addAction(show_layout_action)

    def run_add_node_dialog(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
                self._update_dialog()
        if self.show_critical_path_action.isChecked():
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Please stop showing critical path first!")
            WrongDialog.exec()
            return False
        self.add_node_dlg = AddNodeDialog(self)
        self.add_node_dlg.exec()

    def add_node(self, node: Vertex):
        self.graph_widget.add_node(node)
        self.adjoint_widget.add_node(node)

    def run_add_edge_dialog(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
                self._update_dialog()
        if self.show_critical_path_action.isChecked():
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Please stop showing critical path first!")
            WrongDialog.exec()
            return False
        self.add_edge_dlg = AddEdgeDialog(self)
        self.add_edge_dlg.exec()

    def add_edge(self, edge):
        self.graph_widget.add_edge(edge)
        self.adjoint_widget.add_edge(edge)

    def run_delete_node_dialog(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
                self._update_dialog()
        if self.show_critical_path_action.isChecked():
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Please stop showing critical path first!")
            WrongDialog.exec()
            return False
        self.del_node_dlg = DeleteNodeDialog(self)
        self.del_node_dlg.exec()

    def delete_node(self, node):
        self.graph_widget.remove_node(node)
        self.adjoint_widget.remove_node(node)  # 无需调用参数，直接更新

    def run_delete_edge_dialog(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
                self._update_dialog()
        if self.show_critical_path_action.isChecked():
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("Please stop showing critical path first!")
            WrongDialog.exec()
            return False
        self.del_edge_dlg = DeleteEdgeDialog(self)
        self.del_edge_dlg.exec()

    def delete_edge(self, edge):
        self.graph_widget.remove_edge(edge)
        self.adjoint_widget.remove_edge(edge)  # 无需调用参数，直接更新

    def load_topo_animation(self):
        self.topo_animation_map = {}
        # 先检查连通性和是否有环
        if not self._update_dialog():
            return False

        # 依次记录结点动画
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

    def topo_sort(self):
        self.load_topo_animation()
        if self.topo_animation.state() == QAbstractAnimation.Stopped:
            self.topo_animation.start()
            return QAbstractAnimation.Running
        if self.topo_animation.state() == QAbstractAnimation.Paused:
            self.topo_animation.resume()
            return QAbstractAnimation.Running
        if self.topo_animation.state() == QAbstractAnimation.Running:
            self.topo_animation.pause()
            return QAbstractAnimation.Paused

    def recover_all(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self._update_dialog()
        self.adjoint_widget.recover_all_animation()
        anime = self.graph_widget.recover_all_animation()
        anime.start()

    def show_critical_path(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
                self._update_dialog()
        self.show_critical_path_flag = ~self.show_critical_path_flag
        if self.show_critical_path_flag:
            if not self._update_dialog():
                self.show_critical_path_flag = ~self.show_critical_path_flag
                self.show_critical_path_action.setChecked(False)
                return False
            self.graph_widget._load_critical_path()
        else:
            self.graph_widget._load_graph()

    def _update_dialog(self):
        if self.topo_animation_map != {}:
            if self.topo_animation.state() == QAbstractAnimation.Running:
                self.topo_animation.stop()
                self.recover_all()
        # 空值处理
        if len(self._graph.get_vertices()) == 0:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("The graph is empty!")
            WrongDialog.exec()
            return False
        # 检查连通性
        self.ifconnectivity = CheckConnectivity(self._graph)
        if not self.ifconnectivity:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("The graph is not connected graph!")
            WrongDialog.exec()
            return False

        # 检查是否为有向无环图
        self.ifdag, self.sort_node_list = TopologicalSort(self._graph)
        self.path_list, _, _, _, _, _ = CriticalPath(self._graph)
        if self.ifdag:
            self.sort_column.myupdate(self.sort_node_list)
            self.path_column.myupdate(self.path_list, self._graph.get_dist())
        else:
            WrongDialog = QMessageBox(self)
            WrongDialog.setWindowTitle("Warning")
            WrongDialog.setText("The graph is not DAG!")
            WrongDialog.exec()
            return False
        return True
