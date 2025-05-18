#!/usr/bin/env python3
"""
Database access layer using SQLAlchemy for managing user records.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class to manage SQLAlchemy database connection and queries."""

    def __init__(self) -> None:
        """Initialize a new database connection and session."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)()

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Args:
            email (str): User's email.
            hashed_password (str): Hashed password.
        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by keyword arguments.
        Returns:
            User: The matched user.
        Raises:
            InvalidRequestError: If no keyword is provided.
            NoResultFound: If no matching user is found.
        """
        if not kwargs:
            raise InvalidRequestError
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user attributes.
        Args:
            user_id (int): ID of the user to update.
            kwargs: Attributes to update.
        Raises:
            ValueError: If attribute is invalid.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
