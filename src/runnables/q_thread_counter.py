from PyQt5.QtCore import QObject, pyqtSignal, QMutex, QMutexLocker


class ThreadCounter(QObject):
    thread_count_changed = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._count = 0
        self.mutex = QMutex()

    @property
    def count(self) -> int:
        return self._count

    def increment(self) -> None:
        mutex_locker = QMutexLocker(self.mutex)
        self._count += 1
        self.thread_count_changed.emit(self._count)

    def decrement(self) -> None:
        mutex_locker = QMutexLocker(self.mutex)
        self._count -= 1
        self.thread_count_changed.emit(self._count)
