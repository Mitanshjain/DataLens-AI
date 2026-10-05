# ==========================================
# DATALENS AI - DATA TYPE ANALYZER
# ==========================================

import pandas as pd


def analyze_data_types(df: pd.DataFrame):

    """
    Analyze the technical data types
    of each column in the dataset.
    """

    print("\n================================")
    print("DATA TYPE ANALYSIS")
    print("================================")


    # ------------------------------------------
    # COLUMN DATA TYPES
    # ------------------------------------------

    for column in df.columns:

        dtype = df[column].dtype

        print(
            f"{column:<20} → {dtype}"
        )


    # ------------------------------------------
    # DATA TYPE SUMMARY
    # ------------------------------------------

    print("\nData Type Summary:")

    dtype_counts = (
        df.dtypes
        .astype(str)
        .value_counts()
    )

    for dtype, count in dtype_counts.items():

        print(
            f"  - {dtype}: {count} column(s)"
        )