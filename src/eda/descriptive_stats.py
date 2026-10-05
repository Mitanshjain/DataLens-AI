# ==========================================
# DATALENS AI - DESCRIPTIVE STATISTICS
# ==========================================

import pandas as pd


def analyze_descriptive_statistics(df: pd.DataFrame):

    """
    Generate descriptive statistics
    for numerical features.
    """

    print("\n================================")
    print("DESCRIPTIVE STATISTICS")
    print("================================")


    # ------------------------------------------
    # SELECT NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    # ------------------------------------------
    # REMOVE IDENTIFIER COLUMNS
    # ------------------------------------------

    analysis_columns = []

    for column in numerical_columns:

        column_name = column.lower()

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue

        analysis_columns.append(column)


    # ------------------------------------------
    # CHECK NUMERICAL FEATURES
    # ------------------------------------------

    if not analysis_columns:

        print("No numerical features available.")

        return


    # ------------------------------------------
    # GENERATE STATISTICS
    # ------------------------------------------

    statistics = df[
        analysis_columns
    ].describe()


    print(statistics)