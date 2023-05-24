from typing import Optional, List

from PyQt5.QtCore import QThread, QRegExp, QThreadPool, QCoreApplication
from PyQt5.QtGui import QRegExpValidator, QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QFormLayout, QTextEdit, QVBoxLayout, \
    QDialogButtonBox, QHBoxLayout, QLabel

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
        self._thread_counter.thread_count_changed.connect(lambda count: print("Thread count is: ", count))
        self._thread_pool = QThreadPool.globalInstance()

    def _default_path(self) -> QLineEdit:
        start_path_input = QLineEdit(self)
        start_path_input.setValidator(self._start_path_validator)
        start_path_input.textChanged.connect(self.run_search)
        return start_path_input

    def _exit_button_clicked(self):
        QCoreApplication.instance().quit()

    def _exit_button(self) -> QPushButton:
        exit_button = QPushButton('Exit', self)
        #exit_button.move(20, 80)
        exit_button.clicked.connect(self._exit_button_clicked)
        return exit_button

    def _found_folders(self) -> QTextEdit:
        output_text_box = QTextEdit(self)
        output_text_box.setReadOnly(True)
        return output_text_box

    def _file_pattern_text_box(self) -> QLineEdit:
        file_pattern_text_box = QLineEdit(self)
        file_pattern_text_box.setValidator(self._sub_path_validator)
        file_pattern_text_box.textChanged.connect(self.run_search)
        return file_pattern_text_box

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        # label
        # Create textbox
        self._default_path = self._default_path()
        exit_button = self._exit_button()
        self._found_folders = self._found_folders()
        self._file_pattern_text_box = self._file_pattern_text_box()

        search_button = QPushButton("Search file pattern")
        search_button.clicked.connect(self.run_search)
        file_pattern_label = QLabel("Provide file pattern:")
        self._file_pattern_line_edit = QLineEdit()
        file_pattern_widget = QWidget()
        file_pattern_layout = QHBoxLayout(file_pattern_widget)
        file_pattern_layout.addWidget(file_pattern_label)
        file_pattern_layout.addWidget(self._file_pattern_line_edit)

        outer_layout = QFormLayout()
        outer_layout.addRow("Provide the default search path here.", self._default_path)
        outer_layout.addRow(file_pattern_widget, search_button)
        outer_layout.addRow("Folders found in given path", self._found_folders)
        outer_layout.addRow("Exit button", exit_button)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def run_search(self):
        if self._thread_counter.count < self._max_thread_count:
            if not self._file_pattern_line_edit.text():
                self._runnable = PathSearchRunnable(self._thread_counter, self._default_path.text())
            else:
                self._runnable = PathSearchRunnable(self._thread_counter, self._default_path.text(), self._file_pattern_line_edit.text())
            self._runnable.signal_search_finished.search_result_ready.connect(self._on_search_button_clicked)
            self._thread_pool.start(self._runnable)

    def _on_search_button_clicked(self, search_results: List) -> None:
        """Button Action function"""
        color = 'black'
        if len(search_results) == 0:
            color = 'red'
            search_results = ['Invalid path!!!']
        else:
            self._found_folders.clear()
        for result in search_results:
            append_text_in_color(self._found_folders, result, color)
