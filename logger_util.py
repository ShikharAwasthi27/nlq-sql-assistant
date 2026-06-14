import csv
import os
from datetime import datetime

LOG_FILE = "query_logs.csv"


def initialize_logs():
    """
    Creates log file if it does not exist.
    """

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "timestamp",
                "question",
                "sql",
                "validation_status",
                "execution_time",
                "rows_returned",
                "error_message"
            ])


def log_interaction(
    question,
    sql,
    validation_status,
    execution_time,
    rows_returned,
    error_message=""
):
    """
    Append interaction details to CSV log.
    """

    initialize_logs()

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            question,
            sql,
            validation_status,
            round(execution_time, 2),
            rows_returned,
            error_message
        ])
