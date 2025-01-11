#!/usr/bin/env python3
"""Import the necessary modules"""
import asyncio
import random


"""
    This asynchronous coroutine that takes in an integer
    arguments(max_delay with a default value of 10)
    named wait_rando that waitss for a random delay between 0 and max_delay
    (included and float valu) second and eventually returns it.

    use the random module
"""


async def wait_random(max_delay: int = 10) -> float:
    """This will generate the random max_delay number"""
    random_delay = random.uniform(0, max_delay)
    """ This pauses the execution for random_wait seconds."""
    await asyncio.sleep(random_delay)
    """returns the random delay"""
    return random_delay
