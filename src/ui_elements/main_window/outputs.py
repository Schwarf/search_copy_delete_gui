from PyQt5.QtWidgets import QLineEdit, QTextEdit


def file_counter_setup(parent) -> QLineEdit:
    file_counter = QLineEdit(parent)
    file_counter.setReadOnly(True)
    file_counter.setText("---")
    return file_counter


def search_output_setup(parent) -> QTextEdit:
    output_text_box = QTextEdit(parent)
    output_text_box.setReadOnly(True)
    return output_text_box
