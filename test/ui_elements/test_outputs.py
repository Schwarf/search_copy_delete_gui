import pytest
from PyQt5.QtWidgets import QWidget


@pytest.fixture()
def parent_widget(qtbot):
    parent_widget = QWidget()
    return parent_widget


