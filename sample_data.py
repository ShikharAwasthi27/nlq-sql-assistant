import sqlite3
import random
from faker import Faker

DB_NAME = "ecommerce.db"

fake = Faker()


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        email TEXT,
        city TEXT,
        join_date DATE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category_id INTEGER,
        price REAL,
        FOREIGN KEY(category_id) REFERENCES Categories(category_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderItems (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES Orders(order_id),
        FOREIGN KEY(product_id) REFERENCES Products(product_id)
    )
    """)


def insert_categories(cursor):
    categories = [
        "Electronics",
        "Clothing",
        "Books",
        "Home",
        "Sports"
    ]

    for category in categories:
        cursor.execute(
            "INSERT INTO Categories(category_name) VALUES (?)",
            (category,)
        )


def insert_customers(cursor, n=50):
    for _ in range(n):
        cursor.execute("""
        INSERT INTO Customers(
            customer_name,
            email,
            city,
            join_date
        )
        VALUES (?, ?, ?, ?)
        """, (
            fake.name(),
            fake.email(),
            fake.city(),
            fake.date_between(start_date="-2y", end_date="today")
        ))


def insert_products(cursor):
    products = [
        ("Laptop", 1, 800),
        ("Smartphone", 1, 600),
        ("Headphones", 1, 100),
        ("T-Shirt", 2, 25),
        ("Jeans", 2, 50),
        ("Novel", 3, 15),
        ("Cookbook", 3, 20),
        ("Chair", 4, 120),
        ("Table", 4, 250),
        ("Football", 5, 30)
    ]

    for name, category_id, price in products:
        cursor.execute("""
        INSERT INTO Products(
            product_name,
            category_id,
            price
        )
        VALUES (?, ?, ?)
        """, (name, category_id, price))


def insert_orders(cursor, n=100):
    for _ in range(n):
        customer_id = random.randint(1, 50)

        cursor.execute("""
        INSERT INTO Orders(
            customer_id,
            order_date
        )
        VALUES (?, ?)
        """, (
            customer_id,
            fake.date_between(start_date="-1y", end_date="today")
        ))


def insert_order_items(cursor):
    cursor.execute("SELECT order_id FROM Orders")
    orders = cursor.fetchall()

    for (order_id,) in orders:
        num_items = random.randint(1, 3)

        for _ in range(num_items):
            cursor.execute("""
            INSERT INTO OrderItems(
                order_id,
                product_id,
                quantity
            )
            VALUES (?, ?, ?)
            """, (
                order_id,
                random.randint(1, 10),
                random.randint(1, 5)
            ))


def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    create_tables(cursor)

    insert_categories(cursor)
    insert_customers(cursor)
    insert_products(cursor)
    insert_orders(cursor)
    insert_order_items(cursor)

    conn.commit()
    conn.close()

    print(f"{DB_NAME} created successfully.")


if __name__ == "__main__":
    main()
