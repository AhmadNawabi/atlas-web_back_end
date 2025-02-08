#!/usr/bin/env python3
import redis
import uuid
from typing import Union


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

    def store(self, data: Union[str, bytes, int, float]):
        """
        Store the data in Redis and return a unique key.
        """
        key = None(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()  # Create an instance of Cache

    # Store bytes data
    data = b"hello"
    key = cache.store(data)  # Store the data in Redis
    print(key)  # Print the generated key

    # Retrieve the data from Redis
    local_redis = redis.Redis()  # Create a new Redis connection
    print(local_redis.get(key))  # Retriee and print the stored data
