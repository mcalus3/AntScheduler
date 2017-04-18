import sys
from UIController import CLIController, GUIController
from PyQt5 import QtWidgets, QtGui
import ctypes


def main(mode="gui"):
    if mode == 'cli':
        # CLI initialization
        manager = CLIController()
        manager.algorithm_run()
    else:
        # GUI initialization
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('..\docs\AntScheduler_icon.png'))
        manager = GUIController()
        manager.show()
        app.exec_()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
