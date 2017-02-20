import sys
import ImagesApi
from Manager import Manager, UIManager
from PyQt5 import QtWidgets

config_file = "config.ini"
manager = Manager(config_file)

if len(sys.argv) > 1 and sys.argv[1] == 'cli':
    # CLI initialization
    if manager.config.render_images:
        ImagesApi.draw_graph(manager.nodes_list)
    manager.algorithm_run()
else:
    # GUI initialization
    app = QtWidgets.QApplication(sys.argv)
    uimanager = UIManager(manager)
    uimanager.show()
    app.exec_()
