#!/usr/bin/env python3
"""Import asyncio and typing from the library."""
import asyncio
from typing import List
"""Import wait_random from the previous file."""
task_wait_random = __import__('0-basic_async_syntax').wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Alter wait_n to use task_wait_random"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    result = [await task for task in asyncio.as_completed(tasks)]
    return sorted(result)
