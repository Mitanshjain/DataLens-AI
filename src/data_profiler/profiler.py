# ==========================================
# DATALENS AI - DATA PROFILER
# ==========================================

import pandas as pd


def profile_dataset(df: pd.DataFrame):

    """
    Generate basic information about
    the uploaded dataset.
    """

    print("\n================================")
    print("DATASET PROFILE")
    print("================================")


    # ------------------------------------------
    # TOTAL ROWS
    # ------------------------------------------

    total_rows = df.shape[0]


    # ------------------------------------------
    # TOTAL COLUMNS
    # ------------------------------------------

    total_columns = df.shape[1]


    # ------------------------------------------
    # MEMORY USAGE
    # ------------------------------------------

    memory_usage = df.memory_usage(deep=True).sum()

    memory_mb = memory_usage / (1024 * 1024)


    # ------------------------------------------
    # NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    # ------------------------------------------
    # CATEGORICAL COLUMNS
    # ------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    # ------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------

    print(f"Total Rows: {total_rows}")

    print(f"Total Columns: {total_columns}")

    print(f"Memory Usage: {memory_mb:.4f} MB")

    print(
        f"Numerical Columns: "
        f"{len(numerical_columns)}"
    )

    print(
        f"Categorical Columns: "
        f"{len(categorical_columns)}"
    )


    print("\nNumerical Features:")

    for column in numerical_columns:
        print(f"  - {column}")


    print("\nCategorical Features:")

    for column in categorical_columns:
        print(f"  - {column}")