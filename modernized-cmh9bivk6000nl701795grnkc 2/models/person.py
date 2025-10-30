# Person-related models: Actor, Director, ProductionCompany
# Source: movies_sql_procedures/movies_tables/create_movies_tables.sql

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .base import Base

class Actor(Base):
    """Actor/Actress entity

    Original SQL (lines 71-76):
    CREATE TABLE ACTORS (
        IdActor NUMBER(7) CONSTRAINT ACTORS_PK PRIMARY KEY,
        Name VARCHAR2(36) CONSTRAINT ACTORS_NAME_NN NOT NULL CONSTRAINT ACTORS_NAME_U UNIQUE
    );
    """
    __tablename__ = 'actors'

    id_actor: Mapped[int] = mapped_column('IdActor', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(36), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieActor"]] = relationship("MovieActor", back_populates="actor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Actor(id={self.id_actor!r}, name={self.name!r})"


class Director(Base):
    """Director entity

    Original SQL (lines 78-83):
    CREATE TABLE DIRECTORS (
        IdDirector NUMBER(7) CONSTRAINT DIRECTORS_PK PRIMARY KEY,
        Name VARCHAR2(23) CONSTRAINT DIRECTORS_NAME_NN NOT NULL CONSTRAINT DIRECTORS_NAME_U UNIQUE
    );
    """
    __tablename__ = 'directors'

    id_director: Mapped[int] = mapped_column('IdDirector', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(23), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieDirector"]] = relationship("MovieDirector", back_populates="director", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Director(id={self.id_director!r}, name={self.name!r})"


class ProductionCompany(Base):
    """Production company entity

    Original SQL (lines 85-90):
    CREATE TABLE PROD_COMPS (
        IdComp NUMBER(5) CONSTRAINT PROD_COMPS_PK PRIMARY KEY,
        Name VARCHAR2(44) CONSTRAINT PROD_COMPS_NAME_NN NOT NULL CONSTRAINT PROD_COMPS_NAME_U UNIQUE
    );
    """
    __tablename__ = 'prod_comps'

    id_comp: Mapped[int] = mapped_column('IdComp', Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column('Name', String(44), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieProductionCompany"]] = relationship("MovieProductionCompany", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"ProductionCompany(id={self.id_comp!r}, name={self.name!r})"
