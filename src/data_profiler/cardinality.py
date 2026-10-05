# Cardinality simply means:- How many unique values does a column have?

# ==========================================
# DATALENS AI - CARDINALITY ANALYZER
# ==========================================

import pandas as pd


def analyze_cardinality(df: pd.DataFrame):

    """
    Analyze the number of unique values
    present in every column.
    """

    print("\n================================")
    print("CARDINALITY ANALYSIS")
    print("================================")


    total_rows = len(df)


    for column in df.columns:

        # --------------------------------------
        # UNIQUE VALUES
        # --------------------------------------

        unique_count = df[column].nunique(
            dropna=True
        )


        # --------------------------------------
        # UNIQUE VALUE PERCENTAGE
        # --------------------------------------

        unique_percentage = (
            unique_count / total_rows
        ) * 100


        print(
            f"{column:<20} → "
            f"{unique_count} unique "
            f"({unique_percentage:.2f}%)"
        )