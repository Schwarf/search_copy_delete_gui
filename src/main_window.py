from typing import List

from PyQt5.QtCore import QRegExp, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLabel, QVBoxLayout, QHBoxLayout

from runnables.path_search_runnable import PathSearchRunnable
from runnables.thread_manager import ThreadManager
from ui_elements.main_window import inputs, outputs
from ui_elements.misc import append_text_in_color
from ui_elements import copy_dialog_window


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self._show_files_default_search_path_check_box = None
        self._file_counter = None
        self._search_output = None
        self._search_button = None
        self._ignore_hidden_files_check_box = None
        self._exit_button = None
        self._folder_file_pattern_input = None
        self._search_path_input = None
        self._copy_dialog_button = None
        self._copy_dialog_window = None
        self._title = 'Search for files/folders with pattern in directories'
        self._left = 10
        self._top = 10
        self._width = 1920
        self._height = 1080
        start_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\/]+")
        folder_file_regular_expression = QRegExp("[A-Za-z0-9\-\_\*\.\/]+")
        self._start_path_validator = QRegExpValidator(start_path_regular_expression)
        self._folder_file_validator = QRegExpValidator(folder_file_regular_expression)
        self.init_ui()
        self._thread_manager = ThreadManager()
        self._search_results = None

        # We only use maximum up to half the threads of the system

    def create_ui_elements(self):
        self._search_path_input = inputs.default_search_path_setup(self, self._start_path_validator, self.run_search)
        self._folder_file_pattern_input = inputs.folder_file_pattern_setup(self, self._folder_file_validator)
        self._exit_button = inputs.exit_button_setup(self, QCoreApplication.instance().quit)
        self._ignore_hidden_files_check_box = inputs.ignore_hidden_files_check_box_setup(self, self.run_search)
        self._show_files_default_search_path_check_box = inputs.show_files_default_search_path_check_box_setup(self,
                                                                                                               self.run_search)
        self._search_button = inputs.search_button_setup(self, self.run_search)
        self._copy_dialog_button = inputs.copy_dialog_button(self, self.copy_dialog_window)
        self._search_output = outputs.search_output_setup(self)
        self._file_counter = outputs.file_counter_setup(self)


    def init(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        form_layout.addRow(QLabel("Provide the default search path here: "), self._search_path_input)
        form_layout.addRow(QLabel("Folder/file pattern: "), self._folder_file_pattern_input)
        form_layout.addRow(QLabel("Number of folders/files found: "), self._file_counter)

        check_box_layout = QHBoxLayout()
        check_box_layout.addWidget(QLabel("Show files in default search path: "), self._show_files_default_search_path_check_box)
        check_box_layout.addWidget(QLabel("Ignore hidden folders: "), self._ignore_hidden_files_check_box)
        
    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        self.create_ui_elements()
        outer_layout = QFormLayout()
        outer_layout.addRow(QLabel("Provide the default search path here."), self._search_path_input)
        outer_layout.addRow("Show files in default search path", self._show_files_default_search_path_check_box)
        outer_layout.addRow("Ignore hidden folders", self._ignore_hidden_files_check_box)
        outer_layout.addRow(self._search_button, self._folder_file_pattern_input)
        outer_layout.addRow("Number of folders/files found: ", self._file_counter)
        outer_layout.addRow("Folders/files found in given path (max. 5000)", self._search_output)
        outer_layout.addRow("To copy files please press button", self._copy_dialog_button)
        outer_layout.addRow("Exit button", self._exit_button)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def configure_copy_dialog_input(self):
        input ={}
        input["SearchPathInput"] = self._search_path_input.text()
        input["FolderFilePattern"] = self._folder_file_pattern_input.text()
        input["StartPathValidator"]  =self._start_path_validator
        input["FolderFileValidator"] = self._folder_file_validator
        input["CopyRunnable"] = self.run_copy
        return input

    def copy_dialog_window(self):
#        if self._copy_dialog_window is None or not self._copy_dialog_window.isVisible():
        input = self.configure_copy_dialog_input()
        self._copy_dialog_window = copy_dialog_window.open_copy_dialog_window(input)
#        else:
#            self._copy_dialog_window.activateWindow()
        #self._copy_dialog_window.destroyed.connect(help)

    def _configure_path_search_runnable(self) -> PathSearchRunnable:
        runnable = PathSearchRunnable()
        if self._search_path_input.text():
            runnable.set_path(self._search_path_input.text())
        if self._folder_file_pattern_input.text():
            runnable.set_folder_file_pattern(self._folder_file_pattern_input.text())
        runnable.set_ignore_files(self._ignore_hidden_files_check_box.checkState() == 2)
        runnable.set_show_files_in_path(self._show_files_default_search_path_check_box.checkState() == 2)
        runnable.search_signal_helper.search_result_ready.connect(self._on_search_button_clicked)
        runnable.search_signal_helper.search_still_ongoing.connect(self._on_still_searching)
        return runnable

    def run_search(self):
        runnable = self._configure_path_search_runnable()
        self._thread_manager.start_runnable(runnable)

    def run_copy(self):
        pass

    def _on_still_searching(self, number_of_hits):
        color = 'red'
        self._search_output.clear()
        text = f"Still searching ... So far {number_of_hits} elements found!"
        append_text_in_color(self._search_output, text, color)

    def _on_search_button_clicked(self, search_succeeded: bool, search_results: List) -> None:
        """Button Action function"""
        color = 'black'
        if not search_succeeded:
            color = 'red'
            search_results = ['Invalid path!!!']
        elif len(search_results) == 0:
            color = 'red'
            search_results = ['No results found!']
            self._search_output.clear()
        else:
            self._search_output.clear()
        self._search_results = search_results
        for result in search_results:
            append_text_in_color(self._search_output, result, color)

        if search_succeeded:
            self._file_counter.clear()
            self._file_counter.setText(f"{len(search_results)}")

    def on_exit(self):
        self._thread_manager.stop_all_runnables()
