import UiForm
from PyQt5 import QtWidgets
import sys


class UIManager(QtWidgets.QMainWindow, UiForm.Ui_MainWindow):
    def __init__(self, parent=None):
        super(UIManager, self).__init__(parent)
        self.setupUi(self)
        #self.btnBrowse.clicked.connect(self.browse_folder)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = UIManager()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
