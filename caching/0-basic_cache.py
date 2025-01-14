#!/usr/bin/python3
"""Import BaseCaching from base_caching"""
from base_caching import BaseCaching
"""
Create a class BasicCache that inherits from
BaseCaching and implements a caching system:

This caching system doesn't have a limit.
"""


class BasicCache(BaseCaching):
    """A basic caching system that uses a dictionary
    to store cached items.

    Inherits from BaseCaching and uses the `cache_data` dictionary
    to store cached items. It provides methods to add and retrieve
    items from the cache."""

    def __init__(self):
        """
        Initialize the BasicCache instance.

        Initializes the `cache_data` dictionary inherited from the parent class
        to store the cached items.
        """
        self.cache_data = {}

    def put(self, key, item):
        """
        Add an item to the cache.

        Assigns the value `item` to the given
        `key` in the `cache_data` dictionary.
        If either `key` or `item` is `None`,
        this method will not add the item
        to the cache.

        Args:
            key (str): The key for the cache.
            item (str): The item to store in the cache.

        Returns:
            None: This method does not return any value.
        """
        self.cache_data[key] = item
        if key == None:
            return
        if item == None:
            return
        return self.cache_data

    def get(self, key):
        """
        Retrieve an item from the cache.

        Retrieves the value associated with
        `key` from the `cache_data` dictionary.
        If the `key` is `None` or does not exist
        in the cache, returns `None`.

        Args:
            key (str): The key to retrieve from the cache.

        Returns:
            str or None: The cached item if found,
            or `None` if the `key` is `None`
            or not in the cache.
        """
        if key == None:
            return None
        if key not in self.cache_data:
            return None
        return self.cache_data[key]
