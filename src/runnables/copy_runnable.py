import pathlib
from typing import List, Generator, Callable, Optional

from PyQt5.QtCore import QObject, pyqtSignal

from runnables.runnable_interface import RunnableInterface
from runnables.thread_counter import ThreadCounter


class CopySignalHelper(QObject):
    copy_finished = pyqtSignal()
    copy_process_still_ongoing = pyqtSignal()


class CopyRunnable(RunnableInterface):
    def __init__(self) -> None:
        super().__init__()
        self._thread_counter: ThreadCounter = None
        self._ignore_hidden_files: bool = None
        self._path = pathlib.Path.home()
        self._folder_file_pattern: str = None
        self._show_files_in_path: bool = False
        self.copy_helper = CopySignalHelper()
        self._maximum_items = 5000
        self._is_running = True
