import pathlib
from typing import List

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal


class SignalSearchFinished(QObject):
    search_result_ready = pyqtSignal(list)


class PathSearchRunnable(QRunnable):
    def __init__(self, thread_id: int) -> None:
        super().__init__()
        self._thread_id = thread_id
        self._path = pathlib.Path.home()
        self.signal_search_finished = SignalSearchFinished()

    def list_paths(self):
        return [path for path in self._path.iterdir()]

    def run(self):
        search_list = self.list_paths()
        self.signal_search_finished.search_result_ready.emit(search_list)
        print(f"Thread with id {self._thread_id} is finished")
