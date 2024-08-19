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
        if not user_id or type(user_id) != str:
            return None

        session_id = str(uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user_id based on session_id."""
        if not session_id or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id, None)
