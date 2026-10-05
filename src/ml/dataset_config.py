# ==========================================
# DATALENS AI - DATASET CONFIGURATION V2
# ==========================================


def get_available_targets(df):
    """
    Return all dataset columns that can be
    presented to the user as target options.
    """

    columns = df.columns.tolist()

    print("\n================================")
    print("DATASET TARGET CONFIGURATION")
    print("================================")

    print("Available Target Columns:")

    for index, column in enumerate(
        columns,
        start=1
    ):

        print(
            f"{index}. {column}"
        )

    return columns


# ==========================================
# VALIDATE TARGET COLUMN
# ==========================================

def validate_target_column(
    df,
    target_column
):
    """
    Validate that the selected target exists
    and contains enough usable information
    for machine learning.
    """

    # --------------------------------------
    # TARGET EXISTS
    # --------------------------------------

    if target_column not in df.columns:

        raise ValueError(
            f"Target column '{target_column}' "
            f"does not exist in the dataset."
        )


    target = df[
        target_column
    ]


    # --------------------------------------
    # TARGET NOT COMPLETELY MISSING
    # --------------------------------------

    if target.isna().all():

        raise ValueError(
            f"Target column '{target_column}' "
            f"contains only missing values."
        )


    # --------------------------------------
    # NON-MISSING TARGET ROWS
    # --------------------------------------

    usable_target = (
        target.dropna()
    )


    if len(usable_target) < 2:

        raise ValueError(
            f"Target column '{target_column}' "
            "does not contain enough non-missing "
            "rows for machine learning."
        )


    # --------------------------------------
    # UNIQUE TARGET VALUES
    # --------------------------------------

    unique_values = (
        usable_target.nunique()
    )


    if unique_values < 2:

        raise ValueError(
            f"Target column '{target_column}' "
            f"must contain at least 2 unique values."
        )


    # --------------------------------------
    # FEATURE AVAILABILITY
    # --------------------------------------

    feature_columns = [
        column
        for column in df.columns
        if column != target_column
    ]


    if not feature_columns:

        raise ValueError(
            "The dataset must contain at least "
            "one feature column in addition to "
            "the target column."
        )


    # --------------------------------------
    # STATUS
    # --------------------------------------

    missing_target_rows = int(
        target.isna().sum()
    )


    print(
        f"\n✓ Selected Target: {target_column}"
    )

    print(
        f"✓ Unique Target Values: {unique_values}"
    )

    print(
        f"✓ Usable Target Rows: {len(usable_target)}"
    )

    print(
        f"✓ Missing Target Rows: "
        f"{missing_target_rows}"
    )


    if missing_target_rows > 0:

        print(
            "ℹ Missing target rows will be "
            "excluded before ML training."
        )


    return True


# ==========================================
# CLASS CONFIGURATION
# ==========================================

def get_class_configuration(
    y,
    problem_type,
    positive_class=None
):
    """
    Build class configuration dynamically.

    Positive-class analysis is only relevant
    for binary classification.
    """

    if problem_type != "Classification":

        return {
            "classes": None,
            "classification_type": None,
            "positive_class": None
        }


    clean_y = (
        y.dropna()
    )


    classes = (
        clean_y
        .unique()
        .tolist()
    )


    if len(classes) < 2:

        raise ValueError(
            "Classification target must contain "
            "at least 2 classes."
        )


    # ======================================
    # BINARY CLASSIFICATION
    # ======================================

    if len(classes) == 2:

        classification_type = (
            "Binary Classification"
        )


        if positive_class is not None:

            if positive_class not in classes:

                raise ValueError(
                    f"Positive class "
                    f"'{positive_class}' "
                    f"is not present in target."
                )


        print(
            f"Classification Type: "
            f"{classification_type}"
        )

        print(
            f"Classes: {classes}"
        )


        if positive_class is None:

            print(
                "Positive Class: "
                "Not configured"
            )

        else:

            print(
                f"Positive Class: "
                f"{positive_class}"
            )


        return {
            "classes":
                classes,

            "classification_type":
                classification_type,

            "positive_class":
                positive_class
        }


    # ======================================
    # MULTICLASS CLASSIFICATION
    # ======================================

    classification_type = (
        "Multiclass Classification"
    )


    print(
        f"Classification Type: "
        f"{classification_type}"
    )

    print(
        f"Classes: {classes}"
    )

    print(
        "Positive Class: "
        "Not applicable"
    )


    return {
        "classes":
            classes,

        "classification_type":
            classification_type,

        "positive_class":
            None
    }