from typing import List

from PyQt5.QtCore import QRegExp, QThreadPool, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QFormLayout, QTextEdit, QHBoxLayout, QLabel

from q_misc import append_text_in_color
from q_runnable import PathSearchRunnable, ThreadCounter


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self._title = 'Search for files with pattern in directories'
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
        self._thread_counter.thread_count_changed.connect(lambda count: print("Thread count is: ", count))
        self._thread_pool = QThreadPool.globalInstance()

    def setup_search_path_input(self) -> QLineEdit:
        default_path = QLineEdit(self)
        default_path.setValidator(self._start_path_validator)
        default_path.textChanged.connect(self.run_search)
        return default_path

    def setup_exit_button(self) -> QPushButton:
        exit_button = QPushButton('Exit', self)
        # exit_button.move(20, 80)
        exit_button.clicked.connect(QCoreApplication.instance().quit)
        return exit_button

    def setup_search_output(self) -> QTextEdit:
        output_text_box = QTextEdit(self)
        output_text_box.setReadOnly(True)
        return output_text_box

    def setup_file_pattern_input(self) -> QLineEdit:
        file_pattern_text_box = QLineEdit(self)
        file_pattern_text_box.setValidator(self._sub_path_validator)
        return file_pattern_text_box

    def setup_search_button(self) -> QPushButton:
        search_button = QPushButton("Search file pattern")
        search_button.clicked.connect(self.run_search)
        return search_button

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        # label
        # Create textbox
        self._search_path_input = self.setup_search_path_input()
        self._search_output = self.setup_search_output()
        self._file_pattern_input = self.setup_file_pattern_input()

        exit_button = self.setup_exit_button()
        self._search_button = self.setup_search_button()


        outer_layout = QFormLayout()
        outer_layout.addRow("Provide the default search path here.", self._search_path_input)
        outer_layout.addRow(self._search_button, self._file_pattern_input)
        outer_layout.addRow("Folders found in given path", self._search_output)
        outer_layout.addRow("Exit button", exit_button)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def run_search(self):
        sender = self.sender()
        if self._thread_counter.count < self._max_thread_count:
            if sender == self._search_button:
                self._runnable = PathSearchRunnable(self._thread_counter, self._search_path_input.text(),
                                                    self._file_pattern_input.text())
            elif sender == self._search_path_input:
                self._runnable = PathSearchRunnable(self._thread_counter, self._search_path_input.text())
            self._runnable.signal_search_finished.search_result_ready.connect(self._on_search_button_clicked)
            self._thread_pool.start(self._runnable)

    def _on_search_button_clicked(self, search_results: List) -> None:
        """Button Action function"""
        color = 'black'
        if len(search_results) == 0:
            color = 'red'
            search_results = ['Invalid path!!!']
        else:
            self._search_output.clear()
        for result in search_results:
            append_text_in_color(self._search_output, result, color)
