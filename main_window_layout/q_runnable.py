import time
import random

from PyQt5.QtCore import QRunnable


class PathSearchRunnable(QRunnable):
    def __init__(self, thread_id):
        super().__init__()
        self._thread_id = thread_id

    def run(self):
        for i in range(5):
            print(f"Working on thread with id {self._thread_id}")
            time.sleep(random.randint(700, 2500)/1000)



