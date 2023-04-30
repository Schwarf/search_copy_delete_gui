from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit

from q_layout import MainWindowQVLayout

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self):
        super().__init__()
        self.title = 'Search only'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080
        self.init_ui()
    def init_ui(self):
        """Window Geometry"""
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #label
        # Create textbox
        self.path_input_text_box = QLineEdit(self)
        self.path_input_text_box.move(20, 20)
        self.path_input_text_box.resize(280, 40)
        # Create a button in the window
        self.button = QPushButton('Search', self)
        self.button.move(20, 80)
        #Print affected Rows
        self.output_text_box = QLineEdit(self)
        self.output_text_box.move(120, 120)
        self.output_text_box.resize(880, 140)
        self.output_text_box.setReadOnly(True)
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        """Button Action function"""
        default_value = "So far no files!"
        self.output_text_box.setText(default_value)
        print(self.path_input_text_box.text())
