# @SOURCE: main.java::class EcommerceDbService {::private Connection getConnection()
"""
Database connection management module
"""

from .connection import DatabaseConnection, get_connection

__all__ = ['DatabaseConnection', 'get_connection']
