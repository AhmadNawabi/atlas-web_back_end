#!/usr/bin/python3
"""Import BaseCaching from base_caching"""
from base_caching import BaseCaching
"""
Create a class BasicCache that inherits from
BaseCaching and is a caching system:

You must use self.cache_data - dictionary from
the parent class BaseCaching
This caching system doesn’t have limit
def put(self, key, item):
Must assign to the dictionary self.cache_data the
item value for the key key.
If key or item is None, this method should not
do anything.
def get(self, key):
Must return the value in self.cache_data linked to key.
If key is None or if the key doesn’t exist in self.cache_data,
return None.
"""


class BasicCache(BaseCaching):
    def __init__(self):
        self.cache_data = {}

    """
    def put(self, key, item):
    Must assign to the dictionary self.cache_data
    the item value for the key key.
    If key or item is None, this method should not do anything.
    """

    def put(self, key, item):
        self.cache_data[key] = item
        if key or item == None:
            pass
        return self.cache_data

    """
    def get(self, key):
    Must return the value in self.cache_data linked to key.
    If key is None or if the key doesn’t exist in self.cache_data,
    return None.
    """

    def get(self, key):
        if key == None:
            return None
        if key not in self.cache_data:
            return None
        return self.cache_data[key]
