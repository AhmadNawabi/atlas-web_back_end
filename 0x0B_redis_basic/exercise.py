#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Callable


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
