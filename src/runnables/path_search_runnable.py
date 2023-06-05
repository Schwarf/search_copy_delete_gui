import pathlib
from typing import List, Generator, Callable, Optional

from PyQt5.QtCore import QObject, pyqtSignal

from runnables.runnable_interface import RunnableInterface
from runnables.thread_counter import ThreadCounter


class SearchSignalHelper(QObject):
    search_result_ready = pyqtSignal(bool, list)
    search_still_ongoing = pyqtSignal()


class PathSearchRunnable(RunnableInterface):
    def __init__(self) -> None:
        super().__init__()
        self._thread_counter: ThreadCounter = None
        self._ignore_hidden_files: bool = None
        self._path = pathlib.Path.home()
        self._folder_file_pattern: str = None
        self._show_files_in_path: bool = False
        self.search_signal_helper = SearchSignalHelper()
        self._maximum_items = 5000
        self._is_running = True

    def set_path(self, path: str) -> None:
        self._path = pathlib.Path(path)

    def set_folder_file_pattern(self, folder_file_pattern: str) -> None:
        self._folder_file_pattern = folder_file_pattern

    def set_ignore_files(self, ignore_files: bool) -> None:
        self._ignore_hidden_files = ignore_files

    def set_show_files_in_path(self, show_files: bool) -> None:
        self._show_files_in_path = show_files

    def _perform_search(self, path_generator: Generator[pathlib.Path, None, None],
                        filter_function: Callable[[pathlib.Path], bool]) -> Optional[List[pathlib.Path]]:
        path_list = []
        number_of_files_to_emit_ongoing_search_event = 1000
        if not self._path.exists():
            return None
        item_match_counter = 0
        item_counter = 0
        while self._is_running and item_match_counter < self._maximum_items:
            item_counter += 1
            if item_counter % number_of_files_to_emit_ongoing_search_event == 0:
                self.search_signal_helper.search_still_ongoing.emit()
            try:
                path = next(path_generator)
                if filter_function is None:
                    path_list.append(path)
                    item_match_counter += 1
                elif filter_function(path):
                    path_list.append(path)
                    item_match_counter += 1
            except StopIteration:
                break
        return path_list

    @staticmethod
    def is_not_hidden(path: pathlib.Path) -> bool:
        return not path.name.startswith(".")

    @staticmethod
    def is_directory(path: pathlib.Path) -> bool:
        return path.is_dir()

    def run(self) -> None:
        self._thread_counter.increment()
        path_generator = self._path.iterdir()
        filter_function = self.is_directory
        if self._show_files_in_path:
            filter_function = None
        if self._folder_file_pattern:
            path_generator = self._path.rglob(self._folder_file_pattern)
            filter_function = None
        if self._ignore_hidden_files:
            if filter_function is None:
                filter_function = self.is_not_hidden
            else:
                filter_function = lambda path: self.is_directory(path) and self.is_not_hidden(path)

        search_list = self._perform_search(path_generator, filter_function)
        if search_list is None:
            self.search_signal_helper.search_result_ready.emit(False, [])
        else:
            self.search_signal_helper.search_result_ready.emit(True, search_list)
        self._thread_counter.decrement()

    def stop(self) -> None:
        self._is_running = False

    def set_thread_counter(self, thread_counter: ThreadCounter) -> None:
        self._thread_counter = thread_counter
