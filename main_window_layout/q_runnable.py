import itertools
import pathlib
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QMutex, QMutexLocker


class SignalSearchFinished(QObject):
    search_result_ready = pyqtSignal(list)


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


class PathSearchRunnable(QRunnable):
    def __init__(self, thread_counter: ThreadCounter, path: str = None, pattern: str = None,
                 ignore_hidden_files: bool = True) -> None:
        super().__init__()
        self._thread_counter = thread_counter
        self._ignore_hidden_files = ignore_hidden_files
        if path is None:
            self._path = pathlib.Path.home()
        else:
            self._path = pathlib.Path(path)
        self._pattern = pattern
        self.signal_search_finished = SignalSearchFinished()
        self._maximum_items = 5000

    def list_directory_paths(self) -> List[pathlib.Path]:
        path_list = []
        if not self._path.exists():
            return path_list
        if self._ignore_hidden_files:
            path_list = [path for path in itertools.islice(self._path.iterdir(), self._maximum_items) if
                         path.is_dir() and not path.name.startswith(".")]
        else:
            path_list = [path for path in itertools.islice(self._path.iterdir(), self._maximum_items) if
                         path.is_dir()]
        return path_list

    def list_file_paths(self) -> List[pathlib.Path]:
        file_path_list = []
        if not self._path.exists():
            return file_path_list
        if self._ignore_hidden_files:
            file_path_list = [path for path in itertools.islice(self._path.rglob(self._pattern), self._maximum_items) if
                          path.is_file() and not path.name.startswith(".")]
        else:
            file_path_list = [path for path in itertools.islice(self._path.rglob(self._pattern), self._maximum_items) if
                              path.is_file()]
        return file_path_list

    def run(self) -> None:
        self._thread_counter.increment()
        if self._pattern is None:
            search_list = self.list_directory_paths()
        else:
            search_list = self.list_file_paths()
        if not search_list:
            self.signal_search_finished.search_result_ready.emit([])
        self.signal_search_finished.search_result_ready.emit(search_list)
        self._thread_counter.decrement()
