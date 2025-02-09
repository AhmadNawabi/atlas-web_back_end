#!/usr/bin/env python3
"""
This module provides functionality for interacting with Redis.
It includes decorators for tracking function calls and their history,
a `Cache` class for managing data in Redis, and utility
methods for storing and retrieving data.
"""
import redis
import uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes a single method Callable argument
    and returns a Callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increments the count for that key every time the method
        is called and return the value returned by the original method
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of the method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        The wrapper function is an inner function used within
        the call_history decorator.
        Its primary purpose is to intercept calls to the decorated
        method (e.g., store) and log the inputs and outputs
        of each call into Redis.
        This allows for tracking the history of function calls,
        enabling features like replaying the function's execution history.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> Callable:
    """
    Display the history of calls of a particular function.
    """
    cache = method.__self__  # Get cache instance
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    # Decode inputs and outputs from bytes to strings
    inputs = [input.decode("utf-8") for input in inputs]
    outputs = [output.decode("utf-8") for output in outputs]

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_data}) -> {output_data}")


class Cache:
    """
    A class to interact with Redis and store data with unique keys.
    """

    def __init__(self):
        """
        Initialize the Redis connection and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis and return a unique key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis using the key and optionally
        apply a conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Automatically parametrize Cache.get with the correct
        conversion function to decode bytes to str.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Automatically parametrize Cache.get with the correct
        conversion function to convert bytes to int.
        """
        return self.get(key, fn=int)
