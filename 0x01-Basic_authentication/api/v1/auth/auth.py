#!/usr/bin/env python3
"""Classe to manage API authentication"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check for authentication
        Returns:
            - True when authication successfull
            - False when unsuccessfull
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Check for authoriztion in the request header
        Returns:
            - None if request is none
            - Flask object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Fetch authorized User
        Return:
            - None if User not available
            - return the user
        """
        return None
