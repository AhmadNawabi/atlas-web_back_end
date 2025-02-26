#!/usr/bin/env python3
"""Import asyncio and typing from the library."""
import asyncio
import typing
"""Import wait_random from the previous file."""
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> typing.List[float]:
    """
    Spawns `wait_random` `n` times with the specified `max_delay`.

    Args:
        n (int): The number of times to spawn `wait_random`.
        max_delay (int): The maximum delay value to pass to `wait_random`.

    Returns:
        typing.List[float]: A list of all the delays (float values)
          in ascending order,
                            without using the `sort()` method.
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = []

    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)

    return results
