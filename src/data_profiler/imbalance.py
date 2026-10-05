# ==========================================
# DATALENS AI - CLASS IMBALANCE ANALYZER
# ==========================================

import pandas as pd


def analyze_class_imbalance(df: pd.DataFrame):

    """
    Analyze the distribution of values
    in categorical columns.
    """

    print("\n================================")
    print("CLASS IMBALANCE ANALYSIS")
    print("================================")


    # ------------------------------------------
    # SELECT CATEGORICAL COLUMNS
    # ------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns


    # ------------------------------------------
    # CHECK IF CATEGORICAL COLUMNS EXIST
    # ------------------------------------------

    if len(categorical_columns) == 0:

        print("No categorical columns found.")

        return


    # ------------------------------------------
    # ANALYZE EACH CATEGORICAL COLUMN
    # ------------------------------------------

    for column in categorical_columns:

        print(f"\nColumn: {column}")

        value_counts = df[column].value_counts(
            normalize=True,
            dropna=False
        ) * 100


        for value, percentage in value_counts.items():

            print(
                f"  - {value}: "
                f"{percentage:.2f}%"
            )