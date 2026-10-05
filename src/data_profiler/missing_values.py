# ==========================================
# DATALENS AI - MISSING VALUE ANALYZER
# ==========================================

import pandas as pd


def analyze_missing_values(df: pd.DataFrame):

    """
    Analyze missing values in the dataset.
    """

    print("\n================================")
    print("MISSING VALUE ANALYSIS")
    print("================================")


    # ------------------------------------------
    # TOTAL MISSING VALUES
    # ------------------------------------------

    total_missing = df.isnull().sum().sum()

    print(f"Total Missing Values: {total_missing}")


    # ------------------------------------------
    # NO MISSING VALUES
    # ------------------------------------------

    if total_missing == 0:

        print("✓ No missing values found.")

        return


    # ------------------------------------------
    # COLUMN-WISE ANALYSIS
    # ------------------------------------------

    missing_count = df.isnull().sum()

    missing_percentage = (
        missing_count / len(df)
    ) * 100


    # ------------------------------------------
    # DISPLAY ONLY COLUMNS WITH MISSING VALUES
    # ------------------------------------------

    print("\nColumns with Missing Values:")

    for column in df.columns:

        if missing_count[column] > 0:

            print(
                f"  - {column}: "
                f"{missing_count[column]} missing "
                f"({missing_percentage[column]:.2f}%)"
            )