from datetime import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy_utils as sau
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .entry import VaultEntry, Tag


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(255), unique=True)
    firstname: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    lastname: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    email: Mapped[Optional[str]] = mapped_column(sau.EmailType(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    password: Mapped[str] = mapped_column(sa.String(255))
    token: Mapped[str] = mapped_column(sa.String(255))
    salt: Mapped[str] = mapped_column(sa.String(255))

    vault_entries: Mapped[list[VaultEntry]] = relationship(cascade='all, delete-orphan')
    tags: Mapped[list[Tag]] = relationship(cascade='all, delete-orphan')

    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            id=None,
            *,
            username=None,
            password=None,
            token=None,
            salt=None,
            firstname=None,
            lastname=None,
            email=None,
            create_time=None
    ):
        """
        Model class representing an application user.

        Parameters:
            id (int | None): primary key (not passed directly)
            username (str): the username
            password (str): master password which will be hashed
            token (str): one time given, secret token
            salt (str): salt used for password hashing and token encryption
            firstname (str | None): forename
            lastname (str | None): family name
            email (str | None): email address of the user
            create_time (datetime | None): registration time
        """

        # noinspection PyTypeChecker
        self.id = id
        # noinspection PyTypeChecker
        self.username = username
        # noinspection PyTypeChecker
        self.password = password
        # noinspection PyTypeChecker
        self.token = token
        # noinspection PyTypeChecker
        self.salt = salt
        # noinspection PyTypeChecker
        self.firstname = firstname
        # noinspection PyTypeChecker
        self.lastname = lastname
        # noinspection PyTypeChecker
        self.email = email
        # noinspection PyTypeChecker
        self.created_at = create_time

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'username={self.username}, '
                f'firstname={self.firstname}, '
                f'lastname={self.lastname}, '
                f'email={self.email}')
