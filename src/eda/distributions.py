# ==========================================
# DATALENS AI - DISTRIBUTION ANALYSIS
# ==========================================

import pandas as pd


def analyze_distributions(df: pd.DataFrame):

    """
    Analyze the distribution of
    numerical features.
    """

    print("\n================================")
    print("NUMERICAL DISTRIBUTION ANALYSIS")
    print("================================")


    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    for column in numerical_columns:

        column_name = column.lower()


        # --------------------------------------
        # SKIP IDENTIFIER COLUMNS
        # --------------------------------------

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue


        # --------------------------------------
        # REMOVE MISSING VALUES
        # --------------------------------------

        series = df[column].dropna()


        if series.empty:
            continue


        # --------------------------------------
        # CALCULATE STATISTICS
        # --------------------------------------

        mean = series.mean()

        median = series.median()

        std = series.std()

        minimum = series.min()

        maximum = series.max()

        skewness = series.skew()


        # --------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------

        print(f"\nColumn: {column}")

        print(f"  Mean: {mean:.2f}")

        print(f"  Median: {median:.2f}")

        print(f"  Standard Deviation: {std:.2f}")

        print(f"  Minimum: {minimum:.2f}")

        print(f"  Maximum: {maximum:.2f}")

        print(f"  Skewness: {skewness:.2f}")