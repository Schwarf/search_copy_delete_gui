import platform
from typing import Dict

from PyQt5.QtCore import QRegExp, QCoreApplication
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLabel, QVBoxLayout, QTableWidgetItem

from misc.byte_format import format_size
from misc.dictionary_string_keys import *
from runnables.path_search_runnable import PathSearchRunnable
from runnables.thread_manager import ThreadManager
from ui_elements import copy_dialog_window
from ui_elements.main_window import inputs, outputs


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""

    def __init__(self):
        super().__init__()
        self._show_files_default_search_path_check_box = None
        self._file_counter = None
        self._smallest_file = None
        self._largest_file = None
        self._files_sum = None
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
        self._show_files_default_search_path_check_box = \
            inputs.show_files_default_search_path_check_box_setup(self, self.run_search)

        self._table = outputs.output_table(self)
        self._search_button = inputs.search_button_setup(self, self.run_search)
        self._copy_dialog_button = inputs.copy_dialog_button(self, self.copy_dialog_window)
        self._file_counter = outputs.initialize_read_only_qline_edit(self)
        self._largest_file = outputs.initialize_read_only_qline_edit(self)
        self._smallest_file = outputs.initialize_read_only_qline_edit(self)
        self._files_sum = outputs.initialize_read_only_qline_edit(self)

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        self.create_ui_elements()
        outer_layout = QVBoxLayout()
        self.setCentralWidget(self._table)
        upper_form_layout = QFormLayout()
        upper_form_layout.addRow(QLabel("Detected operating system: "), QLabel(f"{platform.system()}"))
        upper_form_layout.addRow(QLabel("Provide the default search path here."), self._search_path_input)
        upper_form_layout.addRow("Show files in default search path", self._show_files_default_search_path_check_box)
        upper_form_layout.addRow("Ignore hidden folders", self._ignore_hidden_files_check_box)
        upper_form_layout.addRow(self._search_button, self._folder_file_pattern_input)
        upper_form_layout.addRow("Number of folders/files found: ", self._file_counter)
        upper_form_layout.addRow("Smallest file: ", self._smallest_file)
        upper_form_layout.addRow("Largest file: ", self._largest_file)
        upper_form_layout.addRow("Total memory of files found: ", self._files_sum)
        # upper_from_layout.addRow("Folders/files found in given path (max. 5000)", self._search_output)

        lower_form_layout = QFormLayout()
        lower_form_layout.addRow("To copy files please press button", self._copy_dialog_button)
        lower_form_layout.addRow("Exit button", self._exit_button)
        outer_layout.addLayout(upper_form_layout)
        outer_layout.addWidget(self._table)
        outer_layout.addLayout(lower_form_layout)
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        self.show()

    def configure_copy_dialog_input(self):
        input = {}
        input["SearchPathInput"] = self._search_path_input.text()
        input["FolderFilePattern"] = self._folder_file_pattern_input.text()
        input["StartPathValidator"] = self._start_path_validator
        input["FolderFileValidator"] = self._folder_file_validator
        input["CopyRunnable"] = self.run_copy
        return input

    def copy_dialog_window(self):
        #        if self._copy_dialog_window is None or not self._copy_dialog_window.isVisible():
        input = self.configure_copy_dialog_input()
        self._copy_dialog_window = copy_dialog_window.open_copy_dialog_window(input)

    #        else:
    #            self._copy_dialog_window.activateWindow()
    # self._copy_dialog_window.destroyed.connect(help)

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
        text = f"Still searching ... So far {number_of_hits} elements found!"
        outputs.add_one_signal_item_table(text, self._table)

    def _on_search_button_clicked(self, search_succeeded: bool, sorted_path_list: Dict,
                                  search_statistics: Dict) -> None:
        """Button Action function"""
        if not search_succeeded:
            text = "Invalid path!!!"
            outputs.add_one_signal_item_table(text, self._table)
            return
        elif len(sorted_path_list) == 0:
            text = "No results found!"
            outputs.add_one_signal_item_table(text, self._table)
            return

        # self._search_results = search_results
        row = 0
        self._table.setRowCount(len(sorted_path_list))

        for size_or_hash, path in sorted_path_list.items():
            # append_text_in_color(self._search_output, path, color)
            path_item = QTableWidgetItem(str(path))
            self._table.setItem(row, 0, path_item)

            size_item = QTableWidgetItem()
            if hash(path) != size_or_hash:
                size_item = QTableWidgetItem(format_size(size_or_hash))
            self._table.setItem(row, 1, size_item)
            row += 1

        if search_succeeded:
            self._file_counter.clear()
            self._files_sum.clear()
            self._largest_file.clear()
            self._smallest_file.clear()
            if FILE_COUNT in search_statistics:
                self._file_counter.setText(str(search_statistics[FILE_COUNT]))
            if SUM_OF_FILE_SIZES in search_statistics:
                self._files_sum.setText(format_size(search_statistics[SUM_OF_FILE_SIZES]))
            if LARGEST_FILE in search_statistics:
                self._largest_file.setText(format_size(search_statistics[LARGEST_FILE]))
            if SMALLEST_FILE in search_statistics:
                self._smallest_file.setText(format_size(search_statistics[SMALLEST_FILE]))

    def on_exit(self):
        self._thread_manager.stop_all_runnables()
