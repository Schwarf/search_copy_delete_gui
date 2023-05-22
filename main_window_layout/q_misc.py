from PyQt5.QtWidgets import QApplication, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor


def append_text_in_color(text_edit: QTextEdit, text:str, color: str):
    text_edit.append(f"<font color='{color}'>{text}</font>")