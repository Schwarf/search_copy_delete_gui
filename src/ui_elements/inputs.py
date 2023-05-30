from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QPushButton


def file_pattern_setup(parent, validator) -> QLineEdit:
    file_pattern_text_box = QLineEdit(parent)
    file_pattern_text_box.setValidator(validator)
    return file_pattern_text_box

def sub_folder_pattern_setup(parent, validator) -> QLineEdit:
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
