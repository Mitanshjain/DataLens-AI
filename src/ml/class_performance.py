# ==========================================
# DATALENS AI - CLASS PERFORMANCE ANALYZER V1
# ==========================================

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    balanced_accuracy_score
)


def analyze_class_performance(
    y_test,
    predictions,
    positive_class
):

    """
    Analyze classification performance
    specifically for the positive class.

    Example:
        positive_class = "Yes"

    Useful for problems such as:
        churn detection
        fraud detection
        disease prediction
        loan default prediction
    """

    print("\n================================")
    print("POSITIVE CLASS PERFORMANCE")
    print("================================")


    # ==========================================
    # POSITIVE CLASS METRICS
    # ==========================================

    precision = precision_score(
        y_test,
        predictions,
        pos_label=positive_class,
        average="binary",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        pos_label=positive_class,
        average="binary",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        pos_label=positive_class,
        average="binary",
        zero_division=0
    )

    balanced_accuracy = balanced_accuracy_score(
        y_test,
        predictions
    )


    # ==========================================
    # CONFUSION MATRIX VALUES
    # ==========================================

    classes = [
        value
        for value in y_test.unique()
        if value != positive_class
    ]

    if len(classes) != 1:

        print(
            "⚠ Positive class analysis currently "
            "supports binary classification only."
        )

        return None


    negative_class = classes[0]


    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=[
            negative_class,
            positive_class
        ]
    )


    tn, fp, fn, tp = matrix.ravel()


    # ==========================================
    # SPECIFICITY
    # ==========================================

    if (tn + fp) > 0:

        specificity = (
            tn / (tn + fp)
        )

    else:

        specificity = 0.0


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print(
        f"Positive Class: {positive_class}"
    )

    print(
        f"Negative Class: {negative_class}"
    )


    print("\nPositive Class Metrics:")

    print(
        f"Precision:         {precision:.2%}"
    )

    print(
        f"Recall:            {recall:.2%}"
    )

    print(
        f"F1 Score:          {f1:.2%}"
    )

    print(
        f"Specificity:       {specificity:.2%}"
    )

    print(
        f"Balanced Accuracy: {balanced_accuracy:.2%}"
    )


    print("\nPrediction Breakdown:")

    print(
        f"True Positives:  {tp}"
    )

    print(
        f"False Positives: {fp}"
    )

    print(
        f"False Negatives: {fn}"
    )

    print(
        f"True Negatives:  {tn}"
    )


    # ==========================================
    # BASIC DIAGNOSTIC MESSAGE
    # ==========================================

    print("\nDiagnostic:")


    if recall < 0.50:

        print(
            "⚠ Positive-class recall is low. "
            "The model is missing many actual "
            "positive cases."
        )

    elif recall < 0.75:

        print(
            "⚠ Positive-class recall is moderate."
        )

    else:

        print(
            "✓ Positive-class recall is relatively high."
        )


    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return {

        "positive_class":
            positive_class,

        "negative_class":
            negative_class,

        "precision":
            precision,

        "recall":
            recall,

        "f1_score":
            f1,

        "specificity":
            specificity,

        "balanced_accuracy":
            balanced_accuracy,

        "true_positive":
            int(tp),

        "false_positive":
            int(fp),

        "false_negative":
            int(fn),

        "true_negative":
            int(tn)
    }