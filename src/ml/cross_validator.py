# ==========================================
# DATALENS AI - CROSS VALIDATION ENGINE V2
# ==========================================

import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate
)


# ==========================================
# CROSS VALIDATE CLASSIFICATION MODELS
# ==========================================

def cross_validate_classification_models(
    preprocessor,
    X,
    y,
    n_splits=5
):
    """
    Compare multiple classification models
    using Stratified K-Fold Cross-Validation.

    V2 automatically reduces the number of
    folds when the smallest class contains
    fewer samples than the requested number
    of folds.
    """

    print("\n================================")
    print("CROSS-VALIDATION MODEL COMPARISON V2")
    print("================================")


    # ======================================
    # BASIC VALIDATION
    # ======================================

    if len(X) != len(y):

        raise ValueError(
            "X and y must contain the same "
            "number of rows for cross-validation."
        )


    if len(y) < 2:

        raise ValueError(
            "At least 2 samples are required "
            "for cross-validation."
        )


    # ======================================
    # CLASS DISTRIBUTION
    # ======================================

    class_counts = (
        pd.Series(y)
        .value_counts()
    )


    if len(class_counts) < 2:

        raise ValueError(
            "Classification requires at least "
            "2 target classes."
        )


    minimum_class_size = int(
        class_counts.min()
    )


    print(
        f"Class Distribution: "
        f"{class_counts.to_dict()}"
    )

    print(
        f"Smallest Class Size: "
        f"{minimum_class_size}"
    )


    # ======================================
    # DETERMINE SAFE NUMBER OF FOLDS
    # ======================================

    safe_n_splits = min(
        int(n_splits),
        minimum_class_size
    )


    if safe_n_splits < 2:

        raise ValueError(
            "Cross-validation cannot be performed "
            "because at least one class contains "
            "fewer than 2 samples."
        )


    if safe_n_splits < n_splits:

        print(
            f"⚠ Requested {n_splits}-fold "
            f"cross-validation cannot be used."
        )

        print(
            f"✓ Cross-validation automatically "
            f"reduced to {safe_n_splits} folds."
        )

    else:

        print(
            f"✓ Using {safe_n_splits}-fold "
            f"cross-validation."
        )


    # ======================================
    # CANDIDATE MODELS
    # ======================================

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


    # ======================================
    # STRATIFIED K-FOLD
    # ======================================

    cv = StratifiedKFold(
        n_splits=safe_n_splits,
        shuffle=True,
        random_state=42
    )


    # ======================================
    # SCORING METRICS
    # ======================================

    scoring = {
        "accuracy":
            "accuracy",

        "precision":
            "precision_weighted",

        "recall":
            "recall_weighted",

        "f1":
            "f1_weighted"
    }


    # ======================================
    # STORAGE
    # ======================================

    results = []


    # ======================================
    # CROSS-VALIDATE EACH MODEL
    # ======================================

    for model_name, model in models.items():

        print(
            f"\nCross-validating: "
            f"{model_name}"
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


        # ----------------------------------
        # RUN CROSS-VALIDATION
        # ----------------------------------

        scores = cross_validate(
            model_pipeline,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1
        )


        # ----------------------------------
        # MEAN SCORES
        # ----------------------------------

        mean_accuracy = (
            scores[
                "test_accuracy"
            ].mean()
        )

        mean_precision = (
            scores[
                "test_precision"
            ].mean()
        )

        mean_recall = (
            scores[
                "test_recall"
            ].mean()
        )

        mean_f1 = (
            scores[
                "test_f1"
            ].mean()
        )


        # ----------------------------------
        # SCORE VARIATION
        # ----------------------------------

        accuracy_std = (
            scores[
                "test_accuracy"
            ].std()
        )

        f1_std = (
            scores[
                "test_f1"
            ].std()
        )


        # ----------------------------------
        # STORE RESULTS
        # ----------------------------------

        results.append(
            {
                "Model":
                    model_name,

                "CV Folds":
                    safe_n_splits,

                "CV Accuracy":
                    mean_accuracy,

                "CV Precision":
                    mean_precision,

                "CV Recall":
                    mean_recall,

                "CV F1 Score":
                    mean_f1,

                "Accuracy Std":
                    accuracy_std,

                "F1 Std":
                    f1_std
            }
        )


        print(
            f"✓ {model_name} completed "
            f"{safe_n_splits}-fold "
            f"cross-validation."
        )


    # ======================================
    # CREATE RESULTS DATAFRAME
    # ======================================

    cv_results_df = pd.DataFrame(
        results
    )


    cv_results_df = (
        cv_results_df
        .sort_values(
            by="CV F1 Score",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    # ======================================
    # DISPLAY RESULTS
    # ======================================

    print("\n================================")
    print("CROSS-VALIDATION RESULTS")
    print("================================")


    display_results = (
        cv_results_df.copy()
    )


    percentage_columns = [
        "CV Accuracy",
        "CV Precision",
        "CV Recall",
        "CV F1 Score",
        "Accuracy Std",
        "F1 Std"
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


    # ======================================
    # RETURN RESULTS
    # ======================================

    return cv_results_df