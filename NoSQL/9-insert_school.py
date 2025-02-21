#!/usr/bin/env python3
""" Pymongo """


def insert_school(mongo_collection: object, **kwargs):
    """
    function that insert a new documents in a collection
    based on kwargs 
    """
    data = mongo_collection.insert_one({**kwargs})
    return data.inserted_id
