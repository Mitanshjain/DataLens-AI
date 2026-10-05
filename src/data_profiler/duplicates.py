# ==========================================
# DATALENS AI - DUPLICATE ANALYZER
# ==========================================

import pandas as pd


def analyze_duplicates(df: pd.DataFrame):

    """
    Analyze duplicate rows in the dataset.
    """

    print("\n================================")
    print("DUPLICATE ROW ANALYSIS")
    print("================================")


    # ------------------------------------------
    # FIND DUPLICATE ROWS
    # ------------------------------------------

    duplicate_mask = df.duplicated()

    duplicate_count = duplicate_mask.sum()


    # ------------------------------------------
    # CALCULATE DUPLICATE PERCENTAGE
    # ------------------------------------------

    duplicate_percentage = (
        duplicate_count / len(df)
    ) * 100


    # ------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------

    print(f"Duplicate Rows: {duplicate_count}")

    print(
        f"Duplicate Percentage: "
        f"{duplicate_percentage:.2f}%"
    )


    # ------------------------------------------
    # IF NO DUPLICATES
    # ------------------------------------------

    if duplicate_count == 0:

        print("✓ No duplicate rows found.")

        return


    # ------------------------------------------
    # DISPLAY DUPLICATE ROWS
    # ------------------------------------------

    print("\nDuplicate Rows Found:")

    print(df[duplicate_mask])