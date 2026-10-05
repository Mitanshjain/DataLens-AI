# ==========================================
# DATALENS AI - FEATURE ENGINEERING ANALYZER
# ==========================================

import pandas as pd


def analyze_feature_engineering(
    X: pd.DataFrame,
    skew_threshold: float = 1.0,
    high_cardinality_threshold: int = 50,
    near_constant_threshold: float = 0.98
):
    """
    Analyze dataset features and identify
    possible feature-engineering requirements.

    Important:
    This function only ANALYZES the dataset.

    It does not fit learned transformations
    and does not modify the supplied DataFrame.
    """

    print("\n================================")
    print("FEATURE ENGINEERING ANALYSIS")
    print("================================")

    results = {
        "skewed_numerical_features": [],
        "constant_features": [],
        "near_constant_features": [],
        "high_cardinality_features": [],
        "datetime_features": [],
        "interaction_candidates": [],
    }

    # ==========================================
    # 1. CONSTANT / NEAR-CONSTANT FEATURES
    # ==========================================

    for column in X.columns:

        non_null = X[column].dropna()

        if non_null.empty:
            continue

        unique_count = non_null.nunique()

        if unique_count <= 1:

            results[
                "constant_features"
            ].append(column)

            continue

        value_frequencies = (
            non_null
            .value_counts(normalize=True)
        )

        if not value_frequencies.empty:

            dominant_ratio = float(
                value_frequencies.iloc[0]
            )

            if (
                dominant_ratio
                >= near_constant_threshold
            ):

                results[
                    "near_constant_features"
                ].append(column)

    # ==========================================
    # 2. NUMERICAL SKEWNESS
    # ==========================================

    numerical_features = (
        X.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    for column in numerical_features:

        if (
            column
            in results["constant_features"]
        ):
            continue

        values = X[column].dropna()

        if len(values) < 3:
            continue

        skewness = values.skew()

        if pd.isna(skewness):
            continue

        if abs(float(skewness)) >= skew_threshold:

            results[
                "skewed_numerical_features"
            ].append(
                {
                    "feature": column,
                    "skewness": round(
                        float(skewness),
                        4
                    )
                }
            )

    # ==========================================
    # 3. HIGH-CARDINALITY CATEGORICAL FEATURES
    # ==========================================

    categorical_features = (
        X.select_dtypes(
            include=[
                "object",
                "string",
                "category"
            ]
        )
        .columns
        .tolist()
    )

    for column in categorical_features:

        unique_count = int(
            X[column].nunique(
                dropna=True
            )
        )

        if (
            unique_count
            > high_cardinality_threshold
        ):

            results[
                "high_cardinality_features"
            ].append(
                {
                    "feature": column,
                    "unique_values":
                        unique_count
                }
            )

    # ==========================================
    # 4. DATETIME FEATURE DETECTION
    # ==========================================

    for column in X.columns:

        # Already a datetime dtype
        if pd.api.types.is_datetime64_any_dtype(
            X[column]
        ):

            results[
                "datetime_features"
            ].append(column)

            continue

        # Only inspect string-like columns
        if column not in categorical_features:
            continue

        sample = (
            X[column]
            .dropna()
            .astype(str)
            .head(100)
        )

        if sample.empty:
            continue

        parsed = pd.to_datetime(
            sample,
            errors="coerce"
        )

        parse_ratio = float(
            parsed.notna().mean()
        )

        # Require strong evidence before treating
        # a text column as a date.
        if parse_ratio >= 0.90:

            results[
                "datetime_features"
            ].append(column)

    # ==========================================
    # 5. NUMERICAL INTERACTION CANDIDATES
    # ==========================================
    #
    # V1 only reports candidate pairs.
    # We do NOT automatically create every
    # polynomial interaction because that can
    # dramatically increase dimensionality.
    # ==========================================

    usable_numerical = [
        column
        for column in numerical_features
        if column
        not in results["constant_features"]
    ]

    # Limit analysis so a wide dataset does not
    # produce thousands of combinations.
    usable_numerical = usable_numerical[:10]

    for i in range(
        len(usable_numerical)
    ):

        for j in range(
            i + 1,
            len(usable_numerical)
        ):

            results[
                "interaction_candidates"
            ].append(
                {
                    "feature_1":
                        usable_numerical[i],

                    "feature_2":
                        usable_numerical[j]
                }
            )

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print(
        "Skewed Numerical Features:",
        results[
            "skewed_numerical_features"
        ]
    )

    print(
        "Constant Features:",
        results[
            "constant_features"
        ]
    )

    print(
        "Near-Constant Features:",
        results[
            "near_constant_features"
        ]
    )

    print(
        "High-Cardinality Features:",
        results[
            "high_cardinality_features"
        ]
    )

    print(
        "Datetime Features:",
        results[
            "datetime_features"
        ]
    )

    print(
        "Interaction Candidates:",
        len(
            results[
                "interaction_candidates"
            ]
        )
    )

    print(
        "✓ Feature engineering analysis complete."
    )

    return results 