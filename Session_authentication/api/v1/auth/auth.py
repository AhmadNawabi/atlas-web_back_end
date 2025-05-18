#!/usr/bin/env python3
"""
auth.py

This module provides the Auth class to manage API authentication.
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the API authentication.

    Methods:
        require_auth(path: str, excluded_paths: List[str]) -> bool
        authorization_header(request=None) -> str
        current_user(request=None) -> TypeVar('User')
        session_cookie(request=None) -> str
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure the path ends with a slash
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            else:
                if path.rstrip('/') == excluded_path.rstrip('/'):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns the cookie value for a given request based on SESSION_NAME.
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None

        return request.cookies.get(session_name)
