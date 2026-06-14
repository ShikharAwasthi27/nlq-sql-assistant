import sqlite3
import pandas as pd
import time

DB_NAME = "ecommerce.db"
QUERY_TIMEOUT_SECONDS = 10


def execute_query(sql):
    """
    Execute validated SQL query and return:
    success, result/error, execution_time
    """

    start_time = time.time()

    try:
        conn = sqlite3.connect(DB_NAME)

        df = pd.read_sql_query(sql, conn)

        conn.close()

        execution_time = time.time() - start_time

        if execution_time > QUERY_TIMEOUT_SECONDS:
            return (
                False,
                f"Query execution exceeded "
                f"{QUERY_TIMEOUT_SECONDS} seconds.",
                execution_time
            )

        return (
            True,
            df,
            execution_time
        )

    except Exception as e:
        execution_time = time.time() - start_time

        return (
            False,
            str(e),
            execution_time
        )
