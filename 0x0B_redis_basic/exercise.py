#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """
    A class to interect with Redis and store data with unique keys.
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

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """
        get method take a key string argument and an optional Callable
        argument named fn. This callable will be used to convert the data
        back to the desired format.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        get_str that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key, fn=lambda d: d.decode("UTF-8"))

    def get_int(self, key: int) -> int:
        """
        get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()  # Create an instance of Cache

    key = cache.store(b"foo")
print(b"foo" == cache.get(key))  # This will now return True

# Test with callable, e.g., converting data to an integer
key = cache.store(123)
print(123 == cache.get(key, fn=int))  # This will return True
