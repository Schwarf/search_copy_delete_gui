import pytest
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit

from ui_elements import inputs
from runnables.q_path_search_runnable import PathSearchRunnable

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

    def test_default_search_path_setup(self,monkeypatch, parent_widget):
        validator = QRegExpValidator()
        slot_function_called = False
        def mock_slot_function():
            nonlocal slot_function_called
            slot_function_called = True
        monkeypatch.setattr(PathSearchRunnable,"run_search", mock_slot_function)

        default_search_path_text_box = inputs.default_search_path_setup(parent_widget, validator, mock_slot_function)
        assert isinstance(default_search_path_text_box, QLineEdit)
        assert default_search_path_text_box.parentWidget() == parent_widget
        assert default_search_path_text_box.validator() == validator
        default_search_path_text_box.textChanged.emit("test")
        assert slot_function_called is True
