#!/usr/bin/env python3
"""tsak 5. Encrypting passwords"""

import bcrypt


def hash_password(password: bytes) -> bytes:
    """Hash a password using bcrypt"""
    if not type(password) is bytes:
        password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
