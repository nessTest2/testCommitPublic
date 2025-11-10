"""
Unit tests for data model classes
Tests User, Product, and Order models
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from datetime import datetime
from decimal import Decimal

from models.user import User
from models.product import Product
from models.order import Order


class TestUser:
    """Test cases for User model"""

    def test_user_creation_with_all_fields(self):
        """Test creating a user with all fields specified"""
        created_at = datetime(2024, 1, 1, 12, 0, 0)
        user = User(
            user_id=1,
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            created_at=created_at
        )

        assert user.user_id == 1
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.created_at == created_at

    def test_user_default_values(self):
        """Test user creation with default values"""
        user = User()

        assert user.user_id == 0
        assert user.username == ""
        assert user.email == ""
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.created_at is not None

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User(
            user_id=1,
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )

        str_repr = str(user)
        assert "User{" in str_repr
        assert "userId=1" in str_repr
        assert "username='john_doe'" in str_repr
        assert "email='john@example.com'" in str_repr


class TestProduct:
    """Test cases for Product model"""

    def test_product_creation_with_all_fields(self):
        """Test creating a product with all fields specified"""
        product = Product(
            product_id=1,
            product_name="Laptop",
            description="High-performance laptop",
            price=Decimal("999.99"),
            stock_quantity=10,
            category_id=1,
            category_name="Electronics"
        )

        assert product.product_id == 1
        assert product.product_name == "Laptop"
        assert product.description == "High-performance laptop"
        assert product.price == Decimal("999.99")
        assert product.stock_quantity == 10
        assert product.category_id == 1
        assert product.category_name == "Electronics"

    def test_product_price_conversion_to_decimal(self):
        """Test that price is converted to Decimal"""
        product = Product(price=99.99)

        assert isinstance(product.price, Decimal)
        assert product.price == Decimal("99.99")

    def test_product_formatted_price(self):
        """Test formatted price method"""
        product = Product(price=Decimal("999.99"))

        assert product.get_formatted_price() == "$999.99"

    def test_product_is_in_stock(self):
        """Test stock availability check"""
        in_stock = Product(stock_quantity=10)
        out_of_stock = Product(stock_quantity=0)

        assert in_stock.is_in_stock() is True
        assert out_of_stock.is_in_stock() is False

    def test_product_str_representation(self):
        """Test product string representation"""
        product = Product(
            product_id=1,
            product_name="Laptop",
            price=Decimal("999.99"),
            stock_quantity=10,
            category_name="Electronics"
        )

        str_repr = str(product)
        assert "Product{" in str_repr
        assert "productId=1" in str_repr
        assert "productName='Laptop'" in str_repr
        assert "price=999.99" in str_repr


class TestOrder:
    """Test cases for Order model"""

    def test_order_creation_with_all_fields(self):
        """Test creating an order with all fields specified"""
        order_date = datetime(2024, 1, 1, 12, 0, 0)
        order = Order(
            order_id=1,
            user_id=1,
            order_date=order_date,
            total_amount=Decimal("1049.98"),
            status="Pending",
            shipping_address="123 Main St, City, State"
        )

        assert order.order_id == 1
        assert order.user_id == 1
        assert order.order_date == order_date
        assert order.total_amount == Decimal("1049.98")
        assert order.status == "Pending"
        assert order.shipping_address == "123 Main St, City, State"

    def test_order_default_values(self):
        """Test order creation with default values"""
        order = Order()

        assert order.order_id == 0
        assert order.user_id == 0
        assert order.order_date is not None
        assert order.total_amount == Decimal("0.00")
        assert order.status == "Pending"
        assert order.shipping_address == ""

    def test_order_total_conversion_to_decimal(self):
        """Test that total_amount is converted to Decimal"""
        order = Order(total_amount=1049.98)

        assert isinstance(order.total_amount, Decimal)
        assert order.total_amount == Decimal("1049.98")

    def test_order_formatted_total(self):
        """Test formatted total method"""
        order = Order(total_amount=Decimal("1049.98"))

        assert order.get_formatted_total() == "$1049.98"

    def test_order_is_completed(self):
        """Test completed status check"""
        completed_order = Order(status="Delivered")
        pending_order = Order(status="Pending")

        assert completed_order.is_completed() is True
        assert pending_order.is_completed() is False

    def test_order_str_representation(self):
        """Test order string representation"""
        order = Order(
            order_id=1,
            user_id=1,
            total_amount=Decimal("1049.98"),
            status="Pending"
        )

        str_repr = str(order)
        assert "Order{" in str_repr
        assert "orderId=1" in str_repr
        assert "userId=1" in str_repr
        assert "totalAmount=1049.98" in str_repr


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
