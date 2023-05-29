from PyQt5.QtWidgets import QTextEdit


def append_text_in_color(text_edit: QTextEdit, text: str, color: str):
    text_edit.append(f"<font color='{color}'>{text}</font>")
