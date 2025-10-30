# Movie, MovieStatus, and Certification models
# Source: movies_sql_procedures/movies_tables/create_movies_tables.sql

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import date

from .base import Base

class MovieStatus(Base):
    """Movie status lookup table

    Original SQL (lines 62-68):
    CREATE TABLE MOVIES_STATUS (
        IdStatus NUMBER(2) CONSTRAINT MOVIES_STATUS_PK PRIMARY KEY,
        Name VARCHAR2(15) CONSTRAINT MOVIES_STATUS_NAME_NN NOT NULL CONSTRAINT MOVIES_STATUS_NAME_U UNIQUE
    );
    """
    __tablename__ = 'movies_status'

    id_status: Mapped[int] = mapped_column('IdStatus', Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column('Name', String(15), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["Movie"]] = relationship("Movie", back_populates="status")

    def __repr__(self) -> str:
        return f"MovieStatus(id={self.id_status!r}, name={self.name!r})"


class Certification(Base):
    """Movie certification/rating lookup table

    Original SQL (lines 53-59):
    CREATE TABLE CERTIFICATIONS (
        IdCertif NUMBER(3) CONSTRAINT CERTIFICATIONS_PK PRIMARY KEY,
        Name VARCHAR2(12) CONSTRAINT CERTIFICATIONS_NAME_NN NOT NULL CONSTRAINT CERTIFICATIONS_NAME_U UNIQUE
    );
    """
    __tablename__ = 'certifications'

    id_certif: Mapped[int] = mapped_column('IdCertif', Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column('Name', String(12), unique=True, nullable=False)

    # Relationships
    movies: Mapped[List["Movie"]] = relationship("Movie", back_populates="certification")

    def __repr__(self) -> str:
        return f"Certification(id={self.id_certif!r}, name={self.name!r})"


class Movie(Base):
    """Main movie entity

    Original SQL (lines 93-119):
    CREATE TABLE MOVIES (
        IdMovie NUMBER(6) CONSTRAINT MOVIES_PK PRIMARY KEY,
        Title VARCHAR2(58) CONSTRAINT MOVIES_TITLE_NN NOT NULL,
        TitleOrig VARCHAR2(59) CONSTRAINT MOVIES_TITLEORIG_NN NOT NULL,
        ReleaseDate DATE,
        IdStatus NUMBER(2) CONSTRAINT MOVIES_IDSTATUS_NN NOT NULL CONSTRAINT MOVIES_IDSTATUS_FK REFERENCES MOVIES_STATUS(IdStatus) ON DELETE CASCADE,
        VoteAverage NUMBER(2,1) CONSTRAINT MOVIES_VOTEAVG_NN NOT NULL CONSTRAINT MOVIES_VOTEAVG_CH CHECK(VoteAverage >= 0 AND VoteAverage <= 10),
        VoteCount NUMBER(4) CONSTRAINT MOVIES_VOTECOUNT_NN NOT NULL,
        Runtime NUMBER(3),
        IdCertif NUMBER(3) CONSTRAINT MOVIES_IDCERTIF_FK REFERENCES CERTIFICATIONS(IdCertif) ON DELETE CASCADE,
        PosterPath VARCHAR2(32),
        Budget NUMBER(8),
        Revenue NUMBER(8),
        Homepage VARCHAR2(122),
        Tagline VARCHAR2(172),
        Overview VARCHAR2(949),
        SyncToken CHAR(1) DEFAULT '0' CONSTRAINT MOVIES_SYNCTOKEN_NN NOT NULL
    );
    """
    __tablename__ = 'movies'

    # Primary key
    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, primary_key=True)

    # Basic information
    title: Mapped[str] = mapped_column('Title', String(58), nullable=False)
    title_orig: Mapped[str] = mapped_column('TitleOrig', String(59), nullable=False)
    release_date: Mapped[Optional[date]] = mapped_column('ReleaseDate', Date, nullable=True)

    # Foreign keys
    id_status: Mapped[int] = mapped_column('IdStatus', Integer, ForeignKey('movies_status.IdStatus', ondelete='CASCADE'), nullable=False)
    id_certif: Mapped[Optional[int]] = mapped_column('IdCertif', Integer, ForeignKey('certifications.IdCertif', ondelete='CASCADE'), nullable=True)

    # Ratings and metrics
    vote_average: Mapped[float] = mapped_column('VoteAverage', Float, nullable=False)
    vote_count: Mapped[int] = mapped_column('VoteCount', Integer, nullable=False)
    runtime: Mapped[Optional[int]] = mapped_column('Runtime', Integer, nullable=True)

    # Financial
    budget: Mapped[Optional[int]] = mapped_column('Budget', Integer, nullable=True)
    revenue: Mapped[Optional[int]] = mapped_column('Revenue', Integer, nullable=True)

    # Additional information
    poster_path: Mapped[Optional[str]] = mapped_column('PosterPath', String(32), nullable=True)
    homepage: Mapped[Optional[str]] = mapped_column('Homepage', String(122), nullable=True)
    tagline: Mapped[Optional[str]] = mapped_column('Tagline', String(172), nullable=True)
    overview: Mapped[Optional[str]] = mapped_column('Overview', String(949), nullable=True)

    # Sync token for backup/restore
    sync_token: Mapped[str] = mapped_column('SyncToken', String(1), nullable=False, default='0')

    # Relationships
    status: Mapped["MovieStatus"] = relationship("MovieStatus", back_populates="movies")
    certification: Mapped[Optional["Certification"]] = relationship("Certification", back_populates="movies")

    # Many-to-many relationships via association tables
    countries: Mapped[List["MovieCountry"]] = relationship("MovieCountry", back_populates="movie", cascade="all, delete-orphan")
    languages: Mapped[List["MovieLanguage"]] = relationship("MovieLanguage", back_populates="movie", cascade="all, delete-orphan")
    genres: Mapped[List["MovieGenre"]] = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")
    actors: Mapped[List["MovieActor"]] = relationship("MovieActor", back_populates="movie", cascade="all, delete-orphan")
    directors: Mapped[List["MovieDirector"]] = relationship("MovieDirector", back_populates="movie", cascade="all, delete-orphan")
    production_companies: Mapped[List["MovieProductionCompany"]] = relationship("MovieProductionCompany", back_populates="movie", cascade="all, delete-orphan")

    # User reviews
    reviews: Mapped[List["UserReview"]] = relationship("UserReview", back_populates="movie", cascade="all, delete-orphan")

    # Table constraints
    __table_args__ = (
        CheckConstraint('VoteAverage >= 0 AND VoteAverage <= 10', name='movies_voteavg_ch'),
    )

    def __repr__(self) -> str:
        return f"Movie(id={self.id_movie!r}, title={self.title!r}, year={self.release_date.year if self.release_date else None!r})"
