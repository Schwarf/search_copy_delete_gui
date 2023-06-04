from PyQt5.QtWidgets import QDialog


def open_copy_dialog_window(parent):
    copy_dialog_window = QDialog(parent)
    copy_dialog_window.setWindowTitle("Copy dialog")