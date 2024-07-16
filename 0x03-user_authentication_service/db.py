#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add user
        """
        if not email or not hashed_password:
            return

        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ find user function """
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs) -> None:
        """user’s attributes as passed in the method’s arguments
        then commit changes to the database.
        """
        if user_id is None:
            raise ValueError
        try:
            int(user_id)
        except Exception:
            raise ValueError
        user = self.find_user_by(id=user_id)
        for key in kwargs:
            if not hasattr(user, key):
                raise ValueError
        for key, value in kwargs.items():
            setattr(user, key, value)
            return None
