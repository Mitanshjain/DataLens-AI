# ==========================================
# DATALENS AI - FEATURE TARGET SEPARATOR V2
# ==========================================

import pandas as pd


# ==========================================
# IDENTIFIER DETECTION
# ==========================================

def detect_identifier_columns(
    X: pd.DataFrame
):
    """
    Detect obvious identifier columns.

    V2 intentionally uses conservative
    name-based rules.

    We do NOT automatically remove every
    high-cardinality feature because a
    high-cardinality column may contain
    useful predictive information.
    """

    identifier_columns = []


    for column in X.columns:

        column_name = (
            str(column)
            .strip()
            .lower()
        )


        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):

            identifier_columns.append(
                column
            )


    return identifier_columns


# ==========================================
# FEATURE TARGET SEPARATION
# ==========================================

def separate_features_target(
    df: pd.DataFrame,
    target_column: str
):
    """
    Separate the dataset into input features
    (X) and target (y).

    Rows with missing target values are
    excluded before ML training.

    Missing feature values are preserved
    because the preprocessing pipeline is
    responsible for imputing them.
    """

    print("\n================================")
    print("FEATURE & TARGET SEPARATION V2")
    print("================================")


    # --------------------------------------
    # CHECK TARGET EXISTS
    # --------------------------------------

    if target_column not in df.columns:

        raise ValueError(
            f"Target column "
            f"'{target_column}' was not found."
        )


    # --------------------------------------
    # COUNT MISSING TARGET ROWS
    # --------------------------------------

    missing_target_mask = (
        df[target_column]
        .isna()
    )


    missing_target_rows = int(
        missing_target_mask.sum()
    )


    # --------------------------------------
    # REMOVE ROWS WITH MISSING TARGET
    # --------------------------------------
    #
    # Important:
    #
    # We only remove rows where y is missing.
    #
    # Missing values inside feature columns
    # remain available for the preprocessing
    # pipeline.
    # --------------------------------------

    working_df = (
        df.loc[
            ~missing_target_mask
        ]
        .copy()
    )


    if working_df.empty:

        raise ValueError(
            "No usable rows remain after "
            "removing missing target values."
        )


    # --------------------------------------
    # CREATE TARGET
    # --------------------------------------

    y = (
        working_df[
            target_column
        ]
        .copy()
    )


    # --------------------------------------
    # CREATE FEATURES
    # --------------------------------------

    X = (
        working_df.drop(
            columns=[
                target_column
            ]
        )
        .copy()
    )


    # --------------------------------------
    # CHECK FEATURE AVAILABILITY
    # --------------------------------------

    if X.shape[1] == 0:

        raise ValueError(
            "No feature columns are available "
            "after separating the target."
        )


    # --------------------------------------
    # REMOVE IDENTIFIER COLUMNS
    # --------------------------------------

    identifier_columns = (
        detect_identifier_columns(
            X
        )
    )


    if identifier_columns:

        X = X.drop(
            columns=identifier_columns
        )


    # --------------------------------------
    # VERIFY FEATURES STILL EXIST
    # --------------------------------------

    if X.shape[1] == 0:

        raise ValueError(
            "No usable feature columns remain "
            "after removing identifier columns."
        )


    # --------------------------------------
    # VERIFY X AND y ALIGN
    # --------------------------------------

    if len(X) != len(y):

        raise RuntimeError(
            "Feature and target row counts "
            "do not match."
        )


    # --------------------------------------
    # VERIFY TARGET STILL HAS 2 VALUES
    # --------------------------------------

    unique_target_values = (
        y.nunique(
            dropna=True
        )
    )


    if unique_target_values < 2:

        raise ValueError(
            "Target must contain at least "
            "2 unique values after removing "
            "missing target rows."
        )


    # --------------------------------------
    # DISPLAY RESULT
    # --------------------------------------

    print(
        f"Target Column: {target_column}"
    )

    print(
        f"Rows Removed Due To Missing Target: "
        f"{missing_target_rows}"
    )

    print(
        f"Rows Available For ML: "
        f"{len(working_df)}"
    )

    print(
        f"Removed Identifier Columns: "
        f"{identifier_columns}"
    )

    print(
        f"Feature Columns: "
        f"{X.columns.tolist()}"
    )

    print(
        f"Number of Features: "
        f"{X.shape[1]}"
    )

    print(
        f"Unique Target Values: "
        f"{unique_target_values}"
    )

    print(
        f"X Shape: {X.shape}"
    )

    print(
        f"y Shape: {y.shape}"
    )


    return X, y