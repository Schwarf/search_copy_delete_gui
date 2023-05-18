from typing import Optional
from PyQt5.QtCore import QSize, pyqtSlot, QThread, QRegExp, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QFormLayout, QVBoxLayout, QBoxLayout, \
    QTextEdit
from PyQt5.QtGui import QRegExpValidator

from q_layout import MainWindowQVLayout
from q_worker_thread import PathSearchThread
from q_runnable import PathSearchRunnable
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    """Main Window"""
    def __init__(self):
        super().__init__()
        self._title = 'Search only'
        self._left = 10
        self._top = 10
        self._width = 1920
        self._height = 1080
        self._worker_thread : Optional[QThread] = None
        start_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\/]+")
        sub_path_regular_expression = QRegExp("[A-Za-z0-9\-\_\*\/]+")
        self._start_path_validator = QRegExpValidator(start_path_regular_expression)
        self._sub_path_validator = QRegExpValidator(sub_path_regular_expression)
        self.init_ui()
        self._max_thread_count = QThreadPool.globalInstance().maxThreadCount()
        self._thread_pool = QThreadPool.globalInstance()
        self._thread_count: int = 0

    def init_ui(self):
        """Window Geometry"""
        widget = QWidget()
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        #label
        # Create textbox
        self._start_path_input = QLineEdit(self)
        self._start_path_input.move(20, 20)
        self._start_path_input.resize(280, 40)
        self._start_path_input.setValidator(self._start_path_validator)
        self._start_path_input.textChanged.connect(self.run_task)

        search_button = QPushButton('Search', self)
        search_button.move(20, 80)
        search_button.clicked.connect(self.on_click)

        self._output_text_box = QTextEdit(self)
        self._output_text_box.move(120, 120)
        self._output_text_box.resize(880, 140)
        self._output_text_box.setReadOnly(True)

        layout = QFormLayout()
        layout.addRow("Provide the default search path here.", self._start_path_input)
        layout.addRow("Search button", search_button)
        layout.addRow("Output", self._output_text_box)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def run_task(self):
        if self._thread_count < self._max_thread_count:
            self._thread_count +=1
            runnable = PathSearchRunnable(self._thread_count)
            self._thread_pool.start(runnable)
    @pyqtSlot()
    def on_click(self):
        """Button Action function"""
        default_value = "So far no files! \n Hallo1 \n Hallo2"
        self._output_text_box.setText(default_value)
        self._output_text_box.append(self._start_path_input.text())
        print(self._start_path_input.text())
