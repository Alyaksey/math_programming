import sys
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Лабораторная 7'
        self.left = 0
        self.top = 0
        self.width = 720
        self.height = 600
        self.setWindowTitle(self.title)
        self.setFixedSize(720, 600)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)
        self.tabs.addTab(self.tab1, "Теория")
        self.tabs.addTab(self.tab2, "Решение")
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(WebView())
        self.tab1.setLayout(self.tab1.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class WebView(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.browser = QWebEngineView()
        url = os.getcwd().replace('\\', '/') + '/lab7.html'
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
