#!/usr/bin/env python3
"""
Module to handle authentication
"""
from typing import List, TypeVar
import os


class Auth:
    """
    Class to handle Authentication
    """

    def session_cookie(self, request=None):
        """Retrieve cookie from request."""
        if not request:
            return None
        cookie_key = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_key, None)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to enforce auth"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        safe_path = path if path[-1] == '/' else path + '/'
        for xpath in excluded_paths:
            if safe_path == xpath:
                return False
            if xpath[-1] == '*' and path.startswith(xpath[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Method to fetch authorization header"""
        if not request:
            return None
        auth_header_value = request.headers.get('Authorization', None)
        if not auth_header_value:
            return None
        return auth_header_value

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Method to return the currently logged in user"""
        return None
