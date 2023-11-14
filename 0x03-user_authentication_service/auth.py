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
    return hashpw(password.encode('utf-8'), gensalt())
