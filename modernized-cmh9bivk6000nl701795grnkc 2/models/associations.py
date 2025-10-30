# Association tables for many-to-many relationships
# Source: movies_sql_procedures/movies_tables/create_movies_tables.sql lines 121-180

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class MovieCountry(Base):
    """Movie-Country association table

    Original SQL (lines 124-131):
    CREATE TABLE MOVIE_COUNTRIES (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_COUNTRIES_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IsoCountry VARCHAR2(2) CONSTRAINT MOVIE_COUNTRIES_ISOCOUNTRY_FK REFERENCES COUNTRIES(IsoCountry) ON DELETE CASCADE,
        CONSTRAINT MOVIE_COUNTRIES_PK PRIMARY KEY(IdMovie, IsoCountry)
    );
    """
    __tablename__ = 'movie_countries'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)
    iso_country: Mapped[str] = mapped_column('IsoCountry', String(2), ForeignKey('countries.IsoCountry', ondelete='CASCADE'), primary_key=True)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="countries")
    country: Mapped["Country"] = relationship("Country", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieCountry(movie_id={self.id_movie!r}, country={self.iso_country!r})"


class MovieLanguage(Base):
    """Movie-Language association table

    Original SQL (lines 133-140):
    CREATE TABLE MOVIE_LANGUAGES (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_LANGUAGES_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IsoLang VARCHAR2(2) CONSTRAINT MOVIE_LANGUAGES_ISOLANG_FK REFERENCES LANGUAGES(IsoLang) ON DELETE CASCADE,
        CONSTRAINT MOVIE_LANGUAGES_PK PRIMARY KEY(IdMovie, IsoLang)
    );
    """
    __tablename__ = 'movie_languages'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)
    iso_lang: Mapped[str] = mapped_column('IsoLang', String(2), ForeignKey('languages.IsoLang', ondelete='CASCADE'), primary_key=True)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="languages")
    language: Mapped["Language"] = relationship("Language", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieLanguage(movie_id={self.id_movie!r}, language={self.iso_lang!r})"


class MovieGenre(Base):
    """Movie-Genre association table

    Original SQL (lines 142-149):
    CREATE TABLE MOVIE_GENRES (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_GENRES_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IdGenre NUMBER(5) CONSTRAINT MOVIE_GENRES_IDGENRE_FK REFERENCES GENRES(IdGenre) ON DELETE CASCADE,
        CONSTRAINT MOVIE_GENRES_PK PRIMARY KEY(IdMovie, IdGenre)
    );
    """
    __tablename__ = 'movie_genres'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)
    id_genre: Mapped[int] = mapped_column('IdGenre', Integer, ForeignKey('genres.IdGenre', ondelete='CASCADE'), primary_key=True)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="genres")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieGenre(movie_id={self.id_movie!r}, genre_id={self.id_genre!r})"


class MovieActor(Base):
    """Movie-Actor association table with character name

    Original SQL (lines 151-162):
    CREATE TABLE MOVIE_ACTORS (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_ACTORS_IDMOVIE_NN NOT NULL CONSTRAINT MOVIE_ACTORS_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IdActor NUMBER(7) CONSTRAINT MOVIE_ACTORS_IDACTOR_NN NOT NULL CONSTRAINT MOVIE_ACTORS_IDACTOR_FK REFERENCES ACTORS(IdActor) ON DELETE CASCADE,
        CharacterName VARCHAR2(36) CONSTRAINT MOVIE_ACTORS_NAME_NN NOT NULL,
        CONSTRAINT MOVIE_MOVIE_ACTORS_PK PRIMARY KEY(IdMovie, IdActor, CharacterName)
    );
    """
    __tablename__ = 'movie_actors'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_actor: Mapped[int] = mapped_column('IdActor', Integer, ForeignKey('actors.IdActor', ondelete='CASCADE'), primary_key=True, nullable=False)
    character_name: Mapped[str] = mapped_column('CharacterName', String(36), primary_key=True, nullable=False)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="actors")
    actor: Mapped["Actor"] = relationship("Actor", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieActor(movie_id={self.id_movie!r}, actor_id={self.id_actor!r}, character={self.character_name!r})"


class MovieDirector(Base):
    """Movie-Director association table

    Original SQL (lines 164-171):
    CREATE TABLE MOVIE_DIRECTORS (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_DIRECTORS_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IdDirector NUMBER(7) CONSTRAINT MOVIE_DIRECTORS_IDDIRECTOR_FK REFERENCES DIRECTORS(IdDirector) ON DELETE CASCADE,
        CONSTRAINT MOVIE_DIRECTORS_PK PRIMARY KEY(IdMovie, IdDirector)
    );
    """
    __tablename__ = 'movie_directors'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)
    id_director: Mapped[int] = mapped_column('IdDirector', Integer, ForeignKey('directors.IdDirector', ondelete='CASCADE'), primary_key=True)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="directors")
    director: Mapped["Director"] = relationship("Director", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieDirector(movie_id={self.id_movie!r}, director_id={self.id_director!r})"


class MovieProductionCompany(Base):
    """Movie-Production Company association table

    Original SQL (lines 173-180):
    CREATE TABLE MOVIE_PROD_COMPS (
        IdMovie NUMBER(6) CONSTRAINT MOVIE_PROD_COMPS_IDMOVIE_FK REFERENCES MOVIES(IdMovie) ON DELETE CASCADE,
        IdComp NUMBER(5) CONSTRAINT MOVIE_PROD_COMPS_IDCOMP_FK REFERENCES PROD_COMPS(IdComp) ON DELETE CASCADE,
        CONSTRAINT MOVIE_PROD_COMPS_PK PRIMARY KEY(IdMovie, IdComp)
    );
    """
    __tablename__ = 'movie_prod_comps'

    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)
    id_comp: Mapped[int] = mapped_column('IdComp', Integer, ForeignKey('prod_comps.IdComp', ondelete='CASCADE'), primary_key=True)

    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="production_companies")
    company: Mapped["ProductionCompany"] = relationship("ProductionCompany", back_populates="movies")

    def __repr__(self) -> str:
        return f"MovieProductionCompany(movie_id={self.id_movie!r}, company_id={self.id_comp!r})"
