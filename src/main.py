#!/usr/bin/env python3
# @SOURCE: main.java::public class EcommerceApplication {::}
"""
E-commerce Application Main Entry Point
Migrated from Java EcommerceApplication class (lines 369-432)

This module demonstrates all functionality of the e-commerce system:
- Product catalog retrieval
- User information management
- Order creation and management
- Category-based product filtering
"""

import sys
from decimal import Decimal
from typing import NoReturn

from database.connection import get_connection
from services.ecommerce_service import EcommerceDbService


def print_section_header(title: str) -> None:
    """Print a formatted section header"""
    print(f"\n=== {title} ===")


def main() -> int:
    """
    Main application entry point

    Demonstrates all e-commerce operations:
    1. Retrieve and display all products
    2. Get user information
    3. Create a new order
    4. Add items to the order
    5. Retrieve user's order history
    6. Filter products by category

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # @SOURCE: main.java::String connectionUrl = "jdbc:mysql://localhost:3306/EcommerceDB";::String dbPassword = "password";
    # Database connection is now handled through environment variables
    # or defaults in the get_connection() function

    try:
        # @SOURCE: main.java::EcommerceDbService service = new EcommerceDbService(connectionUrl, dbUsername, dbPassword);::EcommerceDbService service = new EcommerceDbService(connectionUrl, dbUsername, dbPassword);
        # Initialize database connection and service
        db_connection = get_connection()
        service = EcommerceDbService(db_connection)

        # @SOURCE: main.java::System.out.println("=== Products ===");::);
        # Get all products
        print_section_header("Products")
        products = service.get_products()
        for product in products:
            print(f"{product.product_name} - ${product.price} "
                  f"({product.category_name})")

        # @SOURCE: main.java::System.out.println("\n=== User Info ===");::}
        # Get user by ID
        print_section_header("User Info")
        user = service.get_user_by_id(1)
        if user:
            print(f"User: {user.first_name} {user.last_name} "
                  f"({user.email})")
        else:
            print("User not found")

        # @SOURCE: main.java::System.out.println("\n=== Creating Order ===");::System.out.println("Created order with ID: " + orderId);
        # Create a new order
        print_section_header("Creating Order")
        order_id = service.create_order(
            user_id=1,
            total_amount=Decimal("1049.98"),
            shipping_address="123 Main St, City, State"
        )
        print(f"Created order with ID: {order_id}")

        # @SOURCE: main.java::service.addOrderItem(orderId, 1, 1, new BigDecimal("999.99"));::System.out.println("Added items to order");
        # Add order items
        service.add_order_item(order_id, 1, 1, Decimal("999.99"))  # Laptop
        service.add_order_item(order_id, 2, 1, Decimal("49.99"))   # Book
        print("Added items to order")

        # @SOURCE: main.java::System.out.println("\n=== User Orders ===");::);
        # Get user orders
        print_section_header("User Orders")
        user_orders = service.get_orders_by_user(1)
        for order in user_orders:
            print(f"Order #{order.order_id}: ${order.total_amount} "
                  f"- {order.status}")

        # @SOURCE: main.java::System.out.println("\n=== Electronics Products ===");::);
        # Get products by category
        print_section_header("Electronics Products")
        electronics = service.get_products_by_category(1)
        for product in electronics:
            print(f"{product.product_name} - ${product.price} "
                  f"(Stock: {product.stock_quantity})")

        return 0

    # @SOURCE: main.java::} catch (ClassNotFoundException e) {::}
    except ImportError as e:
        print(f"Import error: {e}", file=sys.stderr)
        print("Make sure all required packages are installed (pymysql)", file=sys.stderr)
        return 1

    # @SOURCE: main.java::} catch (SQLException e) {::}
    except Exception as e:
        # Catch all database and general errors
        error_type = type(e).__name__
        print(f"{error_type}: {e}", file=sys.stderr)
        return 1


# @SOURCE: main.java::public static void main(String[] args) {::}
if __name__ == "__main__":
    """
    Application entry point when run as a script
    """
    sys.exit(main())
