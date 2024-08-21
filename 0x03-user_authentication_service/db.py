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
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """create a user model and save it to the database."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Retrieve a user by key word argumenets."""
        results = self._session.query(User).filter_by(**kwargs)

        if results.count() == 0:
            raise NoResultFound("No results found")

        return results.first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user using user_id and arbitrary kwargs."""

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            return None
        except InvalidRequestError:
            return None

        for attr, value in kwargs.items():
            if not hasattr(user, attr):
                err = f"'{attr}' does not correspond to a user attribute"
                raise ValueError(err)
            setattr(user, attr, value)

        self._session.commit()
        return None
