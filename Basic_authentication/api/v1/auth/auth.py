#!/usr/bin/env python3
"""
Authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method: determines if path requires authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Public method: retrieves the Authorization header from request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method: retrieves the current user from the request"""
        return None
