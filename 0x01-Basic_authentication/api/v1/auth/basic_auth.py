#!/usr/bin/env python3
"""
Module to handle Basic authentication
"""
import binascii
from api.v1.auth.auth import Auth
import base64


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
        except binascii.Error:
            return None
