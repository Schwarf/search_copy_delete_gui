import pathlib

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
        self._destination_path = None
        self._origin_folder = None

    def set_destination_path(self, destination_path: str) -> None:
        self._destination_path = pathlib.Path(destination_path)

    def set_origin_folder(self, origin_folder: str) -> None:
        self._origin_folder = pathlib.Path(origin_folder)

