# ==========================================
# DATALENS AI - CLASSIFICATION EVALUATOR V2
# ==========================================

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# CLASSIFICATION MODEL EVALUATION
# ==========================================

def evaluate_classification_model(
    y_test,
    predictions,
    labels=None
):
    """
    Evaluate a classification model using
    standard classification metrics.

    V2 improvements:
    - Handles small test sets safely.
    - Handles classes missing from y_test.
    - Handles classes appearing only in predictions.
    - Keeps metric labels as their original values.
    - Uses strings only for display names.
    """

    print("\n================================")
    print("MODEL EVALUATION V2")
    print("================================")


    # --------------------------------------
    # BASIC VALIDATION
    # --------------------------------------

    if len(y_test) == 0:

        raise ValueError(
            "Cannot evaluate classification model "
            "because y_test is empty."
        )


    if len(y_test) != len(predictions):

        raise ValueError(
            "y_test and predictions must contain "
            "the same number of samples."
        )


    # --------------------------------------
    # DETERMINE SAFE LABEL SET
    # --------------------------------------
    #
    # We include:
    # 1. configured/model labels
    # 2. labels actually present in y_test
    # 3. labels produced by predictions
    #
    # This prevents evaluation failures when
    # a small test split does not contain
    # every class.
    # --------------------------------------

    configured_labels = (
        list(labels)
        if labels is not None
        else []
    )


    actual_labels = (
        np.unique(
            np.concatenate(
                [
                    np.asarray(y_test),
                    np.asarray(predictions)
                ]
            )
        )
        .tolist()
    )


    evaluation_labels = []

    for label in (
        configured_labels
        + actual_labels
    ):

        if label not in evaluation_labels:

            evaluation_labels.append(
                label
            )


    if not evaluation_labels:

        raise ValueError(
            "No class labels are available "
            "for model evaluation."
        )


    # --------------------------------------
    # DISPLAY NAMES
    # --------------------------------------

    target_names = [
        str(label)
        for label in evaluation_labels
    ]


    # --------------------------------------
    # BASIC METRICS
    # --------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    precision = precision_score(
        y_test,
        predictions,
        labels=evaluation_labels,
        average="weighted",
        zero_division=0
    )


    recall = recall_score(
        y_test,
        predictions,
        labels=evaluation_labels,
        average="weighted",
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        predictions,
        labels=evaluation_labels,
        average="weighted",
        zero_division=0
    )


    # --------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=evaluation_labels
    )


    # --------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------

    report = classification_report(
        y_test,
        predictions,
        labels=evaluation_labels,
        target_names=target_names,
        zero_division=0
    )


    # --------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------

    print(
        f"Accuracy:  {accuracy:.2%}"
    )

    print(
        f"Precision: {precision:.2%}"
    )

    print(
        f"Recall:    {recall:.2%}"
    )

    print(
        f"F1 Score:  {f1:.2%}"
    )

    print(
        f"Test Samples: {len(y_test)}"
    )

    print(
        f"Configured Labels: "
        f"{configured_labels}"
    )

    print(
        f"Evaluation Labels: "
        f"{evaluation_labels}"
    )


    print("\nConfusion Matrix:")

    print(
        matrix
    )


    print(
        "\nClassification Report:"
    )

    print(
        report
    )


    # --------------------------------------
    # RELIABILITY WARNING
    # --------------------------------------

    if len(y_test) < 30:

        print(
            "⚠ Test dataset is too small "
            "for reliable model evaluation."
        )


    # --------------------------------------
    # CHECK TEST CLASS COVERAGE
    # --------------------------------------

    test_labels = (
        np.unique(
            np.asarray(y_test)
        )
        .tolist()
    )


    missing_test_classes = [
        label
        for label in evaluation_labels
        if label not in test_labels
    ]


    if missing_test_classes:

        print(
            "⚠ Some classes are not represented "
            "in the test split:"
        )

        print(
            missing_test_classes
        )


    # --------------------------------------
    # RETURN RESULTS
    # --------------------------------------

    return {

        "accuracy":
            float(accuracy),

        "precision":
            float(precision),

        "recall":
            float(recall),

        "f1_score":
            float(f1),

        "confusion_matrix":
            matrix,

        "classification_report":
            report,

        "evaluation_labels":
            evaluation_labels,

        "missing_test_classes":
            missing_test_classes
    }