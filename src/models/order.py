# @SOURCE: main.java::class Order {::}
"""
Order model representing customer orders
Migrated from Java Order class (lines 115-165)
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Order:
    """
    Order data model with transaction information

    Attributes:
        order_id: Unique order identifier
        user_id: Foreign key to user who placed the order
        order_date: Timestamp when order was placed
        total_amount: Total order amount (using Decimal for precision)
        status: Order status (e.g., 'Pending', 'Shipped', 'Delivered')
        shipping_address: Delivery address for the order
    """
    # @SOURCE: main.java::private int orderId;::private String shippingAddress;
    order_id: int = 0
    user_id: int = 0
    order_date: Optional[datetime] = None
    total_amount: Decimal = Decimal('0.00')
    status: str = "Pending"
    shipping_address: str = ""

    def __post_init__(self):
        """Initialize order_date and ensure total_amount is Decimal"""
        if self.order_date is None:
            self.order_date = datetime.now()
        if not isinstance(self.total_amount, Decimal):
            self.total_amount = Decimal(str(self.total_amount))

    # @SOURCE: main.java::public String toString() {::}
    def __str__(self) -> str:
        """String representation of Order object"""
        return (f"Order{{orderId={self.order_id}, userId={self.user_id}, "
                f"orderDate={self.order_date}, totalAmount={self.total_amount}, "
                f"status='{self.status}'}}")

    def __repr__(self) -> str:
        """Detailed string representation for debugging"""
        return (f"Order(order_id={self.order_id}, user_id={self.user_id}, "
                f"order_date={self.order_date}, total_amount={self.total_amount}, "
                f"status='{self.status}', shipping_address='{self.shipping_address}')")

    def get_formatted_total(self) -> str:
        """Get formatted total amount with 2 decimal places"""
        return f"${self.total_amount:.2f}"

    def is_completed(self) -> bool:
        """Check if order is in a completed state"""
        return self.status.lower() in ['delivered', 'completed']
