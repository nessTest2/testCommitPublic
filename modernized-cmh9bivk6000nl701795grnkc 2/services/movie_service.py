# Movie Service - Movie details retrieval
# Source: movies_sql_procedures/cb/eval_movies/find_movies.sql (SEARCH_PACKAGE.GetMovieById)
# and LoginSingleton.java getMovieRequest() (lines 189-208)

from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
import logging

from models import (
    Movie, MovieStatus, Certification,
    MovieGenre, MovieActor, MovieDirector, MovieProductionCompany,
    MovieCountry, MovieLanguage,
    Genre, Actor, Director, ProductionCompany, Country, Language,
    UserReview
)

logger = logging.getLogger(__name__)

@dataclass
class MovieDetails:
    """Movie details data class

    Equivalent to MovieObj_t custom Oracle type (find_movies.sql lines 21-45)
    """
    id_movie: int
    title: str
    title_orig: str
    release_year: Optional[int]
    vote_average_tmdb: float
    vote_count_tmdb: int
    vote_average_app: float
    vote_count_app: int
    runtime: Optional[int]
    poster_path: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    overview: Optional[str]
    status: str
    certification: Optional[str]
    genres: List[str] = field(default_factory=list)
    actors: List[str] = field(default_factory=list)
    characters: List[str] = field(default_factory=list)
    directors: List[str] = field(default_factory=list)
    prod_comps: List[str] = field(default_factory=list)
    countries: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)

class MovieService:
    """Service for retrieving movie details

    Migrated from SEARCH_PACKAGE.GetMovieById PL/SQL procedure
    """

    @staticmethod
    def get_movie_by_id(session: Session, movie_id: int) -> Optional[MovieDetails]:
        """Get complete movie details by ID

        Source: SEARCH_PACKAGE.GetMovieById (find_movies.sql lines 79-146)
        and LoginSingleton.getMovieRequest() (LoginSingleton.java lines 189-208)

        Args:
            session: Database session
            movie_id: Movie ID to retrieve

        Returns:
            MovieDetails object with all movie information, or None if not found
        """
        logger.info(f"Retrieving movie details for ID: {movie_id}")

        try:
            # Get base movie information
            # Source: find_movies.sql lines 90-99
            movie = session.query(Movie).filter(Movie.id_movie == movie_id).first()

            if not movie:
                logger.warning(f"Movie {movie_id} not found")
                return None

            # Calculate app ratings (from user reviews)
            # Source: find_movies.sql lines 103-105
            ratings_query = session.query(
                func.coalesce(func.avg(UserReview.rating), 0.0).label('avg_rating'),
                func.count(UserReview.rating).label('count')
            ).filter(UserReview.id_movie == movie_id).first()

            vote_average_app = float(ratings_query.avg_rating) if ratings_query else 0.0
            vote_count_app = int(ratings_query.count) if ratings_query else 0

            # Extract release year
            release_year = movie.release_date.year if movie.release_date else None

            # Get genres
            # Source: find_movies.sql lines 107-110
            genres = session.query(Genre.name).join(
                MovieGenre, MovieGenre.id_genre == Genre.id_genre
            ).filter(MovieGenre.id_movie == movie_id).all()
            genre_list = [g[0] for g in genres]

            # Get actors and characters
            # Source: find_movies.sql lines 112-115
            actors_query = session.query(
                Actor.name, MovieActor.character_name
            ).join(
                MovieActor, MovieActor.id_actor == Actor.id_actor
            ).filter(MovieActor.id_movie == movie_id).all()

            actor_list = [a[0] for a in actors_query]
            character_list = [a[1] for a in actors_query]

            # Get directors
            # Source: find_movies.sql lines 117-120
            directors = session.query(Director.name).join(
                MovieDirector, MovieDirector.id_director == Director.id_director
            ).filter(MovieDirector.id_movie == movie_id).all()
            director_list = [d[0] for d in directors]

            # Get production companies
            # Source: find_movies.sql lines 122-125
            prod_comps = session.query(ProductionCompany.name).join(
                MovieProductionCompany, MovieProductionCompany.id_comp == ProductionCompany.id_comp
            ).filter(MovieProductionCompany.id_movie == movie_id).all()
            prod_comp_list = [pc[0] for pc in prod_comps]

            # Get countries
            # Source: find_movies.sql lines 127-130
            countries = session.query(Country.name).join(
                MovieCountry, MovieCountry.iso_country == Country.iso_country
            ).filter(MovieCountry.id_movie == movie_id).all()
            country_list = [c[0] for c in countries]

            # Get languages
            # Source: find_movies.sql lines 132-135
            languages = session.query(Language.name).join(
                MovieLanguage, MovieLanguage.iso_lang == Language.iso_lang
            ).filter(MovieLanguage.id_movie == movie_id).all()
            language_list = [l[0] for l in languages]

            # Create MovieDetails object
            details = MovieDetails(
                id_movie=movie.id_movie,
                title=movie.title,
                title_orig=movie.title_orig,
                release_year=release_year,
                vote_average_tmdb=movie.vote_average,
                vote_count_tmdb=movie.vote_count,
                vote_average_app=vote_average_app,
                vote_count_app=vote_count_app,
                runtime=movie.runtime,
                poster_path=movie.poster_path,
                budget=movie.budget,
                revenue=movie.revenue,
                overview=movie.overview,
                status=movie.status.name if movie.status else "Unknown",
                certification=movie.certification.name if movie.certification else None,
                genres=genre_list,
                actors=actor_list,
                characters=character_list,
                directors=director_list,
                prod_comps=prod_comp_list,
                countries=country_list,
                languages=language_list
            )

            logger.info(f"Successfully retrieved movie: {movie.title}")
            return details

        except Exception as exc:
            logger.error(f"Error retrieving movie {movie_id}: {exc}")
            raise
