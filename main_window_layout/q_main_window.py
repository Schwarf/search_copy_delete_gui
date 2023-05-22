from typing import Optional, List

from PyQt5.QtCore import QThread, QRegExp, QThreadPool, QCoreApplication
from PyQt5.QtGui import QRegExpValidator, QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QFormLayout, QTextEdit

from q_misc import append_text_in_color
from q_runnable import PathSearchRunnable, ThreadCounter


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self._title = 'Search only'
        self._left = 10
        self._top = 10
        self._width = 1920
        self._height = 1080
        start_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\/]+")
        sub_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\*\/]+")
        self._start_path_validator = QRegExpValidator(start_path_regular_expression)
        self._sub_path_validator = QRegExpValidator(sub_path_regular_expression)
        self.init_ui()
        self._max_thread_count = QThreadPool.globalInstance().maxThreadCount()
        self._thread_counter = ThreadCounter()
        # self._thread_counter.thread_count_changed.connect(lambda count: print("Thread count is: ", count))
        self._thread_pool = QThreadPool.globalInstance()

    def _start_path_input(self) -> QLineEdit:
        start_path_input = QLineEdit(self)
        start_path_input.move(20, 20)
        start_path_input.resize(280, 40)
        start_path_input.setValidator(self._start_path_validator)
        start_path_input.textChanged.connect(self.run_task)
        return start_path_input

    def _exit_button_clicked(self):
        QCoreApplication.instance().quit()

    def _exit_button(self) -> QPushButton:
        exit_button = QPushButton('Exit', self)
        exit_button.move(20, 80)
        exit_button.clicked.connect(self._exit_button_clicked)
        return exit_button

    def _search_button(self) -> QPushButton:
        search_button = QPushButton('Search', self)
        search_button.move(20, 80)
        search_button.clicked.connect(self._on_search_button_clicked)
        return search_button

    def _output_text_box(self) -> QTextEdit:
        output_text_box = QTextEdit(self)
        output_text_box.move(120, 120)
        output_text_box.resize(450, 140)
        output_text_box.setReadOnly(True)
        return output_text_box

    def _file_pattern_text_box(self) -> QLineEdit:
        file_pattern_text_box = QLineEdit(self)
        file_pattern_text_box.setValidator(self._sub_path_validator)
        file_pattern_text_box.textChanged.connect(self.run_task)
        return file_pattern_text_box

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        # label
        # Create textbox
        self._start_path_input = self._start_path_input()
        search_button = self._search_button()
        exit_button = self._exit_button()
        self._output_text_box = self._output_text_box()
        self._file_pattern_text_box = self._file_pattern_text_box()

        layout = QFormLayout()
        layout.addRow("Provide the default search path here.", self._start_path_input)
        layout.addRow("File pattern", self._file_pattern_text_box)
        layout.addRow("Search button", search_button)
        layout.addRow("Output", self._output_text_box)
        layout.addRow("Exit button", exit_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def run_task(self):
        if self._thread_counter.count < self._max_thread_count:
            self._runnable = PathSearchRunnable(self._thread_counter, self._start_path_input.text())
            self._runnable.signal_search_finished.search_result_ready.connect(self._on_search_button_clicked)
            self._thread_pool.start(self._runnable)

    def _on_search_button_clicked(self, search_results: List) -> None:
        """Button Action function"""
        if len(search_results) == 0:
            color = 'red'
            text = 'The path is invalid!'
            append_text_in_color(self._output_text_box, text, color)
            return
        self._output_text_box.clear()
        for result in search_results:
            self._output_text_box.append(str(result))
