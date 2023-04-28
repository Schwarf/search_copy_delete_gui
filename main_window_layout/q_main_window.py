from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget

from q_layout import MainWindowQVLayout

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first App")
        button = QPushButton("Press Me!")
        self.setFixedSize(QSize(400, 300))
        layout = MainWindowQVLayout()
        layout.set_colors(['red', 'blue', 'green'])
        widget = QWidget()
        # Set the central widget of the Window.
        widget.setLayout(layout.get_layout())
        self.setCentralWidget(widget)
        button.setFixedSize(QSize(120, 120))


