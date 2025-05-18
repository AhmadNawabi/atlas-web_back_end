#!/usr/bin/env python3
"""Authentication module for user management and sessions.
"""

import bcrypt
import uuid
from typing import Optional

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with a randomly-generated salt.

    Args:
        password (str): The plain password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID string.

    Returns:
        str: A string representation of a UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Authentication class to manage users and sessions."""

    def __init__(self):
        """Initialize the authentication system with a database connection."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with a hashed password.

        Args:
            email (str): The user's email.
            password (str): The user's plain password.

        Raises:
            ValueError: If the user already exists.

        Returns:
            User: The created user object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's login credentials.

        Args:
            email (str): The user's email.
            password (str): The plain password provided.

        Returns:
            bool: True if credentials are valid, else False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Creates a session ID for a user if email is valid.

        Args:
            email (str): The user's email.

        Returns:
            Optional[str]: The session ID or None if user doesn't exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: Optional[str]) -> Optional[User]:
        """Retrieves a user based on a session ID.

        Args:
            session_id (Optional[str]): The session ID.

        Returns:
            Optional[User]: The user object or None.
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Removes a user's session ID (logs them out).

        Args:
            user_id (int): The user ID.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for a user.

        Args:
            email (str): The user's email.

        Raises:
            ValueError: If user doesn't exist.

        Returns:
            str: The reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_pwd,
                reset_token=None
            )
        except Exception:
            raise ValueError
