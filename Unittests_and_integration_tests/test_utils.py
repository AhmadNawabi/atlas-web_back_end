#!/usr/bin/env python3
"""Unittests for utils.py"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests the access_nested_map function from utils module."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that the method returns what it is supposed to."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that a KeyError is raised for the given inputs."""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(str(e.exception), "'{}'".format(path[-1]))


class TestGetJson(unittest.TestCase):
    """Tests the get_json function from utils module."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json function with a mocked requests.get call."""
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = test_payload
            response = get_json(test_url)
            self.assertEqual(response, test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the memoize decorator ensuring it caches the correct results."""

    def test_memoize(self):
        """Test the memoize decorator to confirm it
        caches the output of methods."""
        class TestClass:
            """Class for testing the memoize decorator."""
            def a_method(self):
                """A dummy method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """A property method to test memoization
                    of a_method's return value."""
                return self.a_method()

        with patch.object(
                TestClass, 'a_method', return_value=42
        ) as mock_method:
            test_class_instance = TestClass()
            self.assertEqual(test_class_instance.a_property, 42)
            self.assertEqual(test_class_instance.a_property, 42)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
