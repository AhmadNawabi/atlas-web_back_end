#!/usr/bin/env python3
""" Pymongo """


def list_all(mango_collection: object) -> list:
    """List all documets in a collection"""
    return mango_collection.find({}) if mango_collection.find({}) else []
