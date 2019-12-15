import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QLabel, QWidget, QTabWidget, QVBoxLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication

import plotter


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Решение задачи безусловной оптимизации функций многих переменных'
        self.setWindowTitle(self.title)
        self.resize(900, 720)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.addTab(self.tab1, "Краткая справка")
        self.tabs.addTab(self.tab2, "Теория")
        self.tabs.addTab(self.tab3, "Литература")
        self.tabs.addTab(self.tab4, "Решение")
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.tab3.layout = QVBoxLayout(self)
        self.tab4.layout = QVBoxLayout(self)
        self.label1 = QLabel('Введите уравнение:')
        self.label2 = QLabel('Начальные координаты:')
        self.label3 = QLabel('Циклический покоординатный спуск:')
        self.label4 = QLabel('Наискорейший спуск:')
        self.textbox1 = QLineEdit()
        self.show_button = QPushButton('Показать график')
        self.hbox = QHBoxLayout()
        self.textbox2 = QLineEdit()
        self.textbox2.setPlaceholderText('x1')
        self.textbox2.setFixedWidth(30)
        self.textbox3 = QLineEdit()
        self.textbox4 = QTextEdit()
        self.textbox5 = QTextEdit()
        self.textbox4.setReadOnly(True)
        self.textbox5.setReadOnly(True)
        self.textbox3.setPlaceholderText('x2')
        self.textbox3.setFixedWidth(30)
        self.hbox.addWidget(self.label2, 0, Qt.AlignRight)
        self.hbox.addWidget(self.textbox2)
        self.hbox.addWidget(self.textbox3)
        self.solve_button = QPushButton('Решить')
        self.show_button.pressed.connect(self.show_plot)
        self.tab4.layout.addWidget(self.label3, 0, Qt.AlignTop)
        self.tab4.layout.addWidget(self.textbox4)
        self.tab4.layout.addWidget(self.label4)
        self.tab4.layout.addWidget(self.textbox5)
        self.tab4.layout.addWidget(self.label1, 0, Qt.AlignBottom)
        self.tab4.layout.addWidget(self.textbox1)
        self.tab4.layout.addWidget(self.show_button)
        self.tab4.layout.addLayout(self.hbox)
        self.tab4.layout.addWidget(self.solve_button)
        self.tab1.layout.addWidget(InfoTab())
        self.tab2.layout.addWidget(TheoryTab())
        self.tab3.layout.addWidget(LiteratureTab())
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)
        self.layout.addWidget(self.tabs)

    def show_plot(self):
        function = self.textbox1.text()
        try:
            plotter.plot(function)
        except (SyntaxError, AttributeError, NameError):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Функция введена неправильно')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


class InfoTab(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.browser = QWebEngineView()
        url = os.getcwd().replace('\\', '/') + '/info.html'
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)


class TheoryTab(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.browser = QWebEngineView()
        url = os.getcwd().replace('\\', '/') + '/doc.pdf'
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)


class LiteratureTab(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.browser = QWebEngineView()
        url = os.getcwd().replace('\\', '/') + '/lit.pdf'
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
