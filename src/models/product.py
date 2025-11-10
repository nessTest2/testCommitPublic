# @SOURCE: main.java::class Product {::}
"""
Product model representing catalog items
Migrated from Java Product class (lines 58-113)
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Product:
    """
    Product data model with pricing and inventory information

    Attributes:
        product_id: Unique product identifier
        product_name: Name of the product
        description: Product description
        price: Product price (using Decimal for precision)
        stock_quantity: Available inventory count
        category_id: Foreign key to category
        category_name: Name of the product category
    """
    # @SOURCE: main.java::private int productId;::private String categoryName;
    product_id: int = 0
    product_name: str = ""
    description: str = ""
    price: Decimal = Decimal('0.00')
    stock_quantity: int = 0
    category_id: int = 0
    category_name: str = ""

    def __post_init__(self):
        """Ensure price is a Decimal for precision"""
        if not isinstance(self.price, Decimal):
            self.price = Decimal(str(self.price))

    # @SOURCE: main.java::public String toString() {::}
    def __str__(self) -> str:
        """String representation of Product object"""
        return (f"Product{{productId={self.product_id}, productName='{self.product_name}', "
                f"price={self.price}, stockQuantity={self.stock_quantity}, "
                f"categoryName='{self.category_name}'}}")

    def __repr__(self) -> str:
        """Detailed string representation for debugging"""
        return (f"Product(product_id={self.product_id}, product_name='{self.product_name}', "
                f"description='{self.description}', price={self.price}, "
                f"stock_quantity={self.stock_quantity}, category_id={self.category_id}, "
                f"category_name='{self.category_name}')")

    def get_formatted_price(self) -> str:
        """Get formatted price string with 2 decimal places"""
        return f"${self.price:.2f}"

    def is_in_stock(self) -> bool:
        """Check if product is available in stock"""
        return self.stock_quantity > 0
