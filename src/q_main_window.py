from typing import List

from PyQt5.QtCore import QRegExp, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout

from runnables.q_path_search_runnable import PathSearchRunnable
from runnables.q_thread_manager import ThreadManager
from ui_elements import inputs, outputs
from ui_elements.misc import append_text_in_color


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self._file_counter = None
        self._search_output = None
        self._search_button = None
        self._ignore_hidden_files_check_box = None
        self._exit_button = None
        self._folder_file_pattern_input = None
        self._search_path_input = None
        self._title = 'Search for files with pattern in directories'
        self._left = 10
        self._top = 10
        self._width = 1920
        self._height = 1080
        start_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\/]+")
        sub_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\*\.\/]+")
        self._start_path_validator = QRegExpValidator(start_path_regular_expression)
        self._sub_path_validator = QRegExpValidator(sub_path_regular_expression)
        self.init_ui()
        self._thread_manager = ThreadManager()

        # We only use maximum up to half the threads of the system

    def create_ui_elements(self):
        self._search_path_input = inputs.default_search_path_setup(self, self._start_path_validator, self.run_search)
        self._folder_file_pattern_input = inputs.folder_file_pattern_setup(self, self._sub_path_validator)
        self._exit_button = inputs.exit_button_setup(self, QCoreApplication.instance().quit)
        self._ignore_hidden_files_check_box = inputs.setup_ignore_hidden_files_check_box(self, self.run_search)
        self._search_button = inputs.search_button_setup(self, self.run_search)
        self._search_output = outputs.search_output_setup(self)
        self._file_counter = outputs.file_counter_setup(self)

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        self.create_ui_elements()
        outer_layout = QFormLayout()
        outer_layout.addRow("Provide the default search path here.", self._search_path_input)
        outer_layout.addRow("Ignore hidden folders", self._ignore_hidden_files_check_box)
        outer_layout.addRow(self._search_button, self._folder_file_pattern_input)
        outer_layout.addRow("Number of folders/files found: ", self._file_counter)
        outer_layout.addRow("Folders/files found in given path (max. 5000)", self._search_output)
        outer_layout.addRow("Exit button", self._exit_button)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def run_search(self):
        runnable = PathSearchRunnable()
        if self._search_path_input.text():
            runnable.set_path(self._search_path_input.text())
        if self._folder_file_pattern_input.text():
            runnable.set_folder_file_pattern(self._folder_file_pattern_input.text())
        runnable.set_ignore_files(self._ignore_hidden_files_check_box.checkState() == 2)
        runnable.search_signal_helper.search_result_ready.connect(self._on_search_button_clicked)
        runnable.search_signal_helper.search_still_ongoing.connect(self._on_still_searching)
        self._thread_manager.start_runnable(runnable)

    def _on_still_searching(self):
        color = 'red'
        self._search_output.clear()
        text = "Still searching ... "
        append_text_in_color(self._search_output, text, color)

    def _on_search_button_clicked(self, search_succeeeded: bool, search_results: List) -> None:
        """Button Action function"""
        color = 'black'
        if not search_succeeeded:
            color = 'red'
            search_results = ['Invalid path!!!']
        elif len(search_results) == 0:
            color = 'red'
            search_results = ['No results found!']
            self._search_output.clear()
        else:
            self._search_output.clear()
        for result in search_results:
            append_text_in_color(self._search_output, result, color)

        if search_succeeeded:
            self._file_counter.clear()
            if len(search_results) < 5000:
                self._file_counter.setText(f"{len(search_results)}")
            else:
                self._file_counter.setText("5000+")

    def on_exit(self):
        self._thread_manager.stop_all_runnables()
