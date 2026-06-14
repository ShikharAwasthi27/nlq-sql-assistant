import sqlite3
import json

DB_NAME = "ecommerce.db"
OUTPUT_FILE = "schema.json"


def extract_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    schema = {"tables": {}}

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        schema["tables"][table_name] = columns

    conn.close()

    return schema


def main():
    schema = extract_schema()

    with open(OUTPUT_FILE, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"Schema saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
