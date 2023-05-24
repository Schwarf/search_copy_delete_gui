from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton

app = QApplication([])
# Create the main widget
widget = QWidget()

# Create a QVBoxLayout to hold the contents
layout = QVBoxLayout(widget)

# Create a QFormLayout to be placed within the QVBoxLayout
form_layout = QFormLayout()

# Add widgets to the QFormLayout
label1 = QLabel("Label 1")
line_edit1 = QLineEdit()
form_layout.addRow(label1, line_edit1)

label2 = QLabel("Label 2")
line_edit2 = QLineEdit()
form_layout.addRow(label2, line_edit2)

# Add the QFormLayout to the QVBoxLayout
layout.addLayout(form_layout)

# Add additional widgets to the QVBoxLayout
button = QPushButton("Submit")
layout.addWidget(button)

# Set the main widget as the central widget of the application

widget.show()
app.exec_()
