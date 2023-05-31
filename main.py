import sys

from PyQt5.QtWidgets import QApplication

from src.q_main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    app.aboutToQuit.connect(main_window.on_exit)
    # Start the event loop.
    app.exec()
