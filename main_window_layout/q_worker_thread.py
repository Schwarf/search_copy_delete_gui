import time

from PyQt5.QtCore import QThread, pyqtSignal


class PathSearchThread(QThread):
    finished = pyqtSignal()
    thread_count : int = 0
    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False


    def run(self):
        self._running = True
        PathSearchThread.thread_count += 1
        while self._running:
            print("Worker thread is running..." + str(PathSearchThread.thread_count))
            time.sleep(1)
        self.finished.emit()

    def stop(self):
        self._running = False