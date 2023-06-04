from PyQt5.QtWidgets import QDialog


def open_copy_dialog_window(parent) -> QDialog:
    copy_dialog_window = QDialog(parent)
    copy_dialog_window.setWindowTitle("Copy dialog")
    copy_dialog_window.setGeometry(200, 200, 300, 200)
    copy_dialog_window.activateWindow()
    copy_dialog_window.show()
    return copy_dialog_window
