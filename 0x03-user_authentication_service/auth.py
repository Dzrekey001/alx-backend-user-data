#!/usr/bin/env python3
import bcrypt
from user import User
from db import DB
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """returns a bytes that is a salted hash of the input password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Hash the password using _hash_password,and save
        the user to the database
        Return:
            ValueError if user already exist base on email.
            Return user object on success.
        """
        user = self._db.find_user_by(email=email)
        hash_pwd = _hash_password(password)
        if user:
            raise ValueError(f"User {email} already exists")
        return self._db.add_user(email, hash_pwd)
