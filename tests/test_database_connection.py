"""
Unit tests for database connection module
Tests DatabaseConnection class and get_connection factory
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import Mock, patch, MagicMock
import pymysql

from database.connection import DatabaseConnection, get_connection


class TestDatabaseConnection:
    """Test cases for DatabaseConnection class"""

    def test_initialization_with_defaults(self):
        """Test DatabaseConnection initialization with default values"""
        db = DatabaseConnection()

        assert db.host == 'localhost'
        assert db.port == 3306
        assert db.database == 'EcommerceDB'
        assert db.user == 'root'
        assert db.password == 'password'

    def test_initialization_with_custom_values(self):
        """Test DatabaseConnection initialization with custom values"""
        db = DatabaseConnection(
            host='db.example.com',
            port=3307,
            database='TestDB',
            user='testuser',
            password='testpass'
        )

        assert db.host == 'db.example.com'
        assert db.port == 3307
        assert db.database == 'TestDB'
        assert db.user == 'testuser'
        assert db.password == 'testpass'

    @patch('database.connection.pymysql.connect')
    def test_get_connection_success(self, mock_connect):
        """Test successful database connection"""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()
        conn = db.get_connection()

        assert conn == mock_connection
        mock_connect.assert_called_once_with(
            host='localhost',
            port=3306,
            database='EcommerceDB',
            user='root',
            password='password',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

    @patch('database.connection.pymysql.connect')
    def test_get_connection_failure(self, mock_connect):
        """Test database connection failure"""
        mock_connect.side_effect = pymysql.Error("Connection failed")

        db = DatabaseConnection()

        with pytest.raises(pymysql.Error) as exc_info:
            db.get_connection()

        assert "Failed to connect to database" in str(exc_info.value)

    @patch('database.connection.pymysql.connect')
    def test_connection_context_manager_success(self, mock_connect):
        """Test context manager for successful connection"""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()

        with db.connection() as conn:
            assert conn == mock_connection

        mock_connection.close.assert_called_once()

    @patch('database.connection.pymysql.connect')
    def test_connection_context_manager_rollback_on_error(self, mock_connect):
        """Test context manager rollback on database error"""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()

        # Test that pymysql.Error triggers rollback
        with pytest.raises(pymysql.Error):
            with db.connection() as conn:
                raise pymysql.Error("Database error")

        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('database.connection.pymysql.connect')
    def test_connection_context_manager_closes_on_other_error(self, mock_connect):
        """Test context manager closes connection on non-database error"""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        db = DatabaseConnection()

        # Test that non-database errors still close the connection
        with pytest.raises(RuntimeError):
            with db.connection() as conn:
                raise RuntimeError("Test error")

        # Rollback should NOT be called for non-database errors
        mock_connection.rollback.assert_not_called()
        # But connection should still be closed
        mock_connection.close.assert_called_once()


class TestGetConnectionFactory:
    """Test cases for get_connection factory function"""

    def test_get_connection_with_defaults(self):
        """Test get_connection factory with default values"""
        db = get_connection()

        assert db.host == 'localhost'
        assert db.port == 3306
        assert db.database == 'EcommerceDB'
        assert db.user == 'root'
        assert db.password == 'password'

    def test_get_connection_with_custom_values(self):
        """Test get_connection factory with custom values"""
        db = get_connection(
            host='custom.host',
            port=3307,
            database='CustomDB',
            user='customuser',
            password='custompass'
        )

        assert db.host == 'custom.host'
        assert db.port == 3307
        assert db.database == 'CustomDB'
        assert db.user == 'customuser'
        assert db.password == 'custompass'

    @patch.dict(os.environ, {
        'DB_HOST': 'env.host',
        'DB_PORT': '3308',
        'DB_NAME': 'EnvDB',
        'DB_USER': 'envuser',
        'DB_PASSWORD': 'envpass'
    })
    def test_get_connection_with_environment_variables(self):
        """Test get_connection factory with environment variables"""
        db = get_connection()

        assert db.host == 'env.host'
        assert db.port == 3308
        assert db.database == 'EnvDB'
        assert db.user == 'envuser'
        assert db.password == 'envpass'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
