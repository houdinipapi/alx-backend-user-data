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
