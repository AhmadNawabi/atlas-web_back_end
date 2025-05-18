#!/usr/bin/env python3
"""Authentication module for user registration, login and session management."""

import bcrypt
import uuid
from typing import Optional

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The plain password.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID string.

    Returns:
        str: UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Authentication system to manage users and sessions."""

    def __init__(self):
        """Initialize the Auth instance with database access."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with a hashed password.

        Args:
            email (str): User's email.
            password (str): User's plain password.

        Raises:
            ValueError: If user already exists.

        Returns:
            User: The created User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials.

        Args:
            email (str): User's email.
            password (str): Plain password.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except (NoResultFound, MultipleResultsFound, Exception):
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Create a session ID for the user.

        Args:
            email (str): User's email.

        Returns:
            Optional[str]: UUID session ID, or None on error.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, MultipleResultsFound, Exception):
            return None

    def get_user_from_session_id(
        self,
        session_id: Optional[str]
    ) -> Optional[User]:
        """Get a user by session ID.

        Args:
            session_id (Optional[str]): UUID session ID.

        Returns:
            Optional[User]: User object or None if not found.
        """
        if not session_id or not isinstance(session_id, str):
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, MultipleResultsFound, Exception):
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session by clearing user's session ID.

        Args:
            user_id (int): ID of the user.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user.

        Args:
            email (str): The user's email.

        Raises:
            ValueError: If user is not found.

        Returns:
            str: UUID reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except (NoResultFound, MultipleResultsFound, Exception):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password using reset token.

        Args:
            reset_token (str): UUID token.
            password (str): New password.

        Raises:
            ValueError: If token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed,
                reset_token=None
            )
        except (NoResultFound, MultipleResultsFound, Exception):
            raise ValueError
