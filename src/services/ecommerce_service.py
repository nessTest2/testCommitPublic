# @SOURCE: main.java::class EcommerceDbService {::}
"""
E-commerce database service layer
Migrated from Java EcommerceDbService class (lines 168-366)

Provides all business logic operations for:
- Product management
- User management
- Order processing
- Inventory management
"""

from decimal import Decimal
from typing import List, Optional
import pymysql
from pymysql.cursors import DictCursor

from models.user import User
from models.product import Product
from models.order import Order
from database.connection import DatabaseConnection


class EcommerceDbService:
    """
    Database service class providing all e-commerce operations

    This class encapsulates all database operations for the e-commerce system,
    including product management, user operations, and order processing.
    """
    # @SOURCE: main.java::public EcommerceDbService(String connectionUrl, String username, String password) {::}

    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize the e-commerce database service

        Args:
            db_connection: DatabaseConnection instance for managing connections
        """
        self.db = db_connection

    # @SOURCE: main.java::public List<Product> getProducts() throws SQLException {::return products;
    def get_products(self) -> List[Product]:
        """
        Retrieve all products with their category information

        Returns:
            List of Product objects with category details

        Raises:
            pymysql.Error: If database operation fails
        """
        products = []

        query = """
            SELECT p.ProductID, p.ProductName, p.Description, p.Price,
                   p.StockQuantity, p.CategoryID, c.CategoryName
            FROM Products p
            JOIN Categories c ON p.CategoryID = c.CategoryID
        """

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in rows:
                        product = Product(
                            product_id=row['ProductID'],
                            product_name=row['ProductName'],
                            description=row['Description'],
                            price=Decimal(str(row['Price'])),
                            stock_quantity=row['StockQuantity'],
                            category_id=row['CategoryID'],
                            category_name=row['CategoryName']
                        )
                        products.append(product)

            return products

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to retrieve products: {e}")

    # @SOURCE: main.java::public User getUserById(int userId) throws SQLException {::return null;
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User object if found, None otherwise

        Raises:
            pymysql.Error: If database operation fails
        """
        query = "SELECT * FROM Users WHERE UserID = %s"

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    row = cursor.fetchone()

                    if row:
                        return User(
                            user_id=row['UserID'],
                            username=row['Username'],
                            email=row['Email'],
                            first_name=row['FirstName'],
                            last_name=row['LastName'],
                            created_at=row['CreatedAt']
                        )

            return None

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to retrieve user {user_id}: {e}")

    # @SOURCE: main.java::public int createOrder(int userId, BigDecimal totalAmount, String shippingAddress) throws SQLException {::throw new SQLException("Failed to create order, no ID obtained.");
    def create_order(self, user_id: int, total_amount: Decimal,
                     shipping_address: str) -> int:
        """
        Create a new order

        Args:
            user_id: ID of the user placing the order
            total_amount: Total order amount
            shipping_address: Shipping address for the order

        Returns:
            The ID of the newly created order

        Raises:
            pymysql.Error: If order creation fails
        """
        query = """
            INSERT INTO Orders (UserID, TotalAmount, ShippingAddress)
            VALUES (%s, %s, %s)
        """

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_id, total_amount, shipping_address))

                    # Get the last inserted ID
                    order_id = cursor.lastrowid

                    if order_id > 0:
                        conn.commit()
                        return order_id
                    else:
                        conn.rollback()
                        raise pymysql.Error("Failed to create order, no ID obtained.")

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to create order: {e}")

    # @SOURCE: main.java::public void addOrderItem(int orderId, int productId, int quantity, BigDecimal unitPrice) throws SQLException {::}
    def add_order_item(self, order_id: int, product_id: int,
                       quantity: int, unit_price: Decimal) -> None:
        """
        Add an item to an existing order

        Args:
            order_id: ID of the order
            product_id: ID of the product to add
            quantity: Quantity of the product
            unit_price: Price per unit

        Raises:
            pymysql.Error: If operation fails
        """
        query = """
            INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
            VALUES (%s, %s, %s, %s)
        """

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (order_id, product_id, quantity, unit_price))
                    conn.commit()

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to add order item: {e}")

    # @SOURCE: main.java::public void updateProductStock(int productId, int newStock) throws SQLException {::}
    def update_product_stock(self, product_id: int, new_stock: int) -> None:
        """
        Update the stock quantity for a product

        Args:
            product_id: ID of the product to update
            new_stock: New stock quantity

        Raises:
            pymysql.Error: If update fails
        """
        query = "UPDATE Products SET StockQuantity = %s WHERE ProductID = %s"

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (new_stock, product_id))
                    conn.commit()

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to update product stock: {e}")

    # @SOURCE: main.java::public List<Order> getOrdersByUser(int userId) throws SQLException {::return orders;
    def get_orders_by_user(self, user_id: int) -> List[Order]:
        """
        Retrieve all orders for a specific user

        Args:
            user_id: ID of the user

        Returns:
            List of Order objects for the user, ordered by date descending

        Raises:
            pymysql.Error: If database operation fails
        """
        orders = []

        query = "SELECT * FROM Orders WHERE UserID = %s ORDER BY OrderDate DESC"

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (user_id,))
                    rows = cursor.fetchall()

                    for row in rows:
                        order = Order(
                            order_id=row['OrderID'],
                            user_id=row['UserID'],
                            order_date=row['OrderDate'],
                            total_amount=Decimal(str(row['TotalAmount'])),
                            status=row['Status'],
                            shipping_address=row['ShippingAddress']
                        )
                        orders.append(order)

            return orders

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to retrieve orders for user {user_id}: {e}")

    # @SOURCE: main.java::public List<Product> getProductsByCategory(int categoryId) throws SQLException {::return products;
    def get_products_by_category(self, category_id: int) -> List[Product]:
        """
        Retrieve all products in a specific category

        Args:
            category_id: ID of the category

        Returns:
            List of Product objects in the specified category

        Raises:
            pymysql.Error: If database operation fails
        """
        products = []

        query = """
            SELECT p.ProductID, p.ProductName, p.Description, p.Price,
                   p.StockQuantity, p.CategoryID, c.CategoryName
            FROM Products p
            JOIN Categories c ON p.CategoryID = c.CategoryID
            WHERE p.CategoryID = %s
        """

        try:
            with self.db.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (category_id,))
                    rows = cursor.fetchall()

                    for row in rows:
                        product = Product(
                            product_id=row['ProductID'],
                            product_name=row['ProductName'],
                            description=row['Description'],
                            price=Decimal(str(row['Price'])),
                            stock_quantity=row['StockQuantity'],
                            category_id=row['CategoryID'],
                            category_name=row['CategoryName']
                        )
                        products.append(product)

            return products

        except pymysql.Error as e:
            raise pymysql.Error(f"Failed to retrieve products for category {category_id}: {e}")
