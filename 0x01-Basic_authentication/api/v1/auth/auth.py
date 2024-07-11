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
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')

            if '*' in excluded_path:
                if fnmatch.fnmatch(path, excluded_path):
                    return False
            else:
                if path == excluded_path:
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
