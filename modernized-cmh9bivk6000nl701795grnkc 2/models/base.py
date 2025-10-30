# Base class for all SQLAlchemy models
# Source: All SQL CREATE TABLE statements

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all database models"""
    pass
