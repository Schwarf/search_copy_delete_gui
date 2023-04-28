from PyQt5.QtWidgets import QVBoxLayout
from typing import List

from q_colors import Color

class MainWindowQVLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self._layout = QVBoxLayout()

    def set_colors(self, colors: List[str]):
        for color in colors:
            self._layout.addWidget(Color(color))

    def get_layout(self):
        return self._layout
