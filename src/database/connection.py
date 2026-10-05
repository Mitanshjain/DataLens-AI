# ==========================================
# DATALENS AI - DATABASE CONNECTION V1
# ==========================================

import sqlite3
from pathlib import Path


# ==========================================
# DATABASE PATH
# ==========================================

DATABASE_DIR = Path("data")

DATABASE_PATH = (
    DATABASE_DIR / "datalens.db"
)


# ==========================================
# GET DATABASE CONNECTION
# ==========================================

def get_database_connection():
    """
    Create and return a SQLite database
    connection.

    row_factory allows database rows to be
    accessed using column names.
    """

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():
    """
    Create the required database tables
    if they do not already exist.
    """

    connection = (
        get_database_connection()
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analyses (
                analysis_id TEXT PRIMARY KEY,
                dataset_id TEXT NOT NULL,
                original_filename TEXT,
                target_column TEXT NOT NULL,
                problem_type TEXT NOT NULL,
                positive_class TEXT,
                rows INTEGER NOT NULL,
                columns INTEGER NOT NULL,
                missing_values INTEGER NOT NULL,
                duplicate_rows INTEGER NOT NULL,
                report_path TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

        print(
            "✓ DataLens database initialized."
        )

    finally:

        connection.close()