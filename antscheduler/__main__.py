import sys
from Manager import CLIManager, UIManager
from PyQt5 import QtWidgets

config_file = "config.ini"


def main(mode="gui"):
    if mode == 'cli':
        # CLI initialization
        manager = CLIManager()
        manager.algorithm_run()
    else:
        # GUI initialization
        app = QtWidgets.QApplication(sys.argv)
        manager = UIManager()
        manager.show()
        app.exec_()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        main('cli')
    else:
        main('gui')
