#!/usr/bin/env python3
"""Module that handles authentication."""

from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Hashes a password."""
    if type(password) != str:
        return
    return hashpw(password.encode('utf-8'), gensalt())
