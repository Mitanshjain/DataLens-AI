# ==========================================
# DATALENS AI - CLASS IMBALANCE HANDLER V1
# ==========================================

import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix
)


def compare_imbalance_strategies(
    preprocessor,
    X_train,
    X_test,
    y_train,
    y_test,
    positive_class
):

    """
    Compare normal classification models
    with class-weighted versions.

    This helps evaluate whether class weighting
    improves minority / positive-class detection.
    """

    print("\n================================")
    print("CLASS IMBALANCE STRATEGY ANALYSIS")
    print("================================")


    # ==========================================
    # DEFINE MODEL STRATEGIES
    # ==========================================

    strategies = {

        "Logistic Regression - Normal":
            LogisticRegression(
                max_iter=1000,
                random_state=42
            ),

        "Logistic Regression - Balanced":
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            ),

        "Decision Tree - Normal":
            DecisionTreeClassifier(
                random_state=42
            ),

        "Decision Tree - Balanced":
            DecisionTreeClassifier(
                class_weight="balanced",
                random_state=42
            ),

        "Random Forest - Normal":
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

        "Random Forest - Balanced":
            RandomForestClassifier(
                n_estimators=100,
                class_weight="balanced",
                random_state=42
            )
    }


    # ==========================================
    # FIND NEGATIVE CLASS
    # ==========================================

    unique_classes = list(
        y_train.unique()
    )

    negative_classes = [
        value
        for value in unique_classes
        if value != positive_class
    ]


    if len(negative_classes) != 1:

        print(
            "⚠ Imbalance strategy analysis "
            "currently supports binary "
            "classification only."
        )

        return None, None


    negative_class = negative_classes[0]


    # ==========================================
    # STORAGE
    # ==========================================

    results = []

    trained_models = {}


    # ==========================================
    # TRAIN AND EVALUATE
    # ==========================================

    for strategy_name, model in strategies.items():

        print(
            f"\nTesting: {strategy_name}"
        )


        model_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    clone(preprocessor)
                ),
                (
                    "model",
                    model
                )
            ]
        )


        # --------------------------------------
        # TRAIN
        # --------------------------------------

        model_pipeline.fit(
            X_train,
            y_train
        )


        # --------------------------------------
        # PREDICT
        # --------------------------------------

        predictions = model_pipeline.predict(
            X_test
        )


        # --------------------------------------
        # OVERALL METRICS
        # --------------------------------------

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        balanced_accuracy = (
            balanced_accuracy_score(
                y_test,
                predictions
            )
        )


        # --------------------------------------
        # POSITIVE CLASS METRICS
        # --------------------------------------

        positive_precision = precision_score(
            y_test,
            predictions,
            pos_label=positive_class,
            average="binary",
            zero_division=0
        )

        positive_recall = recall_score(
            y_test,
            predictions,
            pos_label=positive_class,
            average="binary",
            zero_division=0
        )

        positive_f1 = f1_score(
            y_test,
            predictions,
            pos_label=positive_class,
            average="binary",
            zero_division=0
        )


        # --------------------------------------
        # CONFUSION MATRIX
        # --------------------------------------

        matrix = confusion_matrix(
            y_test,
            predictions,
            labels=[
                negative_class,
                positive_class
            ]
        )

        tn, fp, fn, tp = matrix.ravel()


        # --------------------------------------
        # STORE RESULT
        # --------------------------------------

        results.append(
            {
                "Strategy": strategy_name,

                "Accuracy":
                    accuracy,

                "Balanced Accuracy":
                    balanced_accuracy,

                "Positive Precision":
                    positive_precision,

                "Positive Recall":
                    positive_recall,

                "Positive F1":
                    positive_f1,

                "TP":
                    int(tp),

                "FP":
                    int(fp),

                "FN":
                    int(fn),

                "TN":
                    int(tn)
            }
        )


        trained_models[
            strategy_name
        ] = model_pipeline


        print(
            f"✓ {strategy_name} evaluated."
        )


    # ==========================================
    # CREATE RESULT TABLE
    # ==========================================

    results_df = pd.DataFrame(
        results
    )


    # Sorting is only for convenient inspection.
    # We are not automatically selecting a
    # production model here.

    results_df = (
        results_df
        .sort_values(
            by="Positive F1",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print("\n================================")
    print("IMBALANCE STRATEGY RESULTS")
    print("================================")


    display_results = (
        results_df.copy()
    )


    percentage_columns = [
        "Accuracy",
        "Balanced Accuracy",
        "Positive Precision",
        "Positive Recall",
        "Positive F1"
    ]


    display_results[
        percentage_columns
    ] = (
        display_results[
            percentage_columns
        ] * 100
    ).round(2)


    print(
        display_results.to_string(
            index=False
        )
    )


    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return (
        results_df,
        trained_models
    )