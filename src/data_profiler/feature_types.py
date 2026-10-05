# ==========================================
# DATALENS AI - SMART FEATURE TYPE DETECTOR
# ==========================================

import pandas as pd


def detect_feature_types(df: pd.DataFrame):

    """
    Detect the likely semantic type
    of each feature in the dataset.
    """

    print("\n================================")
    print("SMART FEATURE TYPE DETECTION")
    print("================================")


    for column in df.columns:

        series = df[column]

        column_name = column.lower()


        # --------------------------------------
        # IDENTIFIER DETECTION
        # --------------------------------------

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):

            feature_type = "Identifier"


        # --------------------------------------
        # NUMERICAL DETECTION
        # --------------------------------------

        elif pd.api.types.is_numeric_dtype(series):

            feature_type = "Numerical"


        # --------------------------------------
        # CATEGORICAL DETECTION
        # --------------------------------------

        else:

            feature_type = "Categorical"


        print(
            f"{column:<20} → {feature_type}"
        )