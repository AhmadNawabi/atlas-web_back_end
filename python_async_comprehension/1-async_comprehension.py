#!/usr/bin/env python3
"""import asyncio module from library"""
import asyncio

"""import async_generator form other file"""
async_generator = __import__('0-async_generator').async_generator

"""
Import async_generator from the previous
task and then write a coroutine called
async_comprehension that takes no arguments.

The coroutine will collect 10 random numbers
using an async comprehensing over async_generator,
then return the 10 random numbers.
"""


async def async_comprehension():
    """The coroutine will collect 10 random numbers
    using an async comprehensing over async_generator,"""
    result = [i async for i in async_generator()]
    """return the 10 random numbers"""
    return result
