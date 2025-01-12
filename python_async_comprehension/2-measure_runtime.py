#!/usr/bin/env python3
"""import necessary modules from library"""
import asyncio
import typing
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension
"""
Import async_comprehension from the previous
file and write a measure_runtime coroutine
that will execute async_comprehension four times
in parallel using asyncio.gather.

measure_runtime should measure the total runtime
and return it.

Notice that the total runtime is roughly 10 seconds,
explain it to yourself.
"""


async def measure_runtime() -> typing.List[float]:
    """record the start time"""
    start = time.time()
    """measure_runtime coroutine
    that will execute async_comprehension four times
    in parallel using asyncio.gather"""
    await asyncio.gather(async_comprehension())
    """record the end time"""
    end = time.time()
    """return the total runtime"""
    return (end - start)
