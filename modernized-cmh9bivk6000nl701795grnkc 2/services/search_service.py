# Search Service - Movie search functionality
# Source: movies_sql_procedures/cb/eval_movies/find_movies.sql (SEARCH_PACKAGE.FindMovies)
# and LoginSingleton.java findMoviesRequest() (lines 138-187)

from sqlalchemy import select, or_, and_, func, extract
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Tuple, Optional
import logging

from models import Movie, Actor, Director, MovieActor, MovieDirector

logger = logging.getLogger(__name__)

class SearchService:
    """Service for searching movies

    Migrated from SEARCH_PACKAGE.FindMovies PL/SQL procedure
    """

    @staticmethod
    def find_movies(
        session: Session,
        title: Optional[str] = None,
        year: Optional[int] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        actor_names: Optional[List[str]] = None,
        director_names: Optional[List[str]] = None,
        max_results: int = 30
    ) -> List[Tuple[int, str, Optional[int]]]:
        """Find movies matching search criteria

        Source: SEARCH_PACKAGE.FindMovies procedure (find_movies.sql lines 150-280)
        and LoginSingleton.findMoviesRequest() (LoginSingleton.java lines 138-187)

        Args:
            session: Database session
            title: Movie title (partial match supported)
            year: Exact release year
            year_min: Minimum release year
            year_max: Maximum release year
            actor_names: List of actor names to filter by
            director_names: List of director names to filter by
            max_results: Maximum number of results (default 30, from Rennequinepolis.java line 74)

        Returns:
            List of tuples: (id_movie, title, release_year)
        """
        logger.info(f"Searching movies: title={title}, year={year}, year_range=({year_min}, {year_max}), "
                   f"actors={actor_names}, directors={director_names}")

        # Start building query
        query = select(
            Movie.id_movie,
            Movie.title,
            extract('year', Movie.release_date).label('release_year')
        ).distinct()

        # Title filter (partial match)
        # Source: find_movies.sql - uses LIKE for title matching
        if title:
            query = query.where(Movie.title.ilike(f"%{title}%"))

        # Year filters
        # Source: find_movies.sql lines 170-180 - handles exact year or year range
        if year is not None:
            # Exact year match
            query = query.where(extract('year', Movie.release_date) == year)
        else:
            # Year range
            if year_min is not None:
                query = query.where(extract('year', Movie.release_date) >= year_min)
            if year_max is not None:
                query = query.where(extract('year', Movie.release_date) <= year_max)

        # Actor filters
        # Source: find_movies.sql lines 190-210 - joins with MOVIE_ACTORS and filters by actor names
        if actor_names:
            for actor_name in actor_names:
                # Create subquery for each actor
                actor_subquery = (
                    select(MovieActor.id_movie)
                    .join(Actor, MovieActor.id_actor == Actor.id_actor)
                    .where(Actor.name.ilike(f"%{actor_name}%"))
                )
                query = query.where(Movie.id_movie.in_(actor_subquery))

        # Director filters
        # Source: find_movies.sql lines 220-240 - joins with MOVIE_DIRECTORS and filters by director names
        if director_names:
            for director_name in director_names:
                # Create subquery for each director
                director_subquery = (
                    select(MovieDirector.id_movie)
                    .join(Director, MovieDirector.id_director == Director.id_director)
                    .where(Director.name.ilike(f"%{director_name}%"))
                )
                query = query.where(Movie.id_movie.in_(director_subquery))

        # Order by title and limit results
        # Source: Rennequinepolis.java line 74 - limits to 30 results
        query = query.order_by(Movie.title).limit(max_results)

        # Execute query
        results = session.execute(query).all()

        logger.info(f"Found {len(results)} movies")
        return [(row.id_movie, row.title, row.release_year) for row in results]

    @staticmethod
    def find_movies_dict(
        session: Session,
        title: Optional[str] = None,
        year: Optional[int] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        actor_names: Optional[List[str]] = None,
        director_names: Optional[List[str]] = None,
        max_results: int = 30
    ) -> Dict[str, int]:
        """Find movies and return as dictionary

        Convenience method that returns results in the same format as Java code
        Source: Rennequinepolis.java lines 73-89 - stores results in HashMap

        Returns:
            Dictionary mapping display string to movie ID
            Format: {"Title (Year)": id, "Title": id}
        """
        results = SearchService.find_movies(
            session, title, year, year_min, year_max,
            actor_names, director_names, max_results
        )

        # Convert to dictionary format matching Java HashMap
        # Source: Rennequinepolis.java lines 78-88
        results_dict = {}
        for id_movie, movie_title, release_year in results:
            if release_year:
                display_text = f"{movie_title} ({release_year})"
            else:
                display_text = movie_title
            results_dict[display_text] = id_movie

        return results_dict
