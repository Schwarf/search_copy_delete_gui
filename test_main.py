from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication


class SearchRunnable(QRunnable):
    progressUpdated = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        # Long-running search operation
        total_iterations = 1000
        for i in range(total_iterations):
            # Perform search iteration
            # ...

            # Emit progress signal every 100 ms
            if i % 100 == 0:
                self.progressUpdated.emit(i * 100 // total_iterations)

# Usage example
app = QApplication([])
thread_pool = QThreadPool.globalInstance()

def updateProgress(progress):
    # Update UI with progress information
    print(f"Search progress: {progress}%")

runnable = SearchRunnable()
runnable.progressUpdated.connect(updateProgress)
thread_pool.start(runnable)

app.exec_()
