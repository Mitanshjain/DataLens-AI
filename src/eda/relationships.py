# ==========================================
# DATALENS AI - RELATIONSHIP ANALYSIS
# ==========================================

import pandas as pd


def analyze_relationships(df: pd.DataFrame):

    """
    Analyze relationships between
    categorical and numerical features.
    """

    print("\n================================")
    print("FEATURE RELATIONSHIP ANALYSIS")
    print("================================")


    # ------------------------------------------
    # NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    # ------------------------------------------
    # REMOVE IDENTIFIER COLUMNS
    # ------------------------------------------

    numerical_features = []

    for column in numerical_columns:

        column_name = column.lower()

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue

        numerical_features.append(column)


    # ------------------------------------------
    # CATEGORICAL COLUMNS
    # ------------------------------------------

    categorical_features = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()


    # ------------------------------------------
    # ANALYZE RELATIONSHIPS
    # ------------------------------------------

    for category in categorical_features:

        for numerical in numerical_features:

            print(
                f"\n{numerical} grouped by {category}:"
            )


            result = (
                df.groupby(
                    category,
                    dropna=False
                )[numerical]
                .mean()
            )


            for group, value in result.items():

                print(
                    f"  - {group}: "
                    f"{value:.2f}"
                )