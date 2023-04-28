from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QColor
class MainWindowQVLayout(QVBoxLayout)
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()
        self._layout.addWidget(QColor())

    def get_layout(self):


