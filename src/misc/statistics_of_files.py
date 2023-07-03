import pathlib
from typing import Dict

from dictionary_string_keys import *


# We assume that the existence of the files has already been established
class StatisticsOfFiles:
    def __init__(self) -> None:
        self._smallest_file_size = -1
        self._largest_file_size = -1
        self._size_of_all_files = -1
        self._number_of_files = None
        self._is_valid = False

    def add_file_and_return_size(self, path: pathlib.Path) -> None:
        size = path.stat().st_size
        self._is_valid = True
        if self._number_of_files is None:
            self._smallest_file_size = size
            self._largest_file_size = size
            self._size_of_all_files = size
            self._number_of_files = 1
        else:
            self._smallest_file_size = min(self._smallest_file_size, size)
            self._largest_file_size = max(self._largest_file_size, size)
            self._size_of_all_files += size
            self._number_of_files += 1
        return size

    def is_valid(self):
        return self._is_valid

    def get_statistics(self) -> Dict[str, int]:
        if self._number_of_files is None:
            return {}
        return {SMALLEST_FILE: self._smallest_file_size, LARGEST_FILE: self._largest_file_size, FILE_COUNT:
            self._number_of_files, SUM_OF_FILE_SIZES: self._size_of_all_files}
