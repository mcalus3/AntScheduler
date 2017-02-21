import sys
import ImagesApi
from Manager import CLIManager, UIManager
from PyQt5 import QtWidgets
import pycallgraph

config_file = "config.ini"

graphviz = pycallgraph.output.GraphvizOutput()
graphviz.output_file = 'basic.png'
#with pycallgraph.PyCallGraph(output=graphviz):

if len(sys.argv) > 1 and sys.argv[1] == 'cli':
    # CLI initialization
    manager = CLIManager()
    manager.algorithm_run()
else:
    # GUI initialization
    app = QtWidgets.QApplication(sys.argv)
    manager = UIManager()
    manager.show()
    app.exec_()
