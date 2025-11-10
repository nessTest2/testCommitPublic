# E-commerce Database Application

**Migrated from Java to Python**

A complete e-commerce database service layer providing product management, user operations, and order processing functionality.

## Migration Information

- **Source Language:** Java 14+
- **Target Language:** Python 3.8+
- **Source File:** main.java (433 lines)
- **Migration Date:** 2025-11-07

## Features

### Product Management
- Retrieve all products with category information
- Filter products by category
- Update product inventory/stock levels

### User Management
- Retrieve user information by ID
- User profile management

### Order Processing
- Create new orders
- Add items to orders
- Retrieve order history by user

## Project Structure

```
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── user.py          # User data model
│   ├── product.py       # Product data model
│   └── order.py         # Order data model
├── services/
│   ├── __init__.py
│   └── ecommerce_service.py  # Business logic layer
├── database/
│   ├── __init__.py
│   └── connection.py    # Database connection management
└── main.py              # Application entry point

tests/                   # Test suite (optional)
config/                  # Configuration files
requirements.txt         # Python dependencies
.env.example            # Environment variable template
README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7+ or MariaDB 10.2+
- pip (Python package manager)

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd /app/temp/modernized_cmhow1r9d000kig01psrcka0t
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` with your MySQL connection details:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=EcommerceDB
DB_USER=root
DB_PASSWORD=your_password
```

### 5. Set Up Database Schema

The application expects the following database schema:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS EcommerceDB;
USE EcommerceDB;

-- Users table
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100) NOT NULL
);

-- Products table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    Description TEXT,
    Price DECIMAL(10, 2) NOT NULL,
    StockQuantity INT DEFAULT 0,
    CategoryID INT,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Orders table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(50) DEFAULT 'Pending',
    ShippingAddress TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- OrderItems table
CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```

### 6. Populate Sample Data (Optional)

```sql
-- Sample categories
INSERT INTO Categories (CategoryName) VALUES ('Electronics'), ('Books'), ('Clothing');

-- Sample users
INSERT INTO Users (Username, Email, FirstName, LastName)
VALUES ('johndoe', 'john@example.com', 'John', 'Doe');

-- Sample products
INSERT INTO Products (ProductName, Description, Price, StockQuantity, CategoryID)
VALUES
    ('Laptop', 'High-performance laptop', 999.99, 10, 1),
    ('Python Guide', 'Comprehensive Python book', 49.99, 50, 2);
```

## Usage

### Run the Application

From the project root directory:

```bash
cd src
python main.py
```

Or make it executable:

```bash
chmod +x src/main.py
./src/main.py
```

### Expected Output

```
=== Products ===
Laptop - $999.99 (Electronics)
Python Guide - $49.99 (Books)

=== User Info ===
User: John Doe (john@example.com)

=== Creating Order ===
Created order with ID: 1

=== User Orders ===
Order #1: $1049.98 - Pending

=== Electronics Products ===
Laptop - $999.99 (Stock: 10)
```

## API Usage

### Using the Service Layer

```python
from database.connection import get_connection
from services.ecommerce_service import EcommerceDbService
from decimal import Decimal

# Initialize service
db = get_connection()
service = EcommerceDbService(db)

# Get all products
products = service.get_products()
for product in products:
    print(f"{product.product_name}: {product.price}")

# Get user by ID
user = service.get_user_by_id(1)
if user:
    print(f"User: {user.first_name} {user.last_name}")

# Create order
order_id = service.create_order(
    user_id=1,
    total_amount=Decimal("99.99"),
    shipping_address="123 Main St"
)

# Add items to order
service.add_order_item(order_id, product_id=1, quantity=2, unit_price=Decimal("49.99"))
```

## Key Differences from Java Version

### Language-Specific Changes

1. **Data Classes:** Java POJOs converted to Python `@dataclass`
2. **Type System:** Java static types → Python type hints
3. **Resource Management:** Java try-with-resources → Python context managers (`with` statements)
4. **Decimal Handling:** Java `BigDecimal` → Python `Decimal`
5. **Date/Time:** Java `LocalDateTime` → Python `datetime`
6. **Database Driver:** JDBC → PyMySQL
7. **Error Handling:** Java exceptions → Python exceptions with proper hierarchy

### Improvements

1. **Environment Variables:** Configuration externalized to `.env` file
2. **Modular Structure:** Code organized into separate modules
3. **Context Managers:** Automatic resource cleanup
4. **Type Hints:** Enhanced code documentation and IDE support
5. **Pythonic Idioms:** Following PEP 8 and Python best practices

## Testing

Run tests using pytest:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=src tests/
```

## Migration Traceability

All migrated code includes `@SOURCE` annotations tracing back to the original Java implementation:

```python
# @SOURCE: main.java::class User {::}
```

Format: `# @SOURCE: <file>::<first_line>::<last_line>`

## Troubleshooting

### Connection Errors

- Verify MySQL server is running: `systemctl status mysql`
- Check credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`
- Verify network connectivity: `telnet localhost 3306`

### Import Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

### Database Schema Issues

- Verify all tables exist: `SHOW TABLES;`
- Check table structure: `DESCRIBE Users;`
- Ensure foreign key constraints are valid

## Contributing

This is a migrated project. For improvements or bug fixes, please follow Python best practices and maintain source traceability annotations.

## License

Same as original Java project.

## Contact

For questions about the migration or implementation, refer to the migration documentation in `reports/migration_log.md`.

---

**Note:** This application was automatically migrated from Java to Python while preserving 100% of the original functionality and business logic.
