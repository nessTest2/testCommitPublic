# @SOURCE: main.java::class User {::}
"""
User model representing user accounts and profiles
Migrated from Java User class (lines 7-56)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    User data model with account information

    Attributes:
        user_id: Unique user identifier
        username: User's login name
        email: User's email address
        first_name: User's first name
        last_name: User's last name
        created_at: Timestamp of account creation
    """
    # @SOURCE: main.java::private int userId;::private LocalDateTime createdAt;
    user_id: int = 0
    username: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize created_at if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now()

    # @SOURCE: main.java::public String toString() {::}
    def __str__(self) -> str:
        """String representation of User object"""
        return (f"User{{userId={self.user_id}, username='{self.username}', "
                f"email='{self.email}', firstName='{self.first_name}', "
                f"lastName='{self.last_name}'}}")

    def __repr__(self) -> str:
        """Detailed string representation for debugging"""
        return (f"User(user_id={self.user_id}, username='{self.username}', "
                f"email='{self.email}', first_name='{self.first_name}', "
                f"last_name='{self.last_name}', created_at={self.created_at})")
