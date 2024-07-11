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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or (path + '/') in excluded_paths:
            return False

        # using regex to match paths with asterik sign
        # checking for any match between the provided
        # match and the excluded path

        # matching the ends of the urls i.e end part of the url
        end_input_url = path.split('/', 3)[-1]
        for paths in excluded_paths:
            if "*" in paths:
                end_match_url = paths.split('/', 3)[-1].replace("*", "")
                sim = re.search(f"^{end_match_url}", end_input_url)
                if sim:
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
