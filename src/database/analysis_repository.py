# ==========================================
# DATALENS AI - ANALYSIS REPOSITORY V1
# ==========================================

from datetime import (
    datetime,
    timezone,
)

from src.database.connection import (
    get_database_connection,
)


# ==========================================
# SAVE ANALYSIS
# ==========================================

def save_analysis(
    analysis_id: str,
    dataset_id: str,
    original_filename: str | None,
    target_column: str,
    problem_type: str,
    positive_class,
    rows: int,
    columns: int,
    missing_values: int,
    duplicate_rows: int,
    report_path: str,
):
    """
    Save one completed DataLens analysis
    inside the SQLite database.
    """

    connection = (
        get_database_connection()
    )

    try:

        cursor = connection.cursor()

        created_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        cursor.execute(
            """
            INSERT INTO analyses (
                analysis_id,
                dataset_id,
                original_filename,
                target_column,
                problem_type,
                positive_class,
                rows,
                columns,
                missing_values,
                duplicate_rows,
                report_path,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                analysis_id,
                dataset_id,
                original_filename,
                target_column,
                problem_type,
                (
                    None
                    if positive_class is None
                    else str(positive_class)
                ),
                rows,
                columns,
                missing_values,
                duplicate_rows,
                report_path,
                created_at,
            ),
        )

        connection.commit()

        print(
            f"✓ Analysis saved: "
            f"{analysis_id}"
        )

    finally:

        connection.close()


# ==========================================
# GET ONE ANALYSIS
# ==========================================

def get_analysis(
    analysis_id: str,
):
    """
    Fetch one analysis using its
    analysis ID.
    """

    connection = (
        get_database_connection()
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE analysis_id = ?
            """,
            (
                analysis_id,
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()


# ==========================================
# GET ANALYSIS HISTORY
# ==========================================

def get_analysis_history(
    limit: int = 50,
):
    """
    Return recent DataLens analyses,
    newest first.
    """

    connection = (
        get_database_connection()
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analyses
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (
                limit,
            ),
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:

        connection.close()


# ==========================================
# DELETE ANALYSIS
# ==========================================

def delete_analysis(
    analysis_id: str,
):
    """
    Delete one analysis database record.

    This does not delete the generated
    report file from disk.
    """

    connection = (
        get_database_connection()
    )

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM analyses
            WHERE analysis_id = ?
            """,
            (
                analysis_id,
            ),
        )

        connection.commit()

        deleted = (
            cursor.rowcount > 0
        )

        return deleted

    finally:

        connection.close()