#!/usr/bin/env python3
"""import asyncio, typing, heapq from library"""
import asyncio
"""import wait_random from previos file"""
wait_random = __import__('0-basic_async_syntax').wait_random


"""
    Import wait_random from the previous python
    file that you’ve written and write an async
    routine called wait_n that takes in 2 int arguments
    (in this order): n and max_delay. You will spawn
    wait_random n times with the specified max_delay.

wait_n should return the list of all the delays (float values).
The list of the delays should be in ascending order without
using sort() because of concurrency.
"""


async def wait_n(n: int, max_delay: int) -> list[float]:
    """store wait_random and max_delay in task variable"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    """spawn wait_random n times with the specified max_delay."""
    results = []

    """    Returns:
        list[float]: A list of all the delays (float values)
        in ascending order.
        The list is sorted by collecting results as they complete,
        without using the `sort()` method."""
    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)
    return results
