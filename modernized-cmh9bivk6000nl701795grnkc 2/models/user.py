# User model
# Source: movies_sql_procedures/base_tables/create_base_tables.sql lines 17-23

from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from .base import Base

class User(Base):
    """User model for authentication and reviews

    Original SQL:
    CREATE TABLE USERS (
        IdUser INTEGER CONSTRAINT USERS_PK PRIMARY KEY,
        Login VARCHAR2(30) CONSTRAINT USERS_LOGIN_U UNIQUE CONSTRAINT USERS_LOGIN_NN NOT NULL,
        SyncToken CHAR(1) DEFAULT 0 CONSTRAINT USERS_SYNCTOKEN_NN NOT NULL
    );
    """
    __tablename__ = 'users'

    # Primary key
    id_user: Mapped[int] = mapped_column('IdUser', Integer, primary_key=True, autoincrement=True)

    # Attributes
    login: Mapped[str] = mapped_column('Login', String(30), unique=True, nullable=False)
    sync_token: Mapped[str] = mapped_column('SyncToken', String(1), nullable=False, default='0')

    # Relationships
    reviews: Mapped[List["UserReview"]] = relationship(
        "UserReview", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id_user!r}, login={self.login!r})"
