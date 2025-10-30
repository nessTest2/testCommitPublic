# Sample movie data for testing
# Source: Equivalent to importing from the 182MB text file but with minimal test data

from sqlalchemy.orm import Session
from datetime import date
from database.init_db import get_database_path
from sqlalchemy import create_engine

from models import (
    Movie, Actor, Director, ProductionCompany,
    MovieActor, MovieDirector, MovieGenre, MovieCountry, MovieLanguage, MovieProductionCompany
)

def add_sample_movies(engine):
    """Add sample movie data for testing

    Adds a few well-known movies with complete data for testing all features.
    """
    with Session(engine) as session:
        # Sample actors
        actors = [
            Actor(id_actor=1, name="Tom Hanks"),
            Actor(id_actor=2, name="Tim Allen"),
            Actor(id_actor=3, name="Leonardo DiCaprio"),
            Actor(id_actor=4, name="Kate Winslet"),
            Actor(id_actor=5, name="Keanu Reeves"),
            Actor(id_actor=6, name="Laurence Fishburne"),
            Actor(id_actor=7, name="Morgan Freeman"),
            Actor(id_actor=8, name="Tim Robbins"),
            Actor(id_actor=9, name="Elijah Wood"),
            Actor(id_actor=10, name="Ian McKellen"),
        ]
        session.add_all(actors)

        # Sample directors
        directors = [
            Director(id_director=1, name="John Lasseter"),
            Director(id_director=2, name="James Cameron"),
            Director(id_director=3, name="Lana Wachowski"),
            Director(id_director=4, name="Lilly Wachowski"),
            Director(id_director=5, name="Frank Darabont"),
            Director(id_director=6, name="Peter Jackson"),
        ]
        session.add_all(directors)

        # Sample production companies
        companies = [
            ProductionCompany(id_comp=1, name="Pixar Animation Studios"),
            ProductionCompany(id_comp=2, name="20th Century Fox"),
            ProductionCompany(id_comp=3, name="Warner Bros."),
            ProductionCompany(id_comp=4, name="Castle Rock Entertainment"),
            ProductionCompany(id_comp=5, name="New Line Cinema"),
        ]
        session.add_all(companies)

        # Movie 1: Toy Story (1995)
        movie1 = Movie(
            id_movie=862,
            title="Toy Story",
            title_orig="Toy Story",
            release_date=date(1995, 11, 22),
            id_status=1,  # Released
            vote_average=7.7,
            vote_count=5415,
            runtime=81,
            id_certif=1,  # G
            poster_path="/rhIRbceoE9lR4veEXuwCC2wARtG.jpg",
            budget=30000000,
            revenue=373554033,
            homepage="http://www.disney.com/toy-story",
            tagline="The adventure takes off!",
            overview="Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences."
        )
        session.add(movie1)

        # Movie 2: Titanic (1997)
        movie2 = Movie(
            id_movie=597,
            title="Titanic",
            title_orig="Titanic",
            release_date=date(1997, 12, 19),
            id_status=1,  # Released
            vote_average=7.8,
            vote_count=11800,
            runtime=194,
            id_certif=3,  # PG-13
            poster_path="/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
            budget=200000000,
            revenue=2187463944,
            homepage="http://www.titanicmovie.com/",
            tagline="Nothing on Earth could come between them.",
            overview="101-year-old Rose DeWitt Bukater tells the story of her life aboard the Titanic, 84 years later. A young Rose boards the ship with her mother and fiancé. Meanwhile, Jack Dawson and Fabrizio De Rossi win third-class tickets aboard the ship. Rose tells the whole story from Titanic's departure through to its death—on its first and last voyage—on April 15, 1912."
        )
        session.add(movie2)

        # Movie 3: The Matrix (1999)
        movie3 = Movie(
            id_movie=603,
            title="The Matrix",
            title_orig="The Matrix",
            release_date=date(1999, 3, 31),
            id_status=1,  # Released
            vote_average=8.2,
            vote_count=14000,
            runtime=136,
            id_certif=4,  # R
            poster_path="/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            budget=63000000,
            revenue=463517383,
            homepage="http://www.warnerbros.com/matrix",
            tagline="The fight for the future begins.",
            overview="Set in the 22nd century, The Matrix tells the story of a computer hacker who joins a group of underground insurgents fighting the vast and powerful computers who now rule the earth."
        )
        session.add(movie3)

        # Movie 4: The Shawshank Redemption (1994)
        movie4 = Movie(
            id_movie=278,
            title="The Shawshank Redemption",
            title_orig="The Shawshank Redemption",
            release_date=date(1994, 9, 23),
            id_status=1,  # Released
            vote_average=8.7,
            vote_count=15000,
            runtime=142,
            id_certif=4,  # R
            poster_path="/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            budget=25000000,
            revenue=28341469,
            homepage=None,
            tagline="Fear can hold you prisoner. Hope can set you free.",
            overview="Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates -- including an older prisoner named Red -- for his integrity and unquenchable sense of hope."
        )
        session.add(movie4)

        # Movie 5: The Lord of the Rings: The Fellowship of the Ring (2001)
        movie5 = Movie(
            id_movie=120,
            title="The Lord of the Rings: The Fellowship of the Ring",
            title_orig="The Lord of the Rings: The Fellowship of the Ring",
            release_date=date(2001, 12, 18),
            id_status=1,  # Released
            vote_average=8.3,
            vote_count=16500,
            runtime=178,
            id_certif=3,  # PG-13
            poster_path="/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
            budget=93000000,
            revenue=871530324,
            homepage="http://www.lordoftherings.net/",
            tagline="One ring to rule them all.",
            overview="Young hobbit Frodo Baggins, after inheriting a mysterious ring from his uncle Bilbo, must leave his home in order to keep it from falling into the hands of its evil creator. Along the way, a fellowship is formed to protect the ringbearer and make sure that the ring arrives at its final destination: Mt. Doom, the only place where it can be destroyed."
        )
        session.add(movie5)

        session.flush()  # Ensure movies get IDs

        # Add associations for Toy Story
        session.add_all([
            MovieActor(id_movie=862, id_actor=1, character_name="Woody (voice)"),
            MovieActor(id_movie=862, id_actor=2, character_name="Buzz Lightyear (voice)"),
            MovieDirector(id_movie=862, id_director=1),
            MovieGenre(id_movie=862, id_genre=16),  # Animation
            MovieGenre(id_movie=862, id_genre=35),  # Comedy
            MovieGenre(id_movie=862, id_genre=10751),  # Family
            MovieCountry(id_movie=862, iso_country="US"),
            MovieLanguage(id_movie=862, iso_lang="en"),
            MovieProductionCompany(id_movie=862, id_comp=1),
        ])

        # Add associations for Titanic
        session.add_all([
            MovieActor(id_movie=597, id_actor=3, character_name="Jack Dawson"),
            MovieActor(id_movie=597, id_actor=4, character_name="Rose DeWitt Bukater"),
            MovieDirector(id_movie=597, id_director=2),
            MovieGenre(id_movie=597, id_genre=18),  # Drama
            MovieGenre(id_movie=597, id_genre=10749),  # Romance
            MovieCountry(id_movie=597, iso_country="US"),
            MovieLanguage(id_movie=597, iso_lang="en"),
            MovieProductionCompany(id_movie=597, id_comp=2),
        ])

        # Add associations for The Matrix
        session.add_all([
            MovieActor(id_movie=603, id_actor=5, character_name="Neo"),
            MovieActor(id_movie=603, id_actor=6, character_name="Morpheus"),
            MovieDirector(id_movie=603, id_director=3),
            MovieDirector(id_movie=603, id_director=4),
            MovieGenre(id_movie=603, id_genre=28),  # Action
            MovieGenre(id_movie=603, id_genre=878),  # Science Fiction
            MovieCountry(id_movie=603, iso_country="US"),
            MovieLanguage(id_movie=603, iso_lang="en"),
            MovieProductionCompany(id_movie=603, id_comp=3),
        ])

        # Add associations for The Shawshank Redemption
        session.add_all([
            MovieActor(id_movie=278, id_actor=7, character_name="Ellis Boyd 'Red' Redding"),
            MovieActor(id_movie=278, id_actor=8, character_name="Andy Dufresne"),
            MovieDirector(id_movie=278, id_director=5),
            MovieGenre(id_movie=278, id_genre=18),  # Drama
            MovieGenre(id_movie=278, id_genre=80),  # Crime
            MovieCountry(id_movie=278, iso_country="US"),
            MovieLanguage(id_movie=278, iso_lang="en"),
            MovieProductionCompany(id_movie=278, id_comp=4),
        ])

        # Add associations for The Lord of the Rings
        session.add_all([
            MovieActor(id_movie=120, id_actor=9, character_name="Frodo Baggins"),
            MovieActor(id_movie=120, id_actor=10, character_name="Gandalf"),
            MovieDirector(id_movie=120, id_director=6),
            MovieGenre(id_movie=120, id_genre=12),  # Adventure
            MovieGenre(id_movie=120, id_genre=14),  # Fantasy
            MovieGenre(id_movie=120, id_genre=28),  # Action
            MovieCountry(id_movie=120, iso_country="US"),
            MovieCountry(id_movie=120, iso_country="GB"),
            MovieLanguage(id_movie=120, iso_lang="en"),
            MovieProductionCompany(id_movie=120, id_comp=5),
        ])

        session.commit()
        print("Sample movie data added successfully!")
        print("\n5 movies added:")
        print("  - Toy Story (1995)")
        print("  - Titanic (1997)")
        print("  - The Matrix (1999)")
        print("  - The Shawshank Redemption (1994)")
        print("  - The Lord of the Rings: The Fellowship of the Ring (2001)")

if __name__ == "__main__":
    # Create engine
    database_url = get_database_path()
    engine = create_engine(database_url)

    # Add sample data
    add_sample_movies(engine)

    print("\nSample data loading complete!")
    print("You can now run: python main.py")
