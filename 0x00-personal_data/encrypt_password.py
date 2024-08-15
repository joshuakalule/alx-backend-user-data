#!/usr/bin/env python3
"""tsak 5. Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates the provided password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
