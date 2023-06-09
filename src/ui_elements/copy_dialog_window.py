from typing import Dict, Any

from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QFormLayout, QLineEdit, QPushButton


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

    folder_file_pattern = QLineEdit(copy_dialog_window)
    folder_file_pattern.setText(input["FolderFilePattern"])
    folder_file_pattern.setValidator(input["FolderFileValidator"])

    destination_folder = QLineEdit(copy_dialog_window)
    destination_folder.setValidator(input["StartPathValidator"])

    copy_button = QPushButton('Copy', copy_dialog_window)
    copy_button.clicked.connect(input["CopyRunnable"])

    outer_layout.addRow("Folder/file pattern",folder_file_pattern)
    outer_layout.addRow("Provide the default copy path here.", default_copy_path)
    outer_layout.addRow("Provide the destintaion folder here.", destination_folder)
    outer_layout.addRow("Press to copy:", copy_button)
    copy_dialog_window.setLayout(outer_layout)
    copy_dialog_window.show()
    return copy_dialog_window
