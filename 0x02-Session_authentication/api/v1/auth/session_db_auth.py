#!/usr/bin/env python3
"""
Module to handle Sessions from the database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
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
        except Exception as e:
            return None
        created_at = user_session_obj.created_at
        user_id = user_session_obj.user_id

        if self.session_duration <= 0:
            return user_id

        expire_at = created_at + timedelta(seconds=self.session_duration)
        if expire_at < datetime.now():
            return None
        return user_id

    def destroy_session(self, request=None):
        """Deletes the session in db to implement logout"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            search_results = UserSession.search({'session_id': session_id})
            user_session_obj = search_results[0]
            if not user_session_obj:
                return False
            # Delete object
            user_session_obj.remove()
            # Remove session_id - user_id pair
            if session_id in self.user_id_by_session_id:
                del self.user_id_by_session_id[session_id]
            return True
        except Exception as e:
            # print("Exception: ", e)
            return False
