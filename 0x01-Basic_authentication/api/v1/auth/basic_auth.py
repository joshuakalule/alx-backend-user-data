#!/usr/bin/env python3
"""
Module to handle Basic authentication
"""
from api.v1.auth.auth import Auth


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
