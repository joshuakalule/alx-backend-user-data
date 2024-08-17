#!/usr/bin/env python3
"""
Module to handle authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class to handle Authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to enforce auth"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        safe_path = path if path[-1] == '/' else path + '/'
        if safe_path in excluded_paths:
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
