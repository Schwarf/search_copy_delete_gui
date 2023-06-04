from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow


def create_button_with_lambda(parent, text, lambda_func):
    button = QPushButton(text, parent)
    button.clicked.connect(lambda: lambda_func())
    return button

# Example usage
app = QApplication([])
window = QMainWindow()

button_text = "Click Me"
button_function = lambda: print("Button clicked!")

button = create_button_with_lambda(window, button_text, button_function)
button.show()

app.exec_()
