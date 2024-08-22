#!/usr/bin/env python3
"""Module that handles authentication."""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
from uuid import uuid4


def _generate_uuid() -> str:
    """Returns a string representation of a new uuid"""
    return str(uuid4())


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

    def update_password(self, reset_token: str, password: str) -> None:
        """update user password."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            msg = "no user corresponding to reset token"
            raise ValueError(msg)

        hashed_password = _hash_password(password)

        attributes = {
            'hashed_password': hashed_password,
            'reset_token': None
        }
        self._db.update_user(user.id, **attributes)

    def get_reset_password_token(self, email: str) -> str:
        """set and return a password reset reset token."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            msg = "User with email does not exist"
            raise ValueError(msg)

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def destroy_session(self, user_id: int) -> None:
        """Release user session by setting session_id attr to None"""
        self._db.update_user(user_id, session_id=None)

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Retrieve user based on session id"""
        if not session_id or type(session_id) != str:
            return None

        try:
            found_user = self._db.find_user_by(session_id=session_id)
            return found_user
        except Exception:
            return None

    def create_session(self, email: str) -> Optional[str]:
        """Create user session and return session_id"""
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(found_user.id, session_id=session_id)
        return session_id

    def valid_login(self, email: str, password: str) -> bool:
        """Returns True if email exists and is associated with password"""
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
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
