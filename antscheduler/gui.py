#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QDesktopWidget
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def init_ui(self):

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.resize(1000, 600)
        self.center()
        self.setWindowTitle('AntScheduler')
        self.show()

    def close_event(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    main_frame = Example()
    sys.exit(app.exec_())

