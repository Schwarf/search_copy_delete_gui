import pathlib
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QMutex, QMutexLocker


class SignalSearchFinished(QObject):
    search_result_ready = pyqtSignal(list)


class ThreadCounter(QObject):
    thread_count_changed = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self._count = 0
        self.mutex = QMutex()

    @property
    def count(self):
        return self._count
    def increment(self):
        mutex_locker = QMutexLocker(self.mutex)
        self._count += 1
        self.thread_count_changed.emit(self._count)

    def decrement(self):
        mutex_locker = QMutexLocker(self.mutex)
        self._count -= 1
        self.thread_count_changed.emit(self._count)

class PathSearchRunnable(QRunnable):
    def __init__(self, thread_counter: ThreadCounter, path: str = None) -> None:
        super().__init__()
        self._is_running = True
        self._thread_counter = thread_counter
        if path is None:
            self._path = pathlib.Path.home()
        else:
            self._path = pathlib.Path(path)
        self.signal_search_finished = SignalSearchFinished()

    @property
    def is_running(self):
        return self._is_running

    def list_paths(self):
        self._is_running = False
        if not self._path.exists():
            return []
        path_list = [path for path in self._path.iterdir()]

        return path_list

    def run(self):
        self._thread_counter.increment()
        search_list = self.list_paths()
        if not search_list:
            self.signal_search_finished.search_result_ready.emit(["Path is not valid!"])
        self.signal_search_finished.search_result_ready.emit(search_list)
        self._thread_counter.decrement()