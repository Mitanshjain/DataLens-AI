# ==========================================
# DATALENS AI - CORRELATION ANALYSIS
# ==========================================

import pandas as pd


def analyze_correlations(df: pd.DataFrame):

    """
    Analyze correlations between
    numerical features.
    """

    print("\n================================")
    print("CORRELATION ANALYSIS")
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
    # NEED AT LEAST TWO FEATURES
    # ------------------------------------------

    if len(analysis_columns) < 2:

        print(
            "Not enough numerical features "
            "for correlation analysis."
        )

        return


    # ------------------------------------------
    # CALCULATE CORRELATION MATRIX
    # ------------------------------------------

    correlation_matrix = df[
        analysis_columns
    ].corr()


    print(correlation_matrix)