from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget


@pyqtSlot()
def open_copy_dialog_window() -> QWidget:
    copy_dialog_window = QWidget()
    copy_dialog_window.setWindowTitle("Copy dialog")
    copy_dialog_window.setGeometry(200, 200, 300, 200)
    copy_dialog_window.activateWindow()
    copy_dialog_window.show()
    return copy_dialog_window
