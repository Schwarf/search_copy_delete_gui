import time
import random
from pathlib import Path
from PyQt5.QtCore import QRunnable


class PathSearchRunnable(QRunnable):
    def __init__(self, thread_id):
        super().__init__()
        self._thread_id = thread_id

    def list_paths(self):
        print("List paths")

    def run(self):
        self.list_paths()
        time.sleep(3.0)
        print(f"Thread with id {self._thread_id} is finished")




