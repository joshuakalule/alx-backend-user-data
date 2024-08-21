#!/usr/bin/env python3
"""Module that handles authentication."""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password."""
    if type(password) != str:
        return
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def valid_login(self, email: str, password: str) -> bool:
        """Returns True if email exists and is associated with password"""
        try:
            found_user = self._db.find_user_by(email=email)
        except Exception:
            return False

        bytes_password = password.encode('utf-8')

        return checkpw(bytes_password, found_user.hashed_password)

    def register_user(self, email: str, password: str) -> User:
        """Register a user."""
        try:
            if self._db.find_user_by(email=email):
                msg = f"User {email} already exists"
                raise ValueError(msg)
        except NoResultFound:
            pass

        hashed_passord = _hash_password(password)

        user = self._db.add_user(email=email, hashed_password=hashed_passord)

        return user
