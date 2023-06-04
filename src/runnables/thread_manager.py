from PyQt5.QtCore import QObject, QThreadPool

from runnable_interface import RunnableInterface
from thread_counter import ThreadCounter


class ThreadManager(QObject):
    def __init__(self) -> None:
        super().__init__()
        self._max_thread_count = QThreadPool.globalInstance().maxThreadCount() / 2
        self._thread_pool = QThreadPool.globalInstance()
        self._thread_counter = ThreadCounter()
        self._thread_counter.thread_count_changed.connect(lambda count: print("Thread count is: ", count))

    def start_runnable(self, runnable: RunnableInterface = None) -> None:
        if not runnable:
            raise ValueError("Runnable is None")
        runnable.set_thread_counter(self._thread_counter)
        if self._thread_counter.count < self._max_thread_count:
            self._thread_pool.start(runnable)

    def stop_all_runnables(self) -> None:
        self._thread_pool.waitForDone()
