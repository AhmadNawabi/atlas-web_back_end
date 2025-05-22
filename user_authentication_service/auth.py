#!/usr/bin/env python3
"""
This module provides functionalities for user authentication.
"""

import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if valid login, else False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # Directly use user.hashed_password without encoding
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with an email and password.
        """
        try:
            user = self._db.find_user_by(email=email)
            return user  # Instead of raising, return the existing user
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a session for a user."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve a user from a session ID.

        Args:
            session_id (str): The session ID to find the user for.

        Returns:
            User: The user associated with the session ID,
            or None if no user is found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session."""
        if user_id is None:
            return None

        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for a user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: A reset token as a string.

        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("No user found with this email")

        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns:
        str: A string representation of the newly generated UUID.
    """
    return str(uuid.uuid4())
