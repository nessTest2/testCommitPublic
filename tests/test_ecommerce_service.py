"""
Unit tests for ecommerce service
Tests EcommerceDbService class methods
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import Mock, MagicMock, patch
from decimal import Decimal
from datetime import datetime

from services.ecommerce_service import EcommerceDbService
from models.user import User
from models.product import Product
from models.order import Order


class TestEcommerceDbService:
    """Test cases for EcommerceDbService"""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database connection"""
        mock_db = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()

        # Setup context managers
        mock_db.connection.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_db.connection.return_value.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        mock_cursor.fetchall = Mock()
        mock_cursor.fetchone = Mock()
        mock_cursor.execute = Mock()
        mock_conn.commit = Mock()
        mock_conn.rollback = Mock()

        return mock_db, mock_conn, mock_cursor

    def test_get_products_success(self, mock_db):
        """Test successful retrieval of products"""
        db_mock, conn_mock, cursor_mock = mock_db

        # Mock database response
        cursor_mock.fetchall.return_value = [
            {
                'ProductID': 1,
                'ProductName': 'Laptop',
                'Description': 'High-performance laptop',
                'Price': Decimal('999.99'),
                'StockQuantity': 10,
                'CategoryID': 1,
                'CategoryName': 'Electronics'
            }
        ]

        service = EcommerceDbService(db_mock)
        products = service.get_products()

        assert len(products) == 1
        assert products[0].product_id == 1
        assert products[0].product_name == 'Laptop'
        assert products[0].price == Decimal('999.99')
        assert products[0].category_name == 'Electronics'

    def test_get_products_empty_result(self, mock_db):
        """Test get_products with no results"""
        db_mock, conn_mock, cursor_mock = mock_db
        cursor_mock.fetchall.return_value = []

        service = EcommerceDbService(db_mock)
        products = service.get_products()

        assert len(products) == 0

    def test_get_user_by_id_success(self, mock_db):
        """Test successful retrieval of user by ID"""
        db_mock, conn_mock, cursor_mock = mock_db

        # Mock database response
        cursor_mock.fetchone.return_value = {
            'UserID': 1,
            'Username': 'john_doe',
            'Email': 'john@example.com',
            'FirstName': 'John',
            'LastName': 'Doe',
            'CreatedAt': datetime(2024, 1, 1, 12, 0, 0)
        }

        service = EcommerceDbService(db_mock)
        user = service.get_user_by_id(1)

        assert user is not None
        assert user.user_id == 1
        assert user.username == 'john_doe'
        assert user.email == 'john@example.com'
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'

    def test_get_user_by_id_not_found(self, mock_db):
        """Test get_user_by_id when user doesn't exist"""
        db_mock, conn_mock, cursor_mock = mock_db
        cursor_mock.fetchone.return_value = None

        service = EcommerceDbService(db_mock)
        user = service.get_user_by_id(999)

        assert user is None

    def test_create_order_success(self, mock_db):
        """Test successful order creation"""
        db_mock, conn_mock, cursor_mock = mock_db
        cursor_mock.lastrowid = 123

        service = EcommerceDbService(db_mock)
        order_id = service.create_order(
            user_id=1,
            total_amount=Decimal("1049.98"),
            shipping_address="123 Main St"
        )

        assert order_id == 123
        cursor_mock.execute.assert_called_once()
        conn_mock.commit.assert_called_once()

    def test_create_order_failure(self, mock_db):
        """Test order creation failure"""
        db_mock, conn_mock, cursor_mock = mock_db
        cursor_mock.lastrowid = 0

        service = EcommerceDbService(db_mock)

        with pytest.raises(Exception):
            service.create_order(
                user_id=1,
                total_amount=Decimal("1049.98"),
                shipping_address="123 Main St"
            )

    def test_add_order_item_success(self, mock_db):
        """Test successful addition of order item"""
        db_mock, conn_mock, cursor_mock = mock_db

        service = EcommerceDbService(db_mock)
        service.add_order_item(
            order_id=1,
            product_id=1,
            quantity=2,
            unit_price=Decimal("999.99")
        )

        cursor_mock.execute.assert_called_once()
        conn_mock.commit.assert_called_once()

    def test_update_product_stock_success(self, mock_db):
        """Test successful product stock update"""
        db_mock, conn_mock, cursor_mock = mock_db

        service = EcommerceDbService(db_mock)
        service.update_product_stock(product_id=1, new_stock=50)

        cursor_mock.execute.assert_called_once()
        conn_mock.commit.assert_called_once()

    def test_get_orders_by_user_success(self, mock_db):
        """Test successful retrieval of user orders"""
        db_mock, conn_mock, cursor_mock = mock_db

        # Mock database response
        cursor_mock.fetchall.return_value = [
            {
                'OrderID': 1,
                'UserID': 1,
                'OrderDate': datetime(2024, 1, 1, 12, 0, 0),
                'TotalAmount': Decimal('1049.98'),
                'Status': 'Pending',
                'ShippingAddress': '123 Main St'
            }
        ]

        service = EcommerceDbService(db_mock)
        orders = service.get_orders_by_user(1)

        assert len(orders) == 1
        assert orders[0].order_id == 1
        assert orders[0].user_id == 1
        assert orders[0].total_amount == Decimal('1049.98')
        assert orders[0].status == 'Pending'

    def test_get_products_by_category_success(self, mock_db):
        """Test successful retrieval of products by category"""
        db_mock, conn_mock, cursor_mock = mock_db

        # Mock database response
        cursor_mock.fetchall.return_value = [
            {
                'ProductID': 1,
                'ProductName': 'Laptop',
                'Description': 'High-performance laptop',
                'Price': Decimal('999.99'),
                'StockQuantity': 10,
                'CategoryID': 1,
                'CategoryName': 'Electronics'
            }
        ]

        service = EcommerceDbService(db_mock)
        products = service.get_products_by_category(1)

        assert len(products) == 1
        assert products[0].category_id == 1
        assert products[0].category_name == 'Electronics'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
