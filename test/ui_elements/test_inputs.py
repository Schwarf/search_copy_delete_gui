import pytest
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit

from ui_elements import inputs


@pytest.fixture()
def parent_widget(qtbot):
    parent_widget = QWidget()
    return parent_widget


class TestInputs:
    def test_folder_file_pattern_setup(self, parent_widget):
        validator = QRegExpValidator()

        folder_file_text_box = inputs.folder_file_pattern_setup(parent_widget, validator)
        assert isinstance(folder_file_text_box, QLineEdit)
        assert folder_file_text_box.parentWidget() == parent_widget
        assert folder_file_text_box.validator() == validator
