from typing import Optional
from PyQt5.QtCore import QSize, pyqtSlot, QThread, QRegExp, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit
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
        reg_ex = QRegExp("[A-Za-z0-9\-\_\*\/]+")
        self._input_validator = QRegExpValidator(reg_ex)
        self.init_ui()
        self._max_thread_count = QThreadPool.globalInstance().maxThreadCount()
        self._thread_pool = QThreadPool.globalInstance()
        self._thread_count: int = 0

    def start_worker_thread(self, text):
        if self._worker_thread is not None:
            self._worker_thread.stop()
            self._worker_thread.wait()
        self._worker_thread = PathSearchThread(self)
        self._worker_thread.finished.connect(self.worker_thread_finished)
        self._worker_thread.start()

    def worker_thread_finished(self):
        self._worker_thread = None

    def init_ui(self):
        """Window Geometry"""
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)
        #label
        # Create textbox
        self.path_input_text_box = QLineEdit(self)
        self.path_input_text_box.move(20, 20)
        self.path_input_text_box.resize(280, 40)
        self.path_input_text_box.setValidator(self._input_validator)
        # HERE we USE q_worker_thread
        #self.path_input_text_box.textChanged.connect(self.start_worker_thread)
        # HERE we USE q_runnable
        self.path_input_text_box.textChanged.connect(self.run_task)
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

    def run_task(self):
        if self._thread_count < self._max_thread_count:
            self._thread_count +=1
            runnable = PathSearchRunnable(self._thread_count)
            self._thread_pool.start(runnable)
    @pyqtSlot()
    def on_click(self):
        """Button Action function"""
        default_value = "So far no files!"
        self.output_text_box.setText(default_value)
        print(self.path_input_text_box.text())
