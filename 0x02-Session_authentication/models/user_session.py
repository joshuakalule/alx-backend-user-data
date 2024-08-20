#!/usr/bin/env python3
""" Model for Implementation of storage of sessions
"""
from models.base import Base


class UserSession(Base):
    """Class that implements storage of sessions."""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
