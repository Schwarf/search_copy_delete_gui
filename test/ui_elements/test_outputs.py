import pytest
from PyQt5.QtWidgets import QWidget

from ui_elements import inputs


@pytest.fixture()
def parent_widget(qtbot):
    parent_widget = QWidget()
    return parent_widget


