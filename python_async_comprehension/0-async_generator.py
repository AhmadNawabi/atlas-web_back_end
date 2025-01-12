#!/usr/bin/env python3
"""import asyncio, random and typing mudoles"""
import random
import asyncio
import typing

"""
Write a coroutine called async_generator
that takes no arguments.

The coroutine will loop 10 times,
each time asynchronously wait 1 second,
then yield a random number between 0 and 10.
Use the random module.
"""


async def async_generator() -> typing.Generator[float, None, None]:
    """The coroutine will loop 10 times"""
    for i in range(10):
        """each time asynchronously wait 1 sec"""
        await asyncio.sleep(1)
        """then yield a random numbre between 0 and 10"""
        yield random.uniform(0, 10)
