# ==========================================
# DATALENS AI - MISSING VALUE PREPROCESSOR
# ==========================================

import pandas as pd

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import OneHotEncoder


def handle_missing_values(
    X: pd.DataFrame,
    numerical_features: list,
    categorical_features: list
):

    """
    Handle missing values in numerical
    and categorical features.
    """

    print("\n================================")
    print("MISSING VALUE PREPROCESSING")
    print("================================")


    # Make a copy so the original
    # dataset is not modified.
    X_processed = X.copy()


    # ------------------------------------------
    # NUMERICAL MISSING VALUES
    # ------------------------------------------

    if numerical_features:

        numerical_imputer = SimpleImputer(
            strategy="median"
        )

        X_processed[numerical_features] = (
            numerical_imputer.fit_transform(
                X[numerical_features]
            )
        )

        print(
            "✓ Numerical missing values "
            "handled using median."
        )


    # ------------------------------------------
    # CATEGORICAL MISSING VALUES
    # ------------------------------------------

    if categorical_features:

        categorical_imputer = SimpleImputer(
            strategy="most_frequent"
        )

        X_processed[categorical_features] = (
            categorical_imputer.fit_transform(
                X[categorical_features]
            )
        )

        print(
            "✓ Categorical missing values "
            "handled using most frequent value."
        )


    # ------------------------------------------
    # CHECK REMAINING MISSING VALUES
    # ------------------------------------------

    remaining_missing = (
        X_processed
        .isnull()
        .sum()
        .sum()
    )


    print(
        f"Remaining Missing Values: "
        f"{remaining_missing}"
    )


    return X_processed

def encode_categorical_features(
    X: pd.DataFrame,
    categorical_features: list
):

    """
    Convert categorical features into
    numerical features using one-hot encoding.
    """

    print("\n================================")
    print("CATEGORICAL ENCODING")
    print("================================")


    # ------------------------------------------
    # CHECK CATEGORICAL FEATURES
    # ------------------------------------------

    if not categorical_features:

        print(
            "✓ No categorical features "
            "require encoding."
        )

        return X


    # ------------------------------------------
    # CREATE ENCODER
    # ------------------------------------------

    encoder = OneHotEncoder(
        sparse_output=False,
        handle_unknown="ignore"
    )


    # ------------------------------------------
    # ENCODE CATEGORICAL DATA
    # ------------------------------------------

    encoded_data = encoder.fit_transform(
        X[categorical_features]
    )


    # ------------------------------------------
    # GET NEW COLUMN NAMES
    # ------------------------------------------

    encoded_columns = (
        encoder.get_feature_names_out(
            categorical_features
        )
    )


    encoded_df = pd.DataFrame(
        encoded_data,
        columns=encoded_columns,
        index=X.index
    )


    # ------------------------------------------
    # REMOVE ORIGINAL TEXT COLUMNS
    # ------------------------------------------

    X_encoded = X.drop(
        columns=categorical_features
    )


    # ------------------------------------------
    # ADD ENCODED COLUMNS
    # ------------------------------------------

    X_encoded = pd.concat(
        [
            X_encoded,
            encoded_df
        ],
        axis=1
    )


    print(
        "✓ Categorical features encoded "
        "using One-Hot Encoding."
    )

    print(
        f"Encoded Columns: "
        f"{encoded_columns.tolist()}"
    )


    return X_encoded