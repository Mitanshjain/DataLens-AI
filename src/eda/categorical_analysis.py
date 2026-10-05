# ==========================================
# DATALENS AI - CATEGORICAL ANALYSIS
# ==========================================

import pandas as pd


def analyze_categorical_features(df: pd.DataFrame):

    """
    Analyze the distribution of
    categorical features.
    """

    print("\n================================")
    print("CATEGORICAL FEATURE ANALYSIS")
    print("================================")


    # ------------------------------------------
    # SELECT CATEGORICAL COLUMNS
    # ------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()


    # ------------------------------------------
    # CHECK IF COLUMNS EXIST
    # ------------------------------------------

    if not categorical_columns:

        print("No categorical features found.")

        return


    # ------------------------------------------
    # ANALYZE EACH COLUMN
    # ------------------------------------------

    for column in categorical_columns:

        print(f"\nColumn: {column}")


        # --------------------------------------
        # VALUE COUNTS
        # --------------------------------------

        counts = df[column].value_counts(
            dropna=False
        )


        percentages = df[column].value_counts(
            normalize=True,
            dropna=False
        ) * 100


        # --------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------

        for value, count in counts.items():

            percentage = percentages[value]

            print(
                f"  - {value}: "
                f"{count} record(s) "
                f"({percentage:.2f}%)"
            )