#!/usr/bin/env python3
"""import typing module from library"""
import typing

"""
   function make_multiplier that takes a float
    multiplier as argument and returns a
   function that multiplies a float by multiplier.
"""


def make_multiplier(multiplier: float) -> typing.Callable[[float], float]:
    """Returns and mutiplies by multiplier"""
    return lambda x: x * multiplier
