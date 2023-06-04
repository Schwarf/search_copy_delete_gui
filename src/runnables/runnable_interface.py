from PyQt5.QtCore import QRunnable

from thread_counter import ThreadCounter


class RunnableInterface(QRunnable):
    def stop(self) -> None:
        pass

    def set_thread_counter(self, thread_counter: ThreadCounter) -> None:
        pass
