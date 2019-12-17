import os
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QLabel, QWidget, QTabWidget, QVBoxLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication

import coord
import gradient
import plotter


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Решение задачи безусловной оптимизации функций многих переменных'
        self.setWindowTitle(self.title)
        self.resize(800, 600)
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
        self.info_tab = QWidget()
        self.theory_tab = QWidget()
        self.lit_tab = QWidget()
        self.solve_tab = QWidget()
        self.tabs.addTab(self.info_tab, "Краткая справка")
        self.tabs.addTab(self.theory_tab, "Теория")
        self.tabs.addTab(self.lit_tab, "Литература")
        self.tabs.addTab(self.solve_tab, "Решение")
        self.info_tab.layout = QVBoxLayout(self)
        self.theory_tab.layout = QVBoxLayout(self)
        self.lit_tab.layout = QVBoxLayout(self)
        self.solve_tab.layout = QVBoxLayout(self)
        self.function_label = QLabel('Введите функции:')
        self.coords_label = QLabel('Начальные координаты:')
        self.coord_desc_label = QLabel('Циклический покоординатный спуск:')
        self.grad_desc_label = QLabel('Наискорейший спуск:')
        self.function_textbox = QLineEdit()
        self.show_button = QPushButton('Показать график')
        self.hbox = QHBoxLayout()
        self.x1_textbox = QLineEdit()
        self.x1_textbox.setPlaceholderText('x1')
        self.x1_textbox.setFixedWidth(30)
        self.x2_textbox = QLineEdit()
        self.coord_desc_textbox = QTextEdit()
        self.grad_desc_textbox = QTextEdit()
        self.coord_desc_textbox.setReadOnly(True)
        self.grad_desc_textbox.setReadOnly(True)
        self.x2_textbox.setPlaceholderText('x2')
        self.x2_textbox.setFixedWidth(30)
        self.hbox.addWidget(self.coords_label, 0, Qt.AlignRight)
        self.hbox.addWidget(self.x1_textbox)
        self.hbox.addWidget(self.x2_textbox)
        self.solve_button = QPushButton('Решить')
        self.show_button.pressed.connect(self.show_plot)
        self.solve_button.pressed.connect(self.fill_text_boxes)
        self.solve_tab.layout.addWidget(self.coord_desc_label, 0, Qt.AlignTop)
        self.solve_tab.layout.addWidget(self.coord_desc_textbox)
        self.solve_tab.layout.addWidget(self.grad_desc_label)
        self.solve_tab.layout.addWidget(self.grad_desc_textbox)
        self.solve_tab.layout.addWidget(self.function_label, 0, Qt.AlignBottom)
        self.solve_tab.layout.addWidget(self.function_textbox)
        self.solve_tab.layout.addWidget(self.show_button)
        self.solve_tab.layout.addLayout(self.hbox)
        self.solve_tab.layout.addWidget(self.solve_button)
        self.info_tab.layout.addWidget(Tab('/info.html'))
        self.theory_tab.layout.addWidget(Tab('/doc.pdf'))
        self.lit_tab.layout.addWidget(Tab('/lit.pdf'))
        self.info_tab.setLayout(self.info_tab.layout)
        self.theory_tab.setLayout(self.theory_tab.layout)
        self.lit_tab.setLayout(self.lit_tab.layout)
        self.solve_tab.setLayout(self.solve_tab.layout)
        self.layout.addWidget(self.tabs)

    def show_plot(self):
        function = self.function_textbox.text()
        try:
            plotter.plot(function)
        except (SyntaxError, AttributeError, NameError, ValueError):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Функция введена неправильно')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def fill_text_boxes(self):
        try:
            x1, x2, f = coord.find_min(self.function_textbox.text(), float(self.x1_textbox.text()),
                                       float(self.x2_textbox.text()))
            self.coord_desc_textbox.setReadOnly(False)
            self.coord_desc_textbox.clear()
            self.coord_desc_textbox.setText('x1 = {}\nx2 = {}\nfmin = {}'.format(x1.__str__().rstrip('0').rstrip(','),
                                                                                 x2.__str__().rstrip('0').rstrip('.'),
                                                                                 f.__str__().rstrip('0').rstrip('.')))
            self.coord_desc_textbox.setReadOnly(True)
            dx1, dx2, x1, x2, f = gradient.find_min(self.function_textbox.text(), float(self.x1_textbox.text()),
                                                    float(self.x2_textbox.text()))
            self.grad_desc_textbox.setReadOnly(False)
            self.grad_desc_textbox.clear()
            self.grad_desc_textbox.setText(
                'dx1 = {}\ndx2={}\nx1 = {}\nx2 = {}\nfmin = {}'.format(dx1, dx2, x1.__str__().rstrip('0').rstrip(','),
                                                                       x2.__str__().rstrip('0').rstrip('.'),
                                                                       f.__str__().rstrip('0').rstrip('.')))
            self.grad_desc_textbox.setReadOnly(True)
        except (SyntaxError, AttributeError, NameError):
            self.show_error('Введите правильно функцию')
        except ValueError:
            self.show_error('Введите начальные координаты')
        except OverflowError:
            self.show_error('Подберите другие координаты')
        except RuntimeError:
            self.show_error('Невозможно вычислить')

    def show_error(self, message):
        msg = QMessageBox()
        msg.setWindowTitle('Ошибка')
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class Tab(QMainWindow):
    def __init__(self, file_name):
        super(QMainWindow, self).__init__()
        self.browser = QWebEngineView()
        url = os.getcwd().replace('\\', '/') + file_name
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
