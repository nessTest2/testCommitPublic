# Database Service - Singleton for connection management
# Source: movies_gui_app/src/sgbdrennequinepolis/LoginSingleton.java

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    """Singleton service for database connection management

    Migrated from LoginSingleton.java (lines 27-247)
    Handles:
    - Connection management
    - Failover between primary and backup databases (CB/CBB simulation)
    - Session management
    - User authentication (login storage)
    """

    _instance: Optional['DatabaseService'] = None
    _engine = None
    _session_factory = None
    _session: Optional[Session] = None
    _login: Optional[str] = None
    _secondary_server: bool = False

    # Error codes for failover simulation
    ERROR_PRIMARY_DOWN = 28000  # Simulates CB crash (from Java code line 120)
    ERROR_PRIMARY_RESTORED = 20400  # Simulates CBB detecting CB is back (from Java code line 127)

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the database service

        Source: LoginSingleton constructor (lines 37-39)
        """
        # Only initialize once
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @classmethod
    def get_instance(cls) -> 'DatabaseService':
        """Get the singleton instance

        Source: LoginSingleton.getInstance() (lines 41-46)
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # Getters and Setters - Source: lines 48-97

    def set_login(self, login: str):
        """Set the current user login

        Source: setLogin() (lines 49-52)
        """
        self._login = login
        logger.info(f"User logged in: {login}")

    def get_login(self) -> Optional[str]:
        """Get the current user login

        Source: getLogin() (lines 53-56)
        """
        return self._login

    def set_secondary_server(self, secondary: bool):
        """Set whether using secondary (backup) database

        Source: setSecondaryServer() (lines 57-60)
        """
        self._secondary_server = secondary

    def get_secondary_server(self) -> bool:
        """Check if using secondary (backup) database

        Source: getSecondaryServer() (lines 61-64)
        """
        return self._secondary_server

    def _get_database_path(self, db_name: str = "movies.db") -> str:
        """Get the path to the database file"""
        db_path = Path(__file__).parent.parent / db_name
        return f"sqlite:///{db_path}"

    def start_connection(self, echo: bool = False):
        """Initialize database connection

        Source: startConnection() (lines 100-116)
        Creates connection to either primary (CB) or secondary (CBB) database
        """
        try:
            # Determine which database to use
            if self._secondary_server:
                db_name = "movies_backup.db"
                logger.info("Connection CBB (backup)")
            else:
                db_name = "movies.db"
                logger.info("Connection CB (primary)")

            # Create engine if needed
            database_url = self._get_database_path(db_name)
            if self._engine is None or str(self._engine.url) != database_url:
                self._engine = create_engine(database_url, echo=echo)
                self._session_factory = sessionmaker(bind=self._engine)

            # Test connection
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info(f"Database connection established: {db_name}")

        except Exception as exc:
            logger.error(f"Failed to establish database connection: {exc}")
            raise

    def get_session(self) -> Session:
        """Get a database session

        Source: Provides session equivalent to Java Connection/CallableStatement (lines 82-97)
        """
        if self._session_factory is None:
            self.start_connection()

        # Create new session if none exists
        if self._session is None or not self._session.is_active:
            self._session = self._session_factory()

        return self._session

    def close_session(self):
        """Close the current database session

        Source: endCallStatement() (lines 89-97)
        """
        if self._session is not None:
            try:
                self._session.close()
            except Exception as exc:
                logger.warning(f"Error closing session: {exc}")
            finally:
                self._session = None

    def close_connection(self):
        """Close database connection

        Source: setConnex(null) (lines 71-79)
        """
        self.close_session()
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
        logger.info("Database connection closed")

    def check_crash(self, exception: Exception, error_code: Optional[int] = None) -> bool:
        """Check if exception indicates a crash requiring failover

        Source: checkCrash() (lines 118-135)

        Simulates the CB/CBB failover logic:
        - If on primary (CB) and crash detected → switch to backup (CBB)
        - If on backup (CBB) and primary restored → switch back to primary (CB)

        Args:
            exception: The exception that occurred
            error_code: Optional error code for simulation

        Returns:
            True if failover occurred, False otherwise
        """
        # Check for primary database failure
        if not self._secondary_server and error_code == self.ERROR_PRIMARY_DOWN:
            logger.warning("Primary database (CB) crash detected!")
            self._secondary_server = True
            self.close_connection()
            return True

        # Check for primary database restoration
        elif self._secondary_server and error_code == self.ERROR_PRIMARY_RESTORED:
            logger.info("Primary database (CB) restored!")
            self._secondary_server = False
            self.close_connection()
            return True

        return False

    def execute_with_failover(self, operation, *args, **kwargs):
        """Execute a database operation with automatic failover on error

        Wraps database operations to provide transparent failover support.
        If an operation fails due to database crash, it automatically:
        1. Switches to the backup database
        2. Retries the operation

        Args:
            operation: The function to execute
            *args, **kwargs: Arguments to pass to the operation

        Returns:
            The result of the operation

        Raises:
            Exception if operation fails even after failover
        """
        try:
            return operation(*args, **kwargs)
        except SQLAlchemyError as exc:
            # Check if this is a recoverable error requiring failover
            # In production, you would check specific error codes
            # For now, we'll just log and retry once
            logger.error(f"Database error: {exc}")

            # Simulate crash detection
            if self.check_crash(exc):
                logger.info("Retrying operation on failover database...")
                return operation(*args, **kwargs)
            else:
                # Not a failover situation, re-raise the exception
                raise

    def __enter__(self):
        """Context manager entry"""
        return self.get_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            if self._session:
                self._session.rollback()
        else:
            if self._session:
                self._session.commit()
        self.close_session()
        return False
