#!/usr/bin/env python3
"""import async, typing and time modules"""
import asyncio
import typing
import time

"""Import the previos taks wait_n"""
wait_n = __import__('1-concurrent_coroutines').wait_n
"""
    Create a measure_time function with integers
    n and max_delay as arguments that measures the
    total execution time for wait_n(n, max_delay),
    and returns total_time / n.
    Your function should return a float.
Use the time module to measure an approximate elapsed time.
"""


async def measure_time(n: int, max_delay: int) -> float:
    """record the starting time"""
    start_time = time.time()
    """Execute wait_n and await its result"""
    await wait_n(n, max_delay)
    """record the end time"""
    end_time = time.time()

    """subtract end time from starting time"""
    total_time = end_time - start_time
    """return the total time devided by n"""
    return total_time / n
