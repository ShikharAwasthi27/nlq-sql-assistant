from guardrails import validate_sql


queries = [
    """
    SELECT *
    FROM Customers
    """,

    """
    DELETE FROM Customers
    """,

    """
    SELECT customer_name
    FROM Employees
    """,

    """
    SELECT city
    FROM Customers;
    DROP TABLE Customers
    """,

    """
    SELECT p.product_name,
           SUM(oi.quantity)
    FROM OrderItems oi
    JOIN Products p
      ON oi.product_id = p.product_id
    GROUP BY p.product_name
    """
]


for query in queries:

    print("\n" + "-" * 50)

    try:
        validate_sql(query)

        print("ALLOWED")

    except Exception as e:
        print("BLOCKED")
        print(e)
