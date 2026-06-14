import json
import sqlglot
from sqlglot import expressions as exp

FORBIDDEN_KEYWORDS = {
    "DELETE",
    "DROP",
    "UPDATE",
    "ALTER",
    "TRUNCATE",
    "INSERT"
}


class SQLValidationError(Exception):
    """Raised when SQL validation fails."""
    pass


def load_schema(schema_path="schema.json"):
    with open(schema_path, "r") as f:
        schema = json.load(f)

    return schema["tables"]


def validate_sql(sql, schema_path="schema.json"):
    """
    Validate generated SQL before execution.

    Returns:
        (True, "Valid SQL")

    Raises:
        SQLValidationError
    """

    schema = load_schema(schema_path)

    sql = sql.strip()

    # --------------------------------------------------
    # Rule 1: Restrict semicolons
    # --------------------------------------------------

    if ";" in sql:
        raise SQLValidationError(
            "Multiple SQL statements are not allowed."
        )

    # --------------------------------------------------
    # Rule 2: Block harmful keywords
    # --------------------------------------------------

    upper_sql = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper_sql:
            raise SQLValidationError(
                f"{keyword} statements are not allowed."
            )

    # --------------------------------------------------
    # Rule 3: Parse SQL
    # --------------------------------------------------

    try:
        parsed = sqlglot.parse_one(sql, read="sqlite")

    except Exception:
        raise SQLValidationError(
            "Unable to parse generated SQL."
        )

    # --------------------------------------------------
    # Rule 4: SELECT only
    # --------------------------------------------------

    if not isinstance(parsed, exp.Select):
        raise SQLValidationError(
            "Only SELECT queries are allowed."
        )

    # --------------------------------------------------
    # Rule 5: Validate tables
    # --------------------------------------------------

    valid_tables = set(schema.keys())

    used_tables = {
        table.name
        for table in parsed.find_all(exp.Table)
    }

    invalid_tables = used_tables - valid_tables

    if invalid_tables:
        raise SQLValidationError(
            f"Unauthorized table(s): "
            f"{', '.join(invalid_tables)}"
        )

    # --------------------------------------------------
    # Rule 6: Validate columns
    # --------------------------------------------------

    valid_columns = set()

    for columns in schema.values():
        valid_columns.update(columns)

    for column in parsed.find_all(exp.Column):

        column_name = column.name

        if column_name == "*":
            continue

        if column_name not in valid_columns:
            raise SQLValidationError(
                f"Invalid column: {column_name}"
            )

    # --------------------------------------------------
    # Rule 7: Validate joins
    # --------------------------------------------------

    valid_relationships = {
        ("Products", "Categories"),
        ("Orders", "Customers"),
        ("OrderItems", "Orders"),
        ("OrderItems", "Products")
    }

    joins = list(parsed.find_all(exp.Join))

    for join in joins:

        joined_table = join.this.name

        if joined_table not in valid_tables:
            raise SQLValidationError(
                f"Invalid join table: {joined_table}"
            )

    table_list = list(used_tables)

    for i in range(len(table_list)):
        for j in range(i + 1, len(table_list)):

            pair = (
                table_list[i],
                table_list[j]
            )

            reverse_pair = (
                table_list[j],
                table_list[i]
            )

            if (
                pair not in valid_relationships
                and reverse_pair not in valid_relationships
            ):
                raise SQLValidationError(
                    f"Invalid relationship "
                    f"between {pair[0]} "
                    f"and {pair[1]}"
                )

    return True, "Valid SQL"
