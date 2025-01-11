#!/usr/bin/env python3
"""Import typing module from library"""
import typing

"""
    function to_kv that takes a string k and an int
    OR float v as arguments and returns a tuple.
    The first element of the tuple is the string k.
    The second element is the square of the int/float v
    and should be annotated as a float.
"""


def to_kv(k: str, v: typing.Union[int, float]) -> typing.Tuple[str, float]:
    """Returns eturns a tuple."""
    return (k, v)
