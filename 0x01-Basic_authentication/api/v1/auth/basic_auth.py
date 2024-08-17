#!/usr/bin/env python3
"""
Module to handle Basic authentication
"""
import binascii
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, Union
from models.user import User


class BasicAuth(Auth):
    """Class to handle basic authentication."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Retrieves the autho-params of the Authurization header"""

        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.replace('Basic ', '').strip()

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes auth-param for basic auth"""

        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            b = base64.b64decode(base64_authorization_header, validate=True)
            return b.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """Retrieves email and password fro base64 encoded value"""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        c = decoded_base64_authorization_header.split(':', maxsplit=1)
        email, password = c
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> Union[User, None]:  # type: ignore
        """Fetches user instance based on email and password"""
        if not user_email or not user_pwd:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            found_users = User.search({'email': user_email})
        except KeyError:
            return None
        if len(found_users) == 0:
            return None
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> Union[User, None]:
        """Retrive the current user."""
        auth_header = self.authorization_header(request)
        auth_param = self.extract_base64_authorization_header(auth_header)
        auth_str = self.decode_base64_authorization_header(auth_param)
        email, password = self.extract_user_credentials(auth_str)

        return self.user_object_from_credentials(email, password)
