#!/usr/bin/env python3
"""Classe to manage API authentication"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires authentication
        Returns:
            - True if path requires authentication
            - False if not
        """
        if excluded_paths is None or excluded_paths is []:
            return True
        new_excluded_paths = [p[:-1] if p.endswith("/")
                              else p for p in excluded_paths]

        if path and path.endswith("/"):
            path = path[:-1]

        if path not in new_excluded_paths or path is None:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """Check for authoriztion in the request header
        Returns:
            - None if request is none
            - Authorization value
        """
        if request is None or request.headers.get("Authorization") is None:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Fetch authorized User
        Return:
            - None if User not available
            - return the user
        """
        return None
