# @SOURCE: main.java::private Connection getConnection() throws SQLException {::}
"""
Database connection management with context manager support
Migrated from Java JDBC connection handling (lines 168-181)
"""

import os
from contextlib import contextmanager
from typing import Optional, Generator
import pymysql
from pymysql.cursors import DictCursor


class DatabaseConnection:
    """
    Database connection manager for MySQL

    Manages connection pooling and provides context manager interface
    for automatic resource cleanup (equivalent to Java's try-with-resources)
    """
    # @SOURCE: main.java::private final String connectionUrl;::private final String password;

    def __init__(self, host: str = 'localhost', port: int = 3306,
                 database: str = 'EcommerceDB', user: str = 'root',
                 password: str = 'password'):
        """
        Initialize database connection parameters

        Args:
            host: Database host address
            port: Database port
            database: Database name
            user: Database username
            password: Database password
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._connection: Optional[pymysql.Connection] = None

    # @SOURCE: main.java::private Connection getConnection() throws SQLException {::return DriverManager.getConnection(connectionUrl, username, password);
    def get_connection(self) -> pymysql.Connection:
        """
        Get a database connection

        Returns:
            Active database connection

        Raises:
            pymysql.Error: If connection fails
        """
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                charset='utf8mb4',
                cursorclass=DictCursor,
                autocommit=False
            )
            return connection
        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to connect to database: {e}")

    @contextmanager
    def connection(self) -> Generator[pymysql.Connection, None, None]:
        """
        Context manager for database connections (Python's try-with-resources)

        Yields:
            Active database connection

        Example:
            with db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users")
        """
        conn = None
        try:
            conn = self.get_connection()
            yield conn
        except pymysql.Error as e:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def cursor(self, connection: pymysql.Connection) -> Generator[pymysql.cursors.Cursor, None, None]:
        """
        Context manager for cursors

        Args:
            connection: Active database connection

        Yields:
            Database cursor
        """
        cursor = None
        try:
            cursor = connection.cursor()
            yield cursor
        finally:
            if cursor:
                cursor.close()


# @SOURCE: main.java::EcommerceDbService service = new EcommerceDbService(connectionUrl, dbUsername, dbPassword);::EcommerceDbService service = new EcommerceDbService(connectionUrl, dbUsername, dbPassword);
def get_connection(host: str = None, port: int = None, database: str = None,
                   user: str = None, password: str = None) -> DatabaseConnection:
    """
    Factory function to create DatabaseConnection with environment variable support

    Args:
        host: Database host (defaults to env DB_HOST or 'localhost')
        port: Database port (defaults to env DB_PORT or 3306)
        database: Database name (defaults to env DB_NAME or 'EcommerceDB')
        user: Database user (defaults to env DB_USER or 'root')
        password: Database password (defaults to env DB_PASSWORD or 'password')

    Returns:
        DatabaseConnection instance
    """
    return DatabaseConnection(
        host=host or os.getenv('DB_HOST', 'localhost'),
        port=port or int(os.getenv('DB_PORT', '3306')),
        database=database or os.getenv('DB_NAME', 'EcommerceDB'),
        user=user or os.getenv('DB_USER', 'root'),
        password=password or os.getenv('DB_PASSWORD', 'password')
    )
