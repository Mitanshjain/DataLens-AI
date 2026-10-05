# ==========================================
# DATALENS AI - CROSS VALIDATOR TESTS
# ==========================================

import pandas as pd
import pytest

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

from src.ml.cross_validator import (
    cross_validate_classification_models,
)


# ==========================================
# TEST PREPROCESSOR
# ==========================================

def create_test_preprocessor():
    """
    Create a simple numeric preprocessor
    for cross-validation tests.
    """

    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(),
                ["feature_1", "feature_2"],
            )
        ]
    )


# ==========================================
# TEST DATASET
# ==========================================

def create_balanced_dataset():
    """
    Create a small balanced binary
    classification dataset.
    """

    X = pd.DataFrame({
        "feature_1": [
            1, 2, 3, 4, 5,
            6, 7, 8, 9, 10,
            11, 12, 13, 14, 15,
            16, 17, 18, 19, 20,
        ],
        "feature_2": [
            20, 19, 18, 17, 16,
            15, 14, 13, 12, 11,
            10, 9, 8, 7, 6,
            5, 4, 3, 2, 1,
        ],
    })

    y = pd.Series([
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
    ])

    return X, y


# ==========================================
# BASIC CROSS-VALIDATION
# ==========================================

def test_cross_validation_returns_dataframe():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    assert isinstance(
        result,
        pd.DataFrame,
    )


# ==========================================
# FOUR MODELS
# ==========================================

def test_cross_validation_returns_all_models():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    assert set(result["Model"]) == {
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "K-Nearest Neighbors",
    }

    assert len(result) == 4


# ==========================================
# EXPECTED OUTPUT COLUMNS
# ==========================================

def test_cross_validation_output_columns():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    expected_columns = [
        "Model",
        "CV Folds",
        "CV Accuracy",
        "CV Precision",
        "CV Recall",
        "CV F1 Score",
        "Accuracy Std",
        "F1 Std",
    ]

    assert result.columns.tolist() == (
        expected_columns
    )


# ==========================================
# REQUESTED FOLDS ARE USED
# ==========================================

def test_requested_fold_count_is_used_when_safe():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    assert (
        result["CV Folds"] == 5
    ).all()


# ==========================================
# AUTOMATIC SAFE FOLD REDUCTION
# ==========================================

def test_fold_count_is_reduced_for_small_class():

    X = pd.DataFrame({
        "feature_1": [
            1, 2, 3, 4,
            5, 6, 7, 8,
        ],
        "feature_2": [
            8, 7, 6, 5,
            4, 3, 2, 1,
        ],
    })

    y = pd.Series([
        0, 0, 0, 0,
        1, 1, 1, 1,
    ])

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    assert (
        result["CV Folds"] == 4
    ).all()


# ==========================================
# METRICS WITHIN VALID RANGE
# ==========================================

def test_cross_validation_metrics_are_valid():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    metric_columns = [
        "CV Accuracy",
        "CV Precision",
        "CV Recall",
        "CV F1 Score",
    ]

    for column in metric_columns:

        assert result[column].between(
            0,
            1,
        ).all()


# ==========================================
# STANDARD DEVIATIONS NON-NEGATIVE
# ==========================================

def test_standard_deviations_are_non_negative():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    assert (
        result["Accuracy Std"] >= 0
    ).all()

    assert (
        result["F1 Std"] >= 0
    ).all()


# ==========================================
# RESULTS SORTED BY F1
# ==========================================

def test_results_are_sorted_by_f1_descending():

    X, y = create_balanced_dataset()

    preprocessor = create_test_preprocessor()

    result = cross_validate_classification_models(
        preprocessor,
        X,
        y,
        n_splits=5,
    )

    f1_scores = (
        result["CV F1 Score"]
        .tolist()
    )

    assert f1_scores == sorted(
        f1_scores,
        reverse=True,
    )


# ==========================================
# X AND Y LENGTH MISMATCH
# ==========================================

def test_mismatched_x_y_lengths_raise_error():

    X = pd.DataFrame({
        "feature_1": [1, 2, 3],
        "feature_2": [3, 2, 1],
    })

    y = pd.Series([
        0,
        1,
    ])

    preprocessor = create_test_preprocessor()

    with pytest.raises(
        ValueError,
        match="same number of rows",
    ):
        cross_validate_classification_models(
            preprocessor,
            X,
            y,
        )


# ==========================================
# TOO FEW SAMPLES
# ==========================================

def test_less_than_two_samples_raise_error():

    X = pd.DataFrame({
        "feature_1": [1],
        "feature_2": [2],
    })

    y = pd.Series([
        0,
    ])

    preprocessor = create_test_preprocessor()

    with pytest.raises(
        ValueError,
        match="At least 2 samples",
    ):
        cross_validate_classification_models(
            preprocessor,
            X,
            y,
        )


# ==========================================
# SINGLE CLASS
# ==========================================

def test_single_class_raises_error():

    X = pd.DataFrame({
        "feature_1": [
            1, 2, 3, 4,
        ],
        "feature_2": [
            4, 3, 2, 1,
        ],
    })

    y = pd.Series([
        1, 1, 1, 1,
    ])

    preprocessor = create_test_preprocessor()

    with pytest.raises(
        ValueError,
        match="at least 2 target classes",
    ):
        cross_validate_classification_models(
            preprocessor,
            X,
            y,
        )


# ==========================================
# CLASS WITH ONLY ONE SAMPLE
# ==========================================

def test_class_with_one_sample_raises_error():

    X = pd.DataFrame({
        "feature_1": [
            1, 2, 3, 4, 5,
        ],
        "feature_2": [
            5, 4, 3, 2, 1,
        ],
    })

    y = pd.Series([
        0, 0, 0, 0, 1,
    ])

    preprocessor = create_test_preprocessor()

    with pytest.raises(
        ValueError,
        match="fewer than 2 samples",
    ):
        cross_validate_classification_models(
            preprocessor,
            X,
            y,
            n_splits=5,
        )