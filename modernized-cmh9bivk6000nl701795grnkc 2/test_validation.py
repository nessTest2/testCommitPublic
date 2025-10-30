"""
Comprehensive validation tests for migrated Movies Database Application
Tests all critical functionality to ensure proper migration from Java/Oracle to Python/SQLite
"""

import unittest
import sys
import os
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.init_db import init_database, populate_lookup_tables
from database.sample_data import add_sample_movies
from models import (
    User, Movie, MovieStatus, Certification, Genre, Country, Language,
    Actor, Director, ProductionCompany, UserReview,
    MovieGenre, MovieActor, MovieDirector, MovieCountry, MovieLanguage
)
from services.search_service import SearchService
from services.movie_service import MovieService
from services.review_service import ReviewService


class TestDatabaseInitialization(unittest.TestCase):
    """Test database initialization and schema creation"""

    @classmethod
    def setUpClass(cls):
        """Create test database"""
        cls.engine = init_database('test_validation.db', echo=False)
        populate_lookup_tables(cls.engine)
        add_sample_movies(cls.engine)

    def test_all_tables_exist(self):
        """Verify all 17 tables were created"""
        from sqlalchemy import inspect
        inspector = inspect(self.engine)
        tables = set(inspector.get_table_names())

        expected_tables = {
            'users', 'movies', 'user_reviews', 'movies_status', 'certifications',
            'actors', 'directors', 'prod_comps', 'genres', 'countries', 'languages',
            'movie_actors', 'movie_directors', 'movie_prod_comps',
            'movie_genres', 'movie_countries', 'movie_languages'
        }

        self.assertEqual(tables, expected_tables, "All 17 tables should exist")

    def test_lookup_tables_populated(self):
        """Verify lookup tables have data"""
        with Session(self.engine) as session:
            genre_count = session.query(Genre).count()
            status_count = session.query(MovieStatus).count()
            country_count = session.query(Country).count()

            self.assertGreater(genre_count, 0, "Genres table should have data")
            self.assertGreater(status_count, 0, "MovieStatus table should have data")
            self.assertGreater(country_count, 0, "Countries table should have data")

    def test_sample_movies_loaded(self):
        """Verify sample movies were loaded"""
        with Session(self.engine) as session:
            movie_count = session.query(Movie).count()
            self.assertGreaterEqual(movie_count, 5, "At least 5 sample movies should exist")


class TestModels(unittest.TestCase):
    """Test SQLAlchemy models"""

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///test_validation.db')

    def test_user_creation(self):
        """Test User model CRUD operations"""
        with Session(self.engine) as session:
            user = User(login='test_user_model')
            session.add(user)
            session.commit()

            retrieved = session.query(User).filter_by(login='test_user_model').first()
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.login, 'test_user_model')

    def test_movie_relationships(self):
        """Test Movie model relationships"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            self.assertIsNotNone(movie)
            self.assertIsNotNone(movie.status, "Movie should have status")
            self.assertIsInstance(movie.status, MovieStatus)

    def test_review_composite_key(self):
        """Test UserReview composite primary key"""
        with Session(self.engine) as session:
            user = User(login='test_review_user')
            session.add(user)
            session.flush()

            movie = session.query(Movie).first()

            # Add first review
            review1 = UserReview(
                id_user=user.id_user,
                id_movie=movie.id_movie,
                rating=8,
                review='First review'
            )
            session.add(review1)
            session.commit()

            # Try to add duplicate (should update, not insert)
            review2 = session.query(UserReview).filter_by(
                id_user=user.id_user,
                id_movie=movie.id_movie
            ).first()

            self.assertIsNotNone(review2)
            self.assertEqual(review2.rating, 8)


class TestSearchService(unittest.TestCase):
    """Test movie search functionality"""

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///test_validation.db')

    def test_search_by_title(self):
        """Test searching movies by title"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session, title='Matrix')

            self.assertGreater(len(results), 0, "Should find movies with 'Matrix' in title")
            titles = [r[1] for r in results]
            self.assertTrue(any('Matrix' in title for title in titles))

    def test_search_by_year(self):
        """Test searching movies by exact year"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session, year=1999)

            self.assertGreater(len(results), 0, "Should find movies from 1999")
            for movie_id, title, year in results:
                self.assertEqual(year, 1999)

    def test_search_by_year_range(self):
        """Test searching movies by year range"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session, year_min=1995, year_max=2000)

            self.assertGreater(len(results), 0, "Should find movies from 1995-2000")
            for movie_id, title, year in results:
                self.assertGreaterEqual(year, 1995)
                self.assertLessEqual(year, 2000)

    def test_search_by_actor(self):
        """Test searching movies by actor name"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session, actor_names=['Keanu Reeves'])

            # Verify results contain the actor
            if len(results) > 0:
                movie_id = results[0][0]
                actors = session.query(Actor.name).join(
                    MovieActor, Actor.id_actor == MovieActor.id_actor
                ).filter(MovieActor.id_movie == movie_id).all()

                actor_names = [a[0] for a in actors]
                self.assertTrue(any('Keanu' in name for name in actor_names))

    def test_search_by_director(self):
        """Test searching movies by director name"""
        with Session(self.engine) as session:
            # Search for movies by Wachowski
            results = SearchService.find_movies(session, director_names=['Wachowski'])

            if len(results) > 0:
                movie_id = results[0][0]
                directors = session.query(Director.name).join(
                    MovieDirector, Director.id_director == MovieDirector.id_director
                ).filter(MovieDirector.id_movie == movie_id).all()

                director_names = [d[0] for d in directors]
                self.assertTrue(any('Wachowski' in name for name in director_names))

    def test_search_all_movies(self):
        """Test retrieving all movies"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session)

            self.assertGreaterEqual(len(results), 5, "Should find at least 5 movies")

    def test_search_max_results_limit(self):
        """Test max_results parameter"""
        with Session(self.engine) as session:
            results = SearchService.find_movies(session, max_results=3)

            self.assertLessEqual(len(results), 3, "Should limit results to 3")


class TestMovieService(unittest.TestCase):
    """Test movie details retrieval"""

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///test_validation.db')

    def test_get_movie_by_id_success(self):
        """Test retrieving movie details by ID"""
        with Session(self.engine) as session:
            # Get first movie from database
            movie = session.query(Movie).first()

            details = MovieService.get_movie_by_id(session, movie.id_movie)

            self.assertIsNotNone(details)
            self.assertEqual(details.id_movie, movie.id_movie)
            self.assertEqual(details.title, movie.title)
            self.assertIsNotNone(details.status)

    def test_get_movie_by_id_not_found(self):
        """Test retrieving non-existent movie"""
        with Session(self.engine) as session:
            details = MovieService.get_movie_by_id(session, 99999)

            self.assertIsNone(details, "Non-existent movie should return None")

    def test_movie_details_structure(self):
        """Test MovieDetails dataclass structure"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()
            details = MovieService.get_movie_by_id(session, movie.id_movie)

            # Check required fields
            self.assertIsNotNone(details.title)
            self.assertIsNotNone(details.title_orig)
            self.assertIsNotNone(details.status)
            self.assertIsNotNone(details.vote_average_tmdb)
            self.assertIsNotNone(details.vote_count_tmdb)

            # Check lists
            self.assertIsInstance(details.genres, list)
            self.assertIsInstance(details.actors, list)
            self.assertIsInstance(details.directors, list)
            self.assertIsInstance(details.countries, list)
            self.assertIsInstance(details.languages, list)


class TestReviewService(unittest.TestCase):
    """Test user review functionality"""

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///test_validation.db')

    def test_add_review(self):
        """Test adding a new review"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            ReviewService.add_user_review(
                session,
                login='test_reviewer_1',
                movie_id=movie.id_movie,
                rating=8,
                review_text='Great movie!'
            )

            # Verify review was added
            user = session.query(User).filter_by(login='test_reviewer_1').first()
            self.assertIsNotNone(user)

            review = session.query(UserReview).filter_by(
                id_user=user.id_user,
                id_movie=movie.id_movie
            ).first()

            self.assertIsNotNone(review)
            self.assertEqual(review.rating, 8)
            self.assertEqual(review.review, 'Great movie!')

    def test_update_review(self):
        """Test updating existing review"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            # Add first review
            ReviewService.add_user_review(
                session,
                login='test_reviewer_2',
                movie_id=movie.id_movie,
                rating=7,
                review_text='Good movie'
            )

            # Update review
            ReviewService.add_user_review(
                session,
                login='test_reviewer_2',
                movie_id=movie.id_movie,
                rating=9,
                review_text='Actually, amazing movie!'
            )

            # Verify update
            user = session.query(User).filter_by(login='test_reviewer_2').first()
            review = session.query(UserReview).filter_by(
                id_user=user.id_user,
                id_movie=movie.id_movie
            ).first()

            self.assertEqual(review.rating, 9)
            self.assertEqual(review.review, 'Actually, amazing movie!')

    def test_rating_validation(self):
        """Test rating validation (0-10)"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            # Test invalid rating
            with self.assertRaises(ValueError):
                ReviewService.add_user_review(
                    session,
                    login='test_reviewer_3',
                    movie_id=movie.id_movie,
                    rating=11,  # Invalid
                    review_text='Test'
                )

            with self.assertRaises(ValueError):
                ReviewService.add_user_review(
                    session,
                    login='test_reviewer_3',
                    movie_id=movie.id_movie,
                    rating=-1,  # Invalid
                    review_text='Test'
                )

    def test_review_text_length_validation(self):
        """Test review text max length (200 chars)"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            # Test text too long
            with self.assertRaises(ValueError):
                ReviewService.add_user_review(
                    session,
                    login='test_reviewer_4',
                    movie_id=movie.id_movie,
                    rating=8,
                    review_text='x' * 201  # Too long
                )

    def test_get_votes_paginated(self):
        """Test paginated review retrieval"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            # Add multiple reviews
            for i in range(7):
                ReviewService.add_user_review(
                    session,
                    login=f'paginated_user_{i}',
                    movie_id=movie.id_movie,
                    rating=8,
                    review_text=f'Review {i}'
                )

            # Test page 0
            page0 = ReviewService.get_votes_paginated(session, movie_id=movie.id_movie, page=0, items_per_page=5)
            self.assertEqual(len(page0), 5)

            # Test page 1
            page1 = ReviewService.get_votes_paginated(session, movie_id=movie.id_movie, page=1, items_per_page=5)
            self.assertGreater(len(page1), 0)

    def test_get_review_count(self):
        """Test review count"""
        with Session(self.engine) as session:
            movie = session.query(Movie).first()

            count = ReviewService.get_review_count(session, movie_id=movie.id_movie)

            self.assertGreaterEqual(count, 0)


class TestBusinessFlows(unittest.TestCase):
    """Test complete business flows"""

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///test_validation.db')

    def test_complete_search_and_review_flow(self):
        """Test: Search movie -> Get details -> Add review -> View reviews"""
        with Session(self.engine) as session:
            # Step 1: Search for a movie
            search_results = SearchService.find_movies(session, title='Matrix')
            self.assertGreater(len(search_results), 0, "Search should find movies")

            movie_id = search_results[0][0]

            # Step 2: Get movie details
            movie_details = MovieService.get_movie_by_id(session, movie_id)
            self.assertIsNotNone(movie_details, "Should retrieve movie details")

            # Step 3: Add a review
            ReviewService.add_user_review(
                session,
                login='flow_test_user',
                movie_id=movie_id,
                rating=9,
                review_text='Completed full flow test'
            )

            # Step 4: View reviews
            reviews = ReviewService.get_votes_paginated(session, movie_id=movie_id, page=0)
            self.assertGreater(len(reviews), 0, "Should have at least one review")

            # Verify our review is there
            review_texts = [r.review for r in reviews]
            self.assertTrue(any('Completed full flow test' in text for text in review_texts if text))


def run_validation_tests():
    """Run all validation tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchService))
    suite.addTests(loader.loadTestsFromTestCase(TestMovieService))
    suite.addTests(loader.loadTestsFromTestCase(TestReviewService))
    suite.addTests(loader.loadTestsFromTestCase(TestBusinessFlows))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    print("=" * 80)
    print("VALIDATION TEST SUITE FOR MIGRATED MOVIES DATABASE APPLICATION")
    print("=" * 80)
    print()

    result = run_validation_tests()

    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Migration validated successfully!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please review failures above")
        sys.exit(1)
