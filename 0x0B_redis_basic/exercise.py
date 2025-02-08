#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
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

    def get_int(self, key: str) -> int:
        """
        get_int that will automatically parametrize
        Cache.get with the correct conversion function.
        """
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value