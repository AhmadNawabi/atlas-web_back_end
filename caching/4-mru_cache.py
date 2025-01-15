#!/usr/bin/python3
""" inherits from BaseCaching and is a caching system:"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    Create a class MRUCache that inherits from BaseCaching
    and is a caching system:
    """

    def __init__(self):
        super().__init__()

        self.cache_data = {}
        self.order = []

    def put(self, key, item):
        """
        Must assign to the dictionary self.cache_data
          the item value for the key key.
        If key or item is None, this method
          should not do anything.
        If the number of items in self.cache_data
          is higher that BaseCaching.MAX_ITEMS:
        you must discard the most recently used item (MRU algorithm)
        you must print DISCARD: with the key discarded
          and following by a new line
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.order.remove(key)

        self.cache_data[key] = item
        self.order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            most_use = self.order.pop(-2)
            del self.cache_data[most_use]
            print(f'DISCARD: {most_use}')

    def get(self, key):
        """
        Must return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t
        exist in self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
