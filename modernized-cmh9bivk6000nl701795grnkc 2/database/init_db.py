# Database initialization
# Source: Migrated from movies_sql_procedures/*.sql

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pathlib import Path

# Import all models to ensure they're registered
from models import (
    Base, User, Movie, MovieStatus, Certification,
    Actor, Director, ProductionCompany,
    Genre, Country, Language,
    MovieCountry, MovieLanguage, MovieGenre,
    MovieActor, MovieDirector, MovieProductionCompany,
    UserReview
)

def get_database_path(db_name: str = "movies.db") -> str:
    """Get the path to the database file"""
    # Store in project root
    db_path = Path(__file__).parent.parent / db_name
    return f"sqlite:///{db_path}"

def init_database(db_name: str = "movies.db", echo: bool = False):
    """Initialize the database schema

    Creates all tables based on SQLAlchemy models.
    Equivalent to running all CREATE TABLE statements from SQL files.

    Args:
        db_name: Name of the SQLite database file
        echo: Whether to echo SQL statements (for debugging)
    """
    # Create engine
    database_url = get_database_path(db_name)
    engine = create_engine(database_url, echo=echo)

    print(f"Creating database at: {database_url}")

    # Create all tables
    Base.metadata.create_all(engine)

    print("Database schema created successfully!")
    return engine

def populate_lookup_tables(engine):
    """Populate lookup tables with initial data

    Adds essential data for genres, statuses, certifications, etc.
    """
    with Session(engine) as session:
        # Movie statuses
        # Source: Common movie statuses
        statuses = [
            MovieStatus(id_status=1, name="Released"),
            MovieStatus(id_status=2, name="Post Production"),
            MovieStatus(id_status=3, name="In Production"),
            MovieStatus(id_status=4, name="Planned"),
            MovieStatus(id_status=5, name="Rumored"),
            MovieStatus(id_status=6, name="Canceled"),
        ]
        session.add_all(statuses)

        # Certifications (common movie ratings)
        certifications = [
            Certification(id_certif=1, name="G"),
            Certification(id_certif=2, name="PG"),
            Certification(id_certif=3, name="PG-13"),
            Certification(id_certif=4, name="R"),
            Certification(id_certif=5, name="NC-17"),
            Certification(id_certif=6, name="NR"),
        ]
        session.add_all(certifications)

        # Genres (TMDB genre IDs)
        genres = [
            Genre(id_genre=28, name="Action"),
            Genre(id_genre=12, name="Adventure"),
            Genre(id_genre=16, name="Animation"),
            Genre(id_genre=35, name="Comedy"),
            Genre(id_genre=80, name="Crime"),
            Genre(id_genre=99, name="Documentary"),
            Genre(id_genre=18, name="Drama"),
            Genre(id_genre=10751, name="Family"),
            Genre(id_genre=14, name="Fantasy"),
            Genre(id_genre=36, name="History"),
            Genre(id_genre=27, name="Horror"),
            Genre(id_genre=10402, name="Music"),
            Genre(id_genre=9648, name="Mystery"),
            Genre(id_genre=10749, name="Romance"),
            Genre(id_genre=878, name="Science Fiction"),
            Genre(id_genre=10770, name="TV Movie"),
            Genre(id_genre=53, name="Thriller"),
            Genre(id_genre=10752, name="War"),
            Genre(id_genre=37, name="Western"),
        ]
        session.add_all(genres)

        # Countries (ISO codes)
        countries = [
            Country(iso_country="US", name="United States"),
            Country(iso_country="GB", name="United Kingdom"),
            Country(iso_country="FR", name="France"),
            Country(iso_country="DE", name="Germany"),
            Country(iso_country="IT", name="Italy"),
            Country(iso_country="ES", name="Spain"),
            Country(iso_country="CA", name="Canada"),
            Country(iso_country="JP", name="Japan"),
            Country(iso_country="AU", name="Australia"),
            Country(iso_country="CN", name="China"),
        ]
        session.add_all(countries)

        # Languages (ISO codes)
        languages = [
            Language(iso_lang="en", name="English"),
            Language(iso_lang="fr", name="French"),
            Language(iso_lang="de", name="German"),
            Language(iso_lang="it", name="Italian"),
            Language(iso_lang="es", name="Spanish"),
            Language(iso_lang="ja", name="Japanese"),
            Language(iso_lang="zh", name="Chinese"),
            Language(iso_lang="pt", name="Portuguese"),
            Language(iso_lang="ru", name="Russian"),
            Language(iso_lang="ko", name="Korean"),
        ]
        session.add_all(languages)

        session.commit()
        print("Lookup tables populated successfully!")

if __name__ == "__main__":
    # Initialize database
    engine = init_database(echo=True)

    # Populate lookup tables
    populate_lookup_tables(engine)

    print("\nDatabase initialization complete!")
    print("Next: Run 'python -m database.sample_data' to add sample movie data")
