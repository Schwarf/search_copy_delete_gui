
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
#from main_window_layout.q_main_window import MainWindow
from untitled import Ui_MainWindow
#from main_window_layout.q_resizeable_widget import ResizableLabel
from PyQt5 import QtWidgets
import sys
"""
class Test(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QGridLayout(self)

        for row in range(3):
            for column in range(3):
                if (row, column) == (1, 1):
                    continue
                layout.addWidget(QtWidgets.QPushButton(), row, column)

        label = ResizableLabel()
        layout.addWidget(label, 1, 1)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Test()
    w.show()
    sys.exit(app.exec_())

"""
app = QApplication(sys.argv)
window = uic.loadUi('untitled.ui')
window.show()
# Start the event loop.
app.exec()