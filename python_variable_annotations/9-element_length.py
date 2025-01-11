#!/usr/bin/env python3
"""Import the typing module"""
import typing


"""
    Annotate the below function’s parameters
    and return values with the appropriate types
"""


def element_length(
        lst: typing.Iterable[typing.Sequence]
) -> typing.List[typing.Tuple[typing.Sequence, int]]:
    """Returns appropriate types"""
    return [(i, len(i)) for i in lst]
