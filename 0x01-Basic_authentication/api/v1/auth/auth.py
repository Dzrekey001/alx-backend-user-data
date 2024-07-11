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
        if path is not None and excluded_paths is not None and len(excluded_paths) > 0:  # nopep8
            if path.endswith('/'):
                path = path[:-1]
            for excluded_path in excluded_paths:
                if fnmatch.fnmatch(path, excluded_path):
                    return False
                if excluded_path.endswith('/'):
                    excluded_path = excluded_path[:-1]
                if excluded_path == path:
                    return False
        return True

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
