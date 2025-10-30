# Lookup tables: Genre, Country, Language
# Source: movies_sql_procedures/movies_tables/create_movies_tables.sql

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .base import Base

class Genre(Base):
    """Movie genre lookup table

    Original SQL (lines 45-50):
    CREATE TABLE GENRES (
        IdGenre NUMBER(5) CONSTRAINT GENRES_PK PRIMARY KEY,
        Name VARCHAR2(16) CONSTRAINT GENRES_NAME_NN NOT NULL CONSTRAINT GENRES_NAME_U UNIQUE
    );
    """
    __tablename__ = 'genres'

    id_genre: Mapped[int] = mapped_column('IdGenre', Integer, primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(16), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieGenre"]] = relationship("MovieGenre", back_populates="genre", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Genre(id={self.id_genre!r}, name={self.name!r})"


class Country(Base):
    """Country lookup table

    Original SQL (lines 29-34):
    CREATE TABLE COUNTRIES (
        IsoCountry VARCHAR2(2) CONSTRAINT COUNTRIES_PK PRIMARY KEY,
        Name VARCHAR2(24) CONSTRAINT COUNTRIES_NAME_NN NOT NULL CONSTRAINT COUNTRIES_NAME_U UNIQUE
    );
    """
    __tablename__ = 'countries'

    iso_country: Mapped[str] = mapped_column('IsoCountry', String(2), primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(24), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieCountry"]] = relationship("MovieCountry", back_populates="country", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Country(iso={self.iso_country!r}, name={self.name!r})"


class Language(Base):
    """Language lookup table

    Original SQL (lines 37-42):
    CREATE TABLE LANGUAGES (
        IsoLang VARCHAR2(2) CONSTRAINT LANGUAGES_PK PRIMARY KEY,
        Name VARCHAR2(11) CONSTRAINT LANGUAGES_NAME_NN NOT NULL CONSTRAINT LANGUAGES_NAME_U UNIQUE
    );
    """
    __tablename__ = 'languages'

    iso_lang: Mapped[str] = mapped_column('IsoLang', String(2), primary_key=True)
    name: Mapped[str] = mapped_column('Name', String(11), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["MovieLanguage"]] = relationship("MovieLanguage", back_populates="language", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Language(iso={self.iso_lang!r}, name={self.name!r})"
