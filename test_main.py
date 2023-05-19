from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QApplication


class MyRunnable(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = MySignals()

    def run(self):
        # Perform your task here and obtain the result
        result = [1, 2, 3, 4, 5]
        self.signals.resultReady.emit(result)

class MySignals(QObject):
    resultReady = pyqtSignal(list)

class MainWindow(QObject):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.runnable = MyRunnable()
        self.runnable.signals.resultReady.connect(self.handleResult)

    def startTask(self):
        self.threadpool.start(self.runnable)

    @pyqtSlot(list)
    def handleResult(self, result):
        # Process the result obtained from the worker thread
        print(result)

# Usage example
app = QApplication([])
window = MainWindow()
window.startTask()
app.exec_()
