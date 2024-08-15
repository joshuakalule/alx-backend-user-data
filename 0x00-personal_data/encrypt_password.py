#!/usr/bin/env python3
"""tsak 5. Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
