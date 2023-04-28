from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My first App")
        button = QPushButton("Press Me!")
        self.setFixedSize(QSize(400, 300))
        # Set the central widget of the Window.
        self.setCentralWidget(button)
        button.setFixedSize(QSize(120, 120))
