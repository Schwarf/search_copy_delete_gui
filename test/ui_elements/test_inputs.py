import pytest
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QCheckBox, QPushButton

from main_window import inputs


@pytest.fixture()
def parent_widget(qtbot):
    parent_widget = QWidget()
    return parent_widget


class SlotHelper:
    def __init__(self):
        self.slot_function_called = False

    def slot_function(self):
        self.slot_function_called = True


class TestInputs:
    def test_folder_file_pattern_setup(self, parent_widget):
        validator = QRegExpValidator()

        folder_file_text_box = inputs.folder_file_pattern_setup(parent_widget, validator)
        assert isinstance(folder_file_text_box, QLineEdit)
        assert folder_file_text_box.parentWidget() == parent_widget
        assert folder_file_text_box.validator() == validator

    def test_default_search_path_setup(self, parent_widget):
        validator = QRegExpValidator()
        slot_helper = SlotHelper()
        default_search_path_text_box = inputs.default_search_path_setup(parent_widget, validator,
                                                                        slot_helper.slot_function)
        assert isinstance(default_search_path_text_box, QLineEdit)
        assert default_search_path_text_box.parentWidget() == parent_widget
        assert default_search_path_text_box.validator() == validator
        assert slot_helper.slot_function_called is False
        default_search_path_text_box.textChanged.emit("test")
        assert slot_helper.slot_function_called is True

    def test_setup_ignore_hidden_files_check_box(self, parent_widget):
        slot_helper = SlotHelper()
        ignore_hidden_files_check_box = inputs.ignore_hidden_files_check_box_setup(parent_widget,
                                                                                   slot_helper.slot_function)
        assert isinstance(ignore_hidden_files_check_box, QCheckBox)
        assert ignore_hidden_files_check_box.parentWidget() == parent_widget
        assert slot_helper.slot_function_called is False
        ignore_hidden_files_check_box.clicked.emit()
        assert slot_helper.slot_function_called is True

    def test_setup_show_files_default_search_path_check_box(self, parent_widget):
        slot_helper = SlotHelper()
        show_files_default_search_path_check_box = \
            inputs.show_files_default_search_path_check_box_setup(parent_widget, slot_helper.slot_function)
        assert isinstance(show_files_default_search_path_check_box, QCheckBox)
        assert show_files_default_search_path_check_box.parentWidget() == parent_widget
        assert slot_helper.slot_function_called is False
        show_files_default_search_path_check_box.clicked.emit()
        assert slot_helper.slot_function_called is True

    def test_search_button_setup(self, parent_widget):
        slot_helper = SlotHelper()
        search_button = inputs.search_button_setup(parent_widget, slot_helper.slot_function)
        assert isinstance(search_button, QPushButton)
        assert search_button.parentWidget() == parent_widget
        assert slot_helper.slot_function_called is False
        search_button.clicked.emit()
        assert slot_helper.slot_function_called is True

    def test_exit_button_setup(self, parent_widget):
        slot_helper = SlotHelper()
        exit_button = inputs.exit_button_setup(parent_widget, slot_helper.slot_function)
        assert isinstance(exit_button, QPushButton)
        assert exit_button.parentWidget() == parent_widget
        assert slot_helper.slot_function_called is False
        exit_button.clicked.emit()
        assert slot_helper.slot_function_called is True
