#!/usr/bin/env python3
"""
Function named index_range that takes two
integer arguments page and page_size
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    return a tuple of size two containing a
    start index and an end index corresponding
    to the range of indexes to return in a list
    for those particular pagination parameters
    """
    start_index = page_size * (page - 1)
    end_index = page_size * page

    return (start_index, end_index)
