#!/usr/bin/env python3

"""
Authentication
"""

from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from bcrypt import checkpw
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    hash password
    Args:
        password (str): password
    Returns:
        bytes: hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """
    Returs a string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers new users to database
        Args:
            email (str): user email
            password (str): user password
        Returns:
            User: Newly created user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates credentials
        Args:
            email (str): user email
            password (str): user password
        Returns:
            bool: True if matches else False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()

        if checkpw(encoded_password, user_password):
            return True

        return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Get session id
        Args:
            email (str): user email
        Returns:
            str: session id
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    ef get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get user from session_id
        Args:
            session_id (str): session_id
        Returns:
            Union[User, None]: User object if found else None
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
