# ==========================================
# DATALENS AI - DATA QUALITY SCORE
# ==========================================

import pandas as pd


def calculate_quality_score(df: pd.DataFrame):

    """
    Calculate a simple dataset quality score
    based on common data quality problems.
    """

    print("\n================================")
    print("DATA QUALITY SCORE")
    print("================================")


    score = 100.0


    # ------------------------------------------
    # MISSING VALUE PENALTY
    # ------------------------------------------

    total_cells = df.shape[0] * df.shape[1]

    total_missing = df.isnull().sum().sum()

    missing_percentage = (
        total_missing / total_cells
    ) * 100

    score -= missing_percentage


    # ------------------------------------------
    # DUPLICATE ROW PENALTY
    # ------------------------------------------

    duplicate_count = df.duplicated().sum()

    duplicate_percentage = (
        duplicate_count / len(df)
    ) * 100

    score -= duplicate_percentage


    # ------------------------------------------
    # CONSTANT COLUMN PENALTY
    # ------------------------------------------

    constant_columns = 0

    for column in df.columns:

        if df[column].nunique(dropna=True) == 1:

            constant_columns += 1


    constant_percentage = (
        constant_columns / len(df.columns)
    ) * 100

    score -= constant_percentage


    # ------------------------------------------
    # KEEP SCORE BETWEEN 0 AND 100
    # ------------------------------------------

    score = max(0, min(100, score))


    # ------------------------------------------
    # DISPLAY SCORE
    # ------------------------------------------

    print(f"Overall Quality Score: {score:.2f}/100")


    print("\nQuality Factors:")

    print(
        f"  Missing Data: "
        f"{missing_percentage:.2f}%"
    )

    print(
        f"  Duplicate Rows: "
        f"{duplicate_percentage:.2f}%"
    )

    print(
        f"  Constant Columns: "
        f"{constant_columns}"
    )