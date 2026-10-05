# ==========================================
# DATALENS AI - PREPROCESSING ANALYZER
# ==========================================

import pandas as pd


def analyze_preprocessing_requirements(
    X: pd.DataFrame
):

    """
    Analyze features and determine
    what preprocessing may be required.
    """

    print("\n================================")
    print("ML PREPROCESSING ANALYSIS")
    print("================================")


    # ------------------------------------------
    # DETECT NUMERICAL FEATURES
    # ------------------------------------------

    numerical_features = X.select_dtypes(
        include="number"
    ).columns.tolist()


    # ------------------------------------------
    # DETECT CATEGORICAL FEATURES
    # ------------------------------------------

    categorical_features = X.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()


    print(
        f"Numerical Features: "
        f"{numerical_features}"
    )

    print(
        f"Categorical Features: "
        f"{categorical_features}"
    )


    # ------------------------------------------
    # CHECK MISSING VALUES
    # ------------------------------------------

    print("\nMissing Values:")

    missing_found = False

    for column in X.columns:

        missing_count = X[column].isnull().sum()

        if missing_count > 0:

            print(
                f"  - {column}: "
                f"{missing_count} missing"
            )

            missing_found = True


    if not missing_found:

        print("  ✓ No missing values found.")


    # ------------------------------------------
    # PREPROCESSING REQUIREMENTS
    # ------------------------------------------

    print("\nRequired Preprocessing:")


    if numerical_features:

        print(
            "  - Numerical features may "
            "require missing-value handling."
        )


    if categorical_features:

        print(
            "  - Categorical features require "
            "encoding before model training."
        )


    if not numerical_features and not categorical_features:

        print(
            "  - No supported features detected."
        )


    return (
        numerical_features,
        categorical_features
    )