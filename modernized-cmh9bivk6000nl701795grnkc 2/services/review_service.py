# Review Service - User review management
# Source: movies_sql_procedures/cb/eval_movies/eval_movies.sql (EVAL_PACKAGE.AddUserReview)
# and find_movies.sql (SEARCH_PACKAGE.GetVotes)
# and LoginSingleton.java writeVoteRequest(), showVotesRequest() (lines 210-246)

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

from models import User, UserReview

logger = logging.getLogger(__name__)

@dataclass
class ReviewItem:
    """Review item data class

    Equivalent to VoteListItem_t custom Oracle type (find_movies.sql lines 10-17)
    """
    id_user: int
    login: str
    review_date: datetime
    rating: int
    review: str

class ReviewService:
    """Service for managing user reviews

    Migrated from EVAL_PACKAGE and SEARCH_PACKAGE PL/SQL procedures
    """

    @staticmethod
    def add_user_review(
        session: Session,
        login: str,
        movie_id: int,
        rating: int,
        review_text: str = None
    ) -> None:
        """Add or update a user review

        Source: EVAL_PACKAGE.AddUserReview (eval_movies.sql)
        and LoginSingleton.writeVoteRequest() (LoginSingleton.java lines 210-223)

        Args:
            session: Database session
            login: User login (username)
            movie_id: Movie ID to review
            rating: Rating score (0-10)
            review_text: Optional review text (max 200 characters)

        Raises:
            ValueError: If rating is out of range or review text too long
        """
        logger.info(f"Adding review: user={login}, movie={movie_id}, rating={rating}")

        # Validate rating
        # Source: create_base_tables.sql line 41 - CHECK constraint
        if not (0 <= rating <= 10):
            raise ValueError(f"Rating must be between 0 and 10, got {rating}")

        # Validate review text length
        # Source: create_base_tables.sql line 42 - VARCHAR2(200)
        if review_text and len(review_text) > 200:
            raise ValueError(f"Review text must be at most 200 characters, got {len(review_text)}")

        # Get or create user
        user = session.query(User).filter(User.login == login).first()
        if not user:
            user = User(login=login)
            session.add(user)
            session.flush()  # Get the user ID

        # Check if review already exists
        # Source: create_base_tables.sql line 45 - PRIMARY KEY(IdUser, IdMovie)
        existing_review = session.query(UserReview).filter(
            UserReview.id_user == user.id_user,
            UserReview.id_movie == movie_id
        ).first()

        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.review = review_text
            existing_review.review_date = func.current_timestamp()
            logger.info(f"Updated existing review for user {login}")
        else:
            # Create new review
            # Source: create_base_tables.sql lines 34-46
            new_review = UserReview(
                id_user=user.id_user,
                id_movie=movie_id,
                rating=rating,
                review=review_text
            )
            session.add(new_review)
            logger.info(f"Created new review for user {login}")

        session.commit()

    @staticmethod
    def get_votes_paginated(
        session: Session,
        movie_id: int,
        page: int = 0,
        items_per_page: int = 5
    ) -> List[ReviewItem]:
        """Get paginated user reviews for a movie

        Source: SEARCH_PACKAGE.GetVotes (find_movies.sql - GetVotes procedure)
        and LoginSingleton.showVotesRequest() (LoginSingleton.java lines 225-246)

        Args:
            session: Database session
            movie_id: Movie ID to get reviews for
            page: Page number (0-indexed)
            items_per_page: Number of reviews per page (default 5, from DialogShowVotes.java)

        Returns:
            List of ReviewItem objects for the requested page
        """
        logger.info(f"Getting reviews: movie={movie_id}, page={page}")

        # Calculate offset
        offset = page * items_per_page

        # Query reviews with pagination
        # Source: find_movies.sql GetVotes procedure
        reviews_query = session.query(
            User.id_user,
            User.login,
            UserReview.review_date,
            UserReview.rating,
            UserReview.review
        ).join(
            User, UserReview.id_user == User.id_user
        ).filter(
            UserReview.id_movie == movie_id
        ).order_by(
            UserReview.review_date.desc()  # Most recent first
        ).offset(offset).limit(items_per_page).all()

        # Convert to ReviewItem objects
        # Source: find_movies.sql lines 10-17 - VoteListItem_t type
        review_items = [
            ReviewItem(
                id_user=r.id_user,
                login=r.login,
                review_date=r.review_date,
                rating=r.rating,
                review=r.review or ""  # Handle NULL reviews
            )
            for r in reviews_query
        ]

        logger.info(f"Retrieved {len(review_items)} reviews for page {page}")
        return review_items

    @staticmethod
    def get_review_count(session: Session, movie_id: int) -> int:
        """Get total count of reviews for a movie

        Used for pagination calculations.

        Args:
            session: Database session
            movie_id: Movie ID

        Returns:
            Total number of reviews
        """
        count = session.query(func.count(UserReview.id_user)).filter(
            UserReview.id_movie == movie_id
        ).scalar()
        return count or 0
