# ==========================================
# DATALENS AI - SUSPICIOUS COLUMN DETECTOR
# ==========================================

import pandas as pd


def detect_suspicious_columns(df: pd.DataFrame):

    """
    Detect columns that may require
    attention before analysis or ML.
    """

    print("\n================================")
    print("SUSPICIOUS COLUMN ANALYSIS")
    print("================================")


    suspicious_found = False


    for column in df.columns:

        column_name = column.lower()

        unique_count = df[column].nunique(
            dropna=True
        )


        # --------------------------------------
        # CHECK 1: IDENTIFIER COLUMN
        # --------------------------------------

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):

            print(
                f"⚠ {column}: "
                f"Possible identifier column."
            )

            suspicious_found = True


        # --------------------------------------
        # CHECK 2: CONSTANT COLUMN
        # --------------------------------------

        if unique_count == 1:

            print(
                f"⚠ {column}: "
                f"Constant column."
            )

            suspicious_found = True


    # ------------------------------------------
    # NO SUSPICIOUS COLUMNS
    # ------------------------------------------

    if not suspicious_found:

        print("✓ No suspicious columns detected.")