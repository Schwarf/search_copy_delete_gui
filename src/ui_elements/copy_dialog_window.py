from typing import Dict, Any

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QFormLayout, QLineEdit


@pyqtSlot()
def open_copy_dialog_window(input: Dict[str, Any]) -> QWidget:
    copy_dialog_window = QWidget()
    copy_dialog_window.setWindowTitle("Copy dialog")
    copy_dialog_window.setGeometry(200, 200, 1000, 200)
    copy_dialog_window.activateWindow()

    outer_layout = QFormLayout()
    default_copy_path = QLineEdit(copy_dialog_window)
    default_copy_path.setText(input["SearchPathInput"])
    default_copy_path.setValidator(input["StartPathValidator"])
    outer_layout.addRow("Provide the default copy path here.", default_copy_path)

    folder_file_pattern = QLineEdit(copy_dialog_window)
    folder_file_pattern.setText(input["FolderFilePattern"])
    folder_file_pattern.setValidator(input["FolderFileValidator"])

    outer_layout.addRow("Folder/file pattern",folder_file_pattern)
    copy_dialog_window.setLayout(outer_layout)
    copy_dialog_window.show()
    return copy_dialog_window
