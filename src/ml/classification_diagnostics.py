# ==========================================
# DATALENS AI
# CLASSIFICATION MODEL DIAGNOSTICS V1
# ==========================================

import numpy as np

from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def run_classification_diagnostics(
    trained_model,
    X_test,
    y_test,
    positive_class=None
):
    """
    Generate deeper diagnostics for a trained
    classification model.

    Binary classification:
        ROC curve
        ROC AUC
        Precision-Recall curve
        Average Precision
        Threshold analysis
        Error analysis

    Multiclass classification:
        Basic prediction-error analysis only.

    Probability-based diagnostics require
    predict_proba().
    """

    print("\n================================")
    print("CLASSIFICATION DIAGNOSTICS")
    print("================================")

    predictions = trained_model.predict(
        X_test
    )

    model = (
        trained_model
        .named_steps["model"]
    )

    class_labels = list(
        model.classes_
    )

    results = {
        "diagnostic_type":
            "classification",

        "class_labels":
            class_labels,

        "roc":
            None,

        "precision_recall":
            None,

        "threshold_analysis":
            None,

        "error_analysis":
            None
    }

    # ==========================================
    # ERROR ANALYSIS
    # ==========================================

    incorrect_mask = (
        np.asarray(predictions)
        != np.asarray(y_test)
    )

    incorrect_count = int(
        incorrect_mask.sum()
    )

    total_samples = int(
        len(y_test)
    )

    error_rate = (
        incorrect_count / total_samples
        if total_samples > 0
        else 0.0
    )

    error_analysis = {
        "total_samples":
            total_samples,

        "correct_predictions":
            int(
                total_samples
                - incorrect_count
            ),

        "incorrect_predictions":
            incorrect_count,

        "error_rate":
            float(error_rate)
    }

    # ==========================================
    # CLASS-WISE ERROR COUNTS
    # ==========================================

    class_errors = {}

    y_test_array = np.asarray(
        y_test
    )

    predictions_array = np.asarray(
        predictions
    )

    for class_label in class_labels:

        class_mask = (
            y_test_array
            == class_label
        )

        class_total = int(
            class_mask.sum()
        )

        class_incorrect = int(
            (
                class_mask
                & (
                    predictions_array
                    != y_test_array
                )
            ).sum()
        )

        class_errors[
            str(class_label)
        ] = {
            "samples":
                class_total,

            "incorrect_predictions":
                class_incorrect,

            "error_rate":
                float(
                    class_incorrect
                    / class_total
                )
                if class_total > 0
                else 0.0
        }

    error_analysis[
        "class_errors"
    ] = class_errors

    results[
        "error_analysis"
    ] = error_analysis

    print(
        f"Total Test Samples: "
        f"{total_samples}"
    )

    print(
        f"Incorrect Predictions: "
        f"{incorrect_count}"
    )

    print(
        f"Error Rate: "
        f"{error_rate:.2%}"
    )

    # ==========================================
    # BINARY-ONLY DIAGNOSTICS
    # ==========================================

    if len(class_labels) != 2:

        print(
            "ℹ ROC, Precision-Recall and "
            "threshold diagnostics currently "
            "run only for binary classification."
        )

        print(
            "✓ Classification error analysis complete."
        )

        return results

    # ==========================================
    # RESOLVE POSITIVE CLASS
    # ==========================================

    if positive_class is None:

        print(
            "ℹ Positive class was not specified."
        )

        print(
            "ℹ Probability-based binary diagnostics "
            "were skipped to avoid assuming which "
            "class should be treated as positive."
        )

        return results

    if positive_class not in class_labels:

        print(
            "⚠ Positive class was not found in "
            "the trained model classes."
        )

        return results

    results[
        "positive_class"
    ] = positive_class

    negative_classes = [
        value
        for value in class_labels
        if value != positive_class
    ]

    negative_class = (
        negative_classes[0]
    )

    results[
        "negative_class"
    ] = negative_class

    # ==========================================
    # CHECK PROBABILITY SUPPORT
    # ==========================================

    if not hasattr(
        trained_model,
        "predict_proba"
    ):

        print(
            "⚠ Model does not support "
            "predict_proba()."
        )

        print(
            "Probability-based diagnostics skipped."
        )

        return results

    # ==========================================
    # POSITIVE-CLASS PROBABILITIES
    # ==========================================

    positive_index = (
        class_labels.index(
            positive_class
        )
    )

    probabilities = (
        trained_model
        .predict_proba(
            X_test
        )[:, positive_index]
    )

    y_binary = (
        np.asarray(y_test)
        == positive_class
    ).astype(int)

    # ==========================================
    # ROC CURVE
    # ==========================================

    if len(np.unique(y_binary)) == 2:

        fpr, tpr, roc_thresholds = (
            roc_curve(
                y_binary,
                probabilities
            )
        )

        roc_auc = roc_auc_score(
            y_binary,
            probabilities
        )

        results["roc"] = {
            "auc":
                float(roc_auc),

            "false_positive_rate":
                [
                    float(value)
                    for value in fpr
                ],

            "true_positive_rate":
                [
                    float(value)
                    for value in tpr
                ],

            "thresholds":
                [
                    (
                        float(value)
                        if np.isfinite(value)
                        else None
                    )
                    for value
                    in roc_thresholds
                ]
        }

        print(
            f"ROC AUC: {roc_auc:.4f}"
        )

    else:

        print(
            "⚠ ROC curve could not be calculated "
            "because the test set does not contain "
            "both binary classes."
        )

    # ==========================================
    # PRECISION-RECALL CURVE
    # ==========================================

    if len(np.unique(y_binary)) == 2:

        (
            pr_precision,
            pr_recall,
            pr_thresholds

        ) = precision_recall_curve(
            y_binary,
            probabilities
        )

        average_precision = (
            average_precision_score(
                y_binary,
                probabilities
            )
        )

        results[
            "precision_recall"
        ] = {
            "average_precision":
                float(
                    average_precision
                ),

            "precision":
                [
                    float(value)
                    for value
                    in pr_precision
                ],

            "recall":
                [
                    float(value)
                    for value
                    in pr_recall
                ],

            "thresholds":
                [
                    float(value)
                    for value
                    in pr_thresholds
                ]
        }

        print(
            f"Average Precision: "
            f"{average_precision:.4f}"
        )

    # ==========================================
    # THRESHOLD ANALYSIS
    # ==========================================
    #
    # We evaluate a fixed set of thresholds.
    #
    # We do NOT automatically declare one
    # threshold as universally optimal because
    # the correct threshold depends on business
    # costs and consequences.
    # ==========================================

    threshold_values = [
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.80,
        0.90
    ]

    threshold_results = []

    for threshold in threshold_values:

        threshold_predictions = (
            probabilities
            >= threshold
        ).astype(int)

        precision = precision_score(
            y_binary,
            threshold_predictions,
            zero_division=0
        )

        recall = recall_score(
            y_binary,
            threshold_predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_binary,
            threshold_predictions,
            zero_division=0
        )

        matrix = confusion_matrix(
            y_binary,
            threshold_predictions,
            labels=[0, 1]
        )

        tn, fp, fn, tp = (
            matrix.ravel()
        )

        specificity = (
            tn / (tn + fp)
            if (tn + fp) > 0
            else 0.0
        )

        threshold_results.append(
            {
                "threshold":
                    float(threshold),

                "precision":
                    float(precision),

                "recall":
                    float(recall),

                "f1_score":
                    float(f1),

                "specificity":
                    float(specificity),

                "true_positive":
                    int(tp),

                "false_positive":
                    int(fp),

                "false_negative":
                    int(fn),

                "true_negative":
                    int(tn)
            }
        )

    results[
        "threshold_analysis"
    ] = threshold_results

    print(
        "✓ Threshold analysis complete."
    )

    print(
        "✓ ROC diagnostics complete."
    )

    print(
        "✓ Precision-Recall diagnostics complete."
    )

    print(
        "✓ Classification diagnostics complete."
    )

    return results