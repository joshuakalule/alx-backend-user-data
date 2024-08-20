#!/usr/bin/env python3
"""
Module to handle Session expiration
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Class that implements session expiry."""

    def __init__(self) -> None:
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user based on session id"""
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_value = self.user_id_by_session_id.get(session_id)
        if type(session_value) != dict:
            user_id = session_value
            return user_id

        created_at = session_value.get('created_at')
        user_id = session_value.get('user_id')
        if not created_at:
            return None
        if self.session_duration <= 0:
            return user_id

        duration = created_at + timedelta(seconds=self.session_duration)
        if duration < datetime.now():
            return None
        return user_id

    def create_session(self, user_id=None):
        """create session id with a timestamp"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id
