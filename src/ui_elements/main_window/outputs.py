from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QTableWidget, QHeaderView, QTableWidgetItem


def initialize_read_only_qline_edit(parent) -> QLineEdit:
    qline_edit = QLineEdit(parent)
    qline_edit.setReadOnly(True)
    qline_edit.setText("---")
    return qline_edit


def output_table(parent) -> QTableWidget:
    table = QTableWidget(parent)
    table.setColumnCount(2)
    # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    # self.table.setColumnWidth(0, 1500)
    table.verticalHeader().hide()
    table.setShowGrid(False)
    table.verticalHeader().setDefaultSectionSize(2)
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
    table.setHorizontalHeaderLabels(["Path", "Size"])
    return table


def add_one_signal_item_table(text: str, table: QTableWidget):
    table.setRowCount(1)
    item = QTableWidgetItem(text)
    item.setForeground(Qt.red)
    table.setItem(0, 0, item)