#!/usr/bin/env python3
"""import typing module from library"""
import typing


"""This function takes a list mxd_lst of integers and floats"""


def sum_mixed_list(mxd_lst: typing.List[typing.Union[int, float]]) -> float:
    """Return their sum as floats"""
    return sum(mxd_lst)
