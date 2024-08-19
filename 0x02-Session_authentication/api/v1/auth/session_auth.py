#!/usr/bin/env python3
"""
Module to handle Session authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """Class to handle session authentication."""

    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for user_id"""
        if not user_id:
            return None
        if type(user_id) != str:
            return None

        session_id = uuid4()

        self.user_id_by_session_id[session_id] = user_id

        return session_id
