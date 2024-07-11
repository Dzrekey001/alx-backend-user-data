#!/usr/bin/env python3
"""Inherits from Auth to create a basic Auth"""
from api.v1.auth.auth import Auth


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decodes the Base64 Authorization header.

        Args:
            base64_authorization_header (Optional[str]): The Base64
            part of the Authorization header.

        Returns:
            Optional[str]: The decoded string if decoding was successful,
            otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            import base64
            decoded_byte = base64.b64decode(base64_authorization_header)
            return decoded_byte.decode("utf-8")
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extracts user credentials from the decoded Base64
        Authorization header.

        Args:
            decoded_base64_authorization_header (Optional[str]): The
            decoded Base64 authorization header.

        Returns:
            Optional[Tuple[str, str]]: A tuple of (username, password)
            if successful, otherwise None.
        """

        if decoded_base64_authorization_header is None:
            return(None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        try:
            name, pwd = decoded_base64_authorization_header.split(":", 1)
            return name, pwd
        except Exception as e:
            return (None, None)
