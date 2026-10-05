# ==========================================
# DATALENS AI - MODEL COMPARISON ENGINE V1
# ==========================================

import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def compare_classification_models(
    preprocessor,
    X_train,
    X_test,
    y_train,
    y_test
):

    """
    Train and evaluate multiple classification
    models using the same preprocessing pipeline.

    Returns:
        results_df:
            Comparison table containing model
            performance metrics.

        trained_models:
            Dictionary containing all fitted
            model pipelines.
    """

    print("\n================================")
    print("CLASSIFICATION MODEL COMPARISON")
    print("================================")


    # ==========================================
    # CANDIDATE MODELS
    # ==========================================

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=1000,
                random_state=42
            ),

        "Decision Tree":
            DecisionTreeClassifier(
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

        "K-Nearest Neighbors":
            KNeighborsClassifier(
                n_neighbors=5
            )
    }


    # ==========================================
    # STORAGE
    # ==========================================

    results = []

    trained_models = {}


    # ==========================================
    # TRAIN AND EVALUATE EACH MODEL
    # ==========================================

    for model_name, model in models.items():

        print(
            f"\nTraining: {model_name}"
        )


        # Every model receives its own copy
        # of the preprocessing pipeline.

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
        # TRAIN MODEL
        # --------------------------------------

        model_pipeline.fit(
            X_train,
            y_train
        )


        # --------------------------------------
        # MAKE PREDICTIONS
        # --------------------------------------

        predictions = model_pipeline.predict(
            X_test
        )


        # --------------------------------------
        # CALCULATE METRICS
        # --------------------------------------

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )


        # --------------------------------------
        # STORE RESULTS
        # --------------------------------------

        results.append(
            {
                "Model": model_name,
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1 Score": f1
            }
        )


        trained_models[
            model_name
        ] = model_pipeline


        print(
            f"✓ {model_name} trained and evaluated."
        )


    # ==========================================
    # CREATE COMPARISON TABLE
    # ==========================================

    results_df = pd.DataFrame(
        results
    )


    # Sort only for convenient inspection.
    # We are not yet declaring the highest
    # score to be the final production model.

    results_df = results_df.sort_values(
        by="F1 Score",
        ascending=False
    ).reset_index(
        drop=True
    )


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print("\n================================")
    print("MODEL COMPARISON RESULTS")
    print("================================")

    display_results = results_df.copy()

    metric_columns = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]

    display_results[
        metric_columns
    ] = (
        display_results[
            metric_columns
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