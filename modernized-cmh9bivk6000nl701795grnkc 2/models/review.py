# User Review model
# Source: movies_sql_procedures/base_tables/create_base_tables.sql lines 34-46

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

from .base import Base

class UserReview(Base):
    """User reviews/ratings for movies

    Original SQL:
    CREATE TABLE USER_REVIEWS (
        IdUser INTEGER CONSTRAINT USER_REVIEWS_IDUSER_FK REFERENCES USERS(IdUser) ON DELETE CASCADE,
        IdMovie NUMBER(6),
        ReviewDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP CONSTRAINT USER_REVIEWS_DATEEVAL_NN NOT NULL,
        Rating INTEGER CONSTRAINT USER_REVIEWS_RATING_NN NOT NULL CONSTRAINT USER_REVIEWS_RATING_CH CHECK(Rating >= 0 AND Rating <= 10),
        Review VARCHAR2(200),
        SyncToken CHAR(1) DEFAULT 0 CONSTRAINT USER_REVIEWS_SYNCTOKEN_NN NOT NULL,
        CONSTRAINT USER_REVIEWS_PK PRIMARY KEY(IdUser, IdMovie)
    );
    """
    __tablename__ = 'user_reviews'

    # Composite primary key (Foreign keys)
    id_user: Mapped[int] = mapped_column('IdUser', Integer, ForeignKey('users.IdUser', ondelete='CASCADE'), primary_key=True)
    id_movie: Mapped[int] = mapped_column('IdMovie', Integer, ForeignKey('movies.IdMovie', ondelete='CASCADE'), primary_key=True)

    # Attributes
    review_date: Mapped[datetime] = mapped_column('ReviewDate', DateTime, nullable=False, server_default=func.current_timestamp())
    rating: Mapped[int] = mapped_column('Rating', Integer, nullable=False)
    review: Mapped[Optional[str]] = mapped_column('Review', String(200), nullable=True)
    sync_token: Mapped[str] = mapped_column('SyncToken', String(1), nullable=False, default='0')

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews")

    # Table constraints
    __table_args__ = (
        CheckConstraint('Rating >= 0 AND Rating <= 10', name='user_reviews_rating_ch'),
    )

    def __repr__(self) -> str:
        return f"UserReview(user_id={self.id_user!r}, movie_id={self.id_movie!r}, rating={self.rating!r})"
