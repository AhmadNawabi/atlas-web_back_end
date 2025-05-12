#!/usr/bin/env python3
"""
a method named get_page that takes two integer arguments page with
default value 1 and page_size with default value 10
"""
import csv
import math
from typing import List, Tuple


class Server:
    """
    Server class to paginate a database of popular baby names
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Constructor"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieve a specific page from the dataset"""
        assert (type(page_size) == int and type(page) == int)
        assert (page > 0 and page_size > 0)
        start_index, end_index = self.index_range(page, page_size)
        return self.dataset()[start_index:end_index]

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """
            Return a tuple of size two containing a start index
            and an end index corresponding to the range of indexes
            to return in a list for those particular pagination
            parameters
        """
        start_index = page_size * (page - 1)
        end_index = page_size * page

        return (start_index, end_index)
