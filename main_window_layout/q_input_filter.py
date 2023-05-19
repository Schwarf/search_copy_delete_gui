from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class InputTimeFilter(QObject):
    input_finished =  pyqtSignal()

    def __init__(self, target_widget):
        super.__init__()
        self._target_widget = target_widget
        self._timer = QTimer()
        self._timer.setInterval(200)
        self._timer.setSingleShot(True)

    def eventFilter(self, object, event):
        if object == self._target_widget and event.type() == event.KeyPress:
            self._timer.start()
        return super().eventFilter(object, event)
