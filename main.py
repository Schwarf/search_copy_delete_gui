
from PyQt5.QtWidgets import QApplication
from main_window_layout.q_main_window import MainWindow
import sys

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.


# Start the event loop.
app.exec()