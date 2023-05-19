import pathlib
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal


class SignalSearchFinished(QObject):
    search_result_ready = pyqtSignal(list)


class PathSearchRunnable(QRunnable):
    def __init__(self, thread_id: int, path: str = None) -> None:
        super().__init__()
        self._thread_id = thread_id
        self._is_running = True
        if path is None:
            self._path = pathlib.Path.home()
        else:
            self._path = pathlib.Path(path)
        self.signal_search_finished = SignalSearchFinished()

    def list_paths(self):
        self._is_running = False
        if not self._path.exists():
            return []
        path_list = [path for path in self._path.iterdir()]

        return path_list

    def run(self):
        while self._is_running:
            search_list = self.list_paths()
            if not search_list:
                self.signal_search_finished.search_result_ready.emit(["Path is not valid!"])
            self.signal_search_finished.search_result_ready.emit(search_list)
        print(f"Thread with id {self._thread_id} is finished")
