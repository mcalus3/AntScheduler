import UiForm
from PyQt5 import QtWidgets
import sys
from Manager import Manager
import GVApi

config_file = "config.ini"


class UIManager(QtWidgets.QMainWindow, UiForm.Ui_MainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.RunButton.clicked.connect(self.run_algorithm)

    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def run_algorithm(self):
        manager = Manager(config_file)
        if manager.config.render_images:
            GVApi.draw_graph(manager.nodes_list)
            
        manager.algorithm_run()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = UIManager()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
