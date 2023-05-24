import itertools
import pathlib
from typing import List, Generator, Callable

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
        self.ignore_hidden_files = ignore_hidden_files
        if path is None:
            self._path = pathlib.Path.home()
        else:
            self._path = pathlib.Path(path)
        self._file_pattern = pattern
        self.signal_search_finished = SignalSearchFinished()
        self._maximum_items = 5000
        self._is_running = True

    def _perform_search(self, path_generator: Generator[pathlib.Path, None, None],
                        filter_function: Callable[[pathlib.Path], bool]) -> List[pathlib.Path]:
        path_list = []
        if not self._path.exists():
            return path_list
        counter = 0
        while self._is_running and counter < self._maximum_items:
            try:
                path = next(path_generator)
                if filter_function(path):
                    path_list.append(path)
                    counter += 1
            except StopIteration:
                break
        return path_list

    def _ignore_hidden_files(self, path: pathlib.Path) -> bool:
        return not path.name.startswith(".")

    def _is_file(self, path: pathlib.Path) -> bool:
        return path.is_file()

    def _is_directory(self, path: pathlib.Path) -> bool:
        return path.is_dir()

    def list_directory_paths(self) -> List[pathlib.Path]:
        path_list = []
        if not self._path.exists():
            return path_list
        if self.ignore_hidden_files:
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
        if self.ignore_hidden_files:
            file_path_list = [path for path in
                              itertools.islice(self._path.rglob(self._file_pattern), self._maximum_items) if
                              path.is_file() and not path.name.startswith(".")]
        else:
            file_path_list = [path for path in
                              itertools.islice(self._path.rglob(self._file_pattern), self._maximum_items) if
                              path.is_file()]
        return file_path_list

    def folder_generator(self, directory: pathlib.Path):
        return directory.iterdir()

    def file_generator(self, file: pathlib.Path, pattern: str):
        return file.rglob(pattern)

    def run(self) -> None:
        self._thread_counter.increment()
        generator = self.folder_generator(self._path)
        filter_function = self._is_directory
        if self._file_pattern:
            generator = self.file_generator(self._path, self._file_pattern)
            filter_function = self._is_file

        if self.ignore_hidden_files:
            filter_function = filter_function and self._ignore_hidden_files

        search_list = self._perform_search(generator, filter_function)
        self.signal_search_finished.search_result_ready.emit(search_list)
        self._thread_counter.decrement()
