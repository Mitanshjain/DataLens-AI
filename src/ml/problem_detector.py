# ==========================================
# DATALENS AI - ML PROBLEM DETECTOR V3
# ==========================================

import pandas as pd


# ==========================================
# DETECTION SETTINGS
# ==========================================

MAX_NUMERIC_CLASS_VALUES = 10


# ==========================================
# DETECT PROBLEM TYPE
# ==========================================

def detect_problem_type(
    df: pd.DataFrame,
    target_column: str
):
    """
    Detect whether the machine learning
    problem is classification or regression.

    Detection rules:

    1. Boolean target
       -> Classification

    2. Categorical / non-numeric target
       -> Classification

    3. Numeric target:
       - Low-cardinality integer-like labels
         -> Classification
       - Otherwise
         -> Regression

    Important:
    Problem detection is heuristic-based.
    It cannot always understand the real-world
    semantic meaning of a numeric target.
    """

    print("\n================================")
    print("ML PROBLEM DETECTION V3")
    print("================================")


    # --------------------------------------
    # CHECK TARGET EXISTS
    # --------------------------------------

    if target_column not in df.columns:

        raise ValueError(
            f"Target column "
            f"'{target_column}' was not found."
        )


    target = df[
        target_column
    ]


    # --------------------------------------
    # REMOVE MISSING TARGET VALUES
    # --------------------------------------

    usable_target = (
        target
        .dropna()
    )


    if usable_target.empty:

        raise ValueError(
            f"Target column '{target_column}' "
            "does not contain usable values."
        )


    # --------------------------------------
    # TARGET INFORMATION
    # --------------------------------------

    unique_values = int(
        usable_target.nunique()
    )


    print(
        f"Target Column: {target_column}"
    )

    print(
        f"Target Data Type: {target.dtype}"
    )

    print(
        f"Unique Target Values: {unique_values}"
    )


    # ======================================
    # BOOLEAN TARGET
    # ======================================

    if pd.api.types.is_bool_dtype(
        target
    ):

        problem_type = (
            "Classification"
        )

        detection_reason = (
            "Boolean target"
        )


    # ======================================
    # CATEGORICAL TARGET
    # ======================================

    elif isinstance(
        target.dtype,
        pd.CategoricalDtype
    ):

        problem_type = (
            "Classification"
        )

        detection_reason = (
            "Categorical target"
        )


    # ======================================
    # NON-NUMERIC TARGET
    # ======================================

    elif not pd.api.types.is_numeric_dtype(
        target
    ):

        problem_type = (
            "Classification"
        )

        detection_reason = (
            "Non-numeric target"
        )


    # ======================================
    # NUMERIC TARGET
    # ======================================

    else:

        # ----------------------------------
        # CHECK INTEGER-LIKE VALUES
        # ----------------------------------
        #
        # Examples:
        #
        # 0, 1
        # 1, 2, 3
        #
        # can reasonably represent encoded
        # classes.
        #
        # Salary values such as:
        #
        # 30000, 42000, 65000...
        #
        # should not automatically become
        # classification merely because the
        # dataset is small.
        # ----------------------------------

        numeric_target = pd.to_numeric(
            usable_target,
            errors="coerce"
        )


        integer_like = bool(
            (
                numeric_target
                .dropna()
                .mod(1)
                == 0
            ).all()
        )


        unique_numeric_values = (
            numeric_target
            .dropna()
            .unique()
        )


        if len(unique_numeric_values) > 0:

            numeric_range = (
                float(
                    max(unique_numeric_values)
                )
                -
                float(
                    min(unique_numeric_values)
                )
            )

        else:

            numeric_range = 0.0


        # ----------------------------------
        # LOW-CARDINALITY ENCODED CLASSES
        # ----------------------------------
        #
        # Conservative heuristic:
        #
        # Few unique integer-like values AND
        # a relatively small numeric range
        # are likely encoded classes.
        #
        # This avoids treating values such as
        # salaries as class labels.
        # ----------------------------------

        if (
            unique_values
            <= MAX_NUMERIC_CLASS_VALUES
            and integer_like
            and numeric_range
            <= MAX_NUMERIC_CLASS_VALUES
        ):

            problem_type = (
                "Classification"
            )

            detection_reason = (
                "Low-cardinality integer-like "
                "numeric target"
            )


        # ----------------------------------
        # NUMERIC REGRESSION TARGET
        # ----------------------------------

        else:

            problem_type = (
                "Regression"
            )

            detection_reason = (
                "Numeric target appears "
                "continuous"
            )


    # ======================================
    # RESULT
    # ======================================

    print(
        f"Detection Reason: "
        f"{detection_reason}"
    )

    print(
        f"Detected Problem Type: "
        f"{problem_type}"
    )


    return problem_type