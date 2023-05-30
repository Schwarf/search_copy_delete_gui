from PyQt5.QtWidgets import QLineEdit, QPushButton, QCheckBox


def folder_file_pattern_setup(parent, validator) -> QLineEdit:
    sub_folder_text_box = QLineEdit(parent)
    sub_folder_text_box.setValidator(validator)
    return sub_folder_text_box


def default_search_path_setup(parent, validator, slot_function) -> QLineEdit:
    search_path_input = QLineEdit(parent)
    search_path_input.setValidator(validator)
    search_path_input.textChanged.connect(slot_function)
    return search_path_input


def exit_button_setup(parent, slot_function) -> QPushButton:
    exit_button = QPushButton('Exit', parent)
    exit_button.clicked.connect(slot_function)
    return exit_button


def search_button_setup(parent, slot_function) -> QPushButton:
    search_button = QPushButton("Folder/file pattern", parent)
    search_button.clicked.connect(slot_function)
    return search_button


def setup_ignore_hidden_files_check_box(parent, slot_function) -> QCheckBox:
    ignore_hidden_files = QCheckBox("", parent)
    ignore_hidden_files.setCheckState(2)
    ignore_hidden_files.clicked.connect(slot_function)
    return ignore_hidden_files
