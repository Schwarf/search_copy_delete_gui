from PyQt5.QtWidgets import QLineEdit, QTextEdit


def initialize_read_only_qline_edit(parent) -> QLineEdit:
    qline_edit = QLineEdit(parent)
    qline_edit.setReadOnly(True)
    qline_edit.setText("---")
    return qline_edit


def search_output_setup(parent) -> QTextEdit:
    output_text_box = QTextEdit(parent)
    output_text_box.setReadOnly(True)
    return output_text_box
