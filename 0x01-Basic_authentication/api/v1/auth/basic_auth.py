#!/usr/bin/env python3
"""Inherits from Auth to create a basic Auth"""
from .auth import Auth


class BasicAuth(Auth):
    """class for basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base64 authorization value"""

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        basic_auth_values = authorization_header.split(" ")

        if len(basic_auth_values) != 2:
            return None
        return basic_auth_values[1]
