#!/usr/bin/env python3
import bcrypt
from user import User
from uuid import uuid4
from db import DB
from typing import TypeVar, Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

T = TypeVar("T", bound="User")
TypeUser = Union[T, None]


def _hash_password(password: str) -> bytes:
    """returns a bytes that is a salted hash of the input password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def _generate_uuid() -> str:
    """return a string representation of a UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Hash the password using _hash_password,and save
        the user to the database
        Return:
            ValueError if user already exist base on email.
            Return user object on success.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Locate user by email, check the password with bcrypt.checkpw
        Return:
            True, if it matches
            False, if other cases
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Takes email string argument
        Return:
            Session id on success.
            None on failure.
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> TypeUser:
        """Takes a single session_id
        Return:
            User on success
            None on failure
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Takes user_id argument and updat the corresponding user's
        session_id to None
        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user.session_id is not None:
                self._db.update_user(user.id, session_id=None)
        except Exception:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Takes an email string as arguments and set user reset_token
        Return:
            - Generated token on success.
            - ValueError on Failure.
        """
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                raise ValueError
        except Exception:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password via reset token"""
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
            hsh_pw = _hash_password(password)
            self._db.update_user(
                usr.id, hashed_password=hsh_pw, reset_token=None)
            return None
        except NoResultFound:
            raise ValueError
