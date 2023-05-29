import pathlib
from typing import List, Generator, Callable

from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from runnables.q_runnable_interface import RunnableInterface
from runnables.q_thread_counter import ThreadCounter


class SearchSignalHelper(QObject):
    search_result_ready = pyqtSignal(list)
    search_update = pyqtSignal()

class PathSearchRunnable(RunnableInterface):
    def __init__(self, path: str = None, pattern: str = None,
                 ignore_hidden_files: bool = True) -> None:
        super().__init__()
        self._thread_counter: ThreadCounter = None

        self.ignore_hidden_files = ignore_hidden_files
        if path is None:
            self._path = pathlib.Path.home()
        else:
            self._path = pathlib.Path(path)
        self._file_pattern = pattern
        self.search_signal_helper = SearchSignalHelper()
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
            if counter % 1000 == 0:
                self.search_signal_helper.search_update.emit()
        return path_list

    def _ignore_hidden_files(self, path: pathlib.Path) -> bool:
        return not path.name.startswith(".")

    def _is_file(self, path: pathlib.Path) -> bool:
        return path.is_file()

    def _is_directory(self, path: pathlib.Path) -> bool:
        return path.is_dir()

    def run(self) -> None:
        self._thread_counter.increment()
        path_generator = self._path.iterdir()
        filter_function = self._is_directory
        if self._file_pattern:
            path_generator = self._path.rglob(self._file_pattern)
            filter_function = self._is_file

        if self.ignore_hidden_files:
            filter_function = filter_function and self._ignore_hidden_files

        search_list = self._perform_search(path_generator, filter_function)
        self.search_signal_helper.search_result_ready.emit(search_list)
        self._thread_counter.decrement()

    def stop(self) -> None:
        self._is_running = False

    def set_thread_counter(self, thread_counter: ThreadCounter) -> None:
        self._thread_counter = thread_counter
