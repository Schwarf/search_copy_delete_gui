from typing import List

from PyQt5.QtCore import QRegExp, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QFormLayout, QTextEdit, QCheckBox

from q_misc import append_text_in_color
from runnables.q_path_search_runnable import PathSearchRunnable
from runnables.q_thread_manager import ThreadManager

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
        sub_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\*]+")
        self._start_path_validator = QRegExpValidator(start_path_regular_expression)
        self._sub_path_validator = QRegExpValidator(sub_path_regular_expression)
        self.init_ui()
        self._thread_manager = ThreadManager()
        # We only use maximum up to half the threads of the system

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
        search_button = QPushButton("Search file pattern", self)
        search_button.clicked.connect(self.run_search)
        return search_button

    def setup_ignore_hidden_files_check_box(self) -> QCheckBox:
        ignore_hidden_files = QCheckBox("Ignore hidden folders and files.", self)
        ignore_hidden_files.setCheckState(2)
        ignore_hidden_files.clicked.connect(self.run_search)
        return ignore_hidden_files

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
        self._ignore_hidden_files_check_box = self.setup_ignore_hidden_files_check_box()
        exit_button = self.setup_exit_button()
        self._search_button = self.setup_search_button()

        outer_layout = QFormLayout()
        outer_layout.addRow("Provide the default search path here.", self._search_path_input)
        outer_layout.addRow(self._search_button, self._file_pattern_input)
        outer_layout.addRow("", self._ignore_hidden_files_check_box)
        outer_layout.addRow("Folders/files found in given path (max. 5000)", self._search_output)
        outer_layout.addRow("Exit button", exit_button)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def run_search(self):
        sender = self.sender()
        if sender == self._search_button:
            runnable = PathSearchRunnable(self._search_path_input.text(), self._file_pattern_input.text())
        elif sender == self._search_path_input:
            runnable = PathSearchRunnable(self._search_path_input.text())
        elif sender == self._ignore_hidden_files_check_box:
            runnable = PathSearchRunnable(self._search_path_input.text(),
                                          ignore_hidden_files=self._ignore_hidden_files_check_box.checkState() == 2)
        runnable.search_signal_helper.search_result_ready.connect(self._on_search_button_clicked)
        runnable.search_signal_helper.search_update.connect(self._on_still_searching)
        self._thread_manager.start_runnable(runnable)

    def _on_still_searching(self):
        color = 'red'
        self._search_output.clear()
        text = "Still searching ... "
        append_text_in_color(self._search_output, text, color)


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

    def on_exit(self):
        self._thread_manager.stop_all_runnables()
