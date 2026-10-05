# ==========================================
# DATALENS AI - OUTLIER DETECTOR
# ==========================================

import pandas as pd


def detect_outliers(df: pd.DataFrame):

    """
    Detect outliers in numerical columns
    using the IQR method.
    """

    print("\n================================")
    print("OUTLIER ANALYSIS")
    print("================================")


    # ------------------------------------------
    # SELECT NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns


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
        # CALCULATE QUARTILES
        # --------------------------------------

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1


        # --------------------------------------
        # CALCULATE OUTLIER LIMITS
        # --------------------------------------

        lower_limit = q1 - (1.5 * iqr)

        upper_limit = q3 + (1.5 * iqr)


        # --------------------------------------
        # FIND OUTLIERS
        # --------------------------------------

        outliers = df[
            (df[column] < lower_limit)
            |
            (df[column] > upper_limit)
        ]


        outlier_count = len(outliers)


        # --------------------------------------
        # CALCULATE PERCENTAGE
        # --------------------------------------

        outlier_percentage = (
            outlier_count / len(df)
        ) * 100


        print(
            f"{column:<20} → "
            f"{outlier_count} outlier(s) "
            f"({outlier_percentage:.2f}%)"
        )