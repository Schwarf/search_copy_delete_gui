import time

from PyQt5.QtCore import QThread, pyqtSignal, QRegExp


class PathSearchThread(QThread):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False


    def run(self):
        self._running = True
        while self._running:
            print("Worker thread is running...")
            time.sleep(1)
        self.finished.emit()

    def stop(self):
        self._running = False