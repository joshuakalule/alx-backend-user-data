#!/usr/bin/env python3
"""
Module to handle Sessions from the database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Class that handles sessions stored in the database."""

    def create_session(self, user_id=None):
        """Create session_id and store in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session_obj = UserSession(user_id=user_id, session_id=session_id)
        user_session_obj.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id based on session_id from the database."""
        if not session_id:
            return None
        try:
            search_results = UserSession.search({'session_id': session_id})
            user_session_obj = search_results[0]
            return user_session_obj.user_id
        except Exception as e:
            return None

    def destroy_session(self, request=None):
        """Deletes the session in db to implement logout"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            user_session_obj = UserSession.search({'session_id': session_id})
            if not user_session_obj:
                return False
            user_session_obj.remove()
            return True
        except Exception:
            return False
