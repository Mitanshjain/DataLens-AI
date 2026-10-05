# ==========================================
# DATALENS AI - DATASET CONFIG TESTS
# ==========================================

import pandas as pd
import pytest

from src.ml.dataset_config import (
    get_available_targets,
    validate_target_column,
    get_class_configuration,
)


# ==========================================
# GET AVAILABLE TARGETS
# ==========================================

def test_get_available_targets_returns_all_columns():

    df = pd.DataFrame({
        "age": [22, 30],
        "city": ["Jaipur", "Delhi"],
        "purchased": ["Yes", "No"],
    })

    result = get_available_targets(df)

    assert result == [
        "age",
        "city",
        "purchased",
    ]


def test_get_available_targets_empty_dataframe():

    df = pd.DataFrame()

    result = get_available_targets(df)

    assert result == []


# ==========================================
# VALID TARGET
# ==========================================

def test_valid_target_returns_true():

    df = pd.DataFrame({
        "age": [22, 25, 30, 35],
        "purchased": ["Yes", "No", "Yes", "No"],
    })

    result = validate_target_column(
        df,
        "purchased",
    )

    assert result is True


# ==========================================
# TARGET DOES NOT EXIST
# ==========================================

def test_missing_target_column_raises_error():

    df = pd.DataFrame({
        "age": [22, 25, 30],
        "city": ["Jaipur", "Delhi", "Mumbai"],
    })

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        validate_target_column(
            df,
            "purchased",
        )


# ==========================================
# TARGET COMPLETELY MISSING
# ==========================================

def test_all_missing_target_raises_error():

    df = pd.DataFrame({
        "age": [22, 25, 30],
        "target": [None, None, None],
    })

    with pytest.raises(
        ValueError,
        match="contains only missing values",
    ):
        validate_target_column(
            df,
            "target",
        )


# ==========================================
# NOT ENOUGH USABLE TARGET ROWS
# ==========================================

def test_single_usable_target_row_raises_error():

    df = pd.DataFrame({
        "feature": [10, 20, 30],
        "target": ["Yes", None, None],
    })

    with pytest.raises(
        ValueError,
        match="does not contain enough non-missing rows",
    ):
        validate_target_column(
            df,
            "target",
        )


# ==========================================
# CONSTANT TARGET
# ==========================================

def test_constant_target_raises_error():

    df = pd.DataFrame({
        "feature": [10, 20, 30, 40],
        "target": ["Yes", "Yes", "Yes", "Yes"],
    })

    with pytest.raises(
        ValueError,
        match="must contain at least 2 unique values",
    ):
        validate_target_column(
            df,
            "target",
        )


# ==========================================
# TARGET WITHOUT FEATURES
# ==========================================

def test_dataset_with_only_target_raises_error():

    df = pd.DataFrame({
        "target": ["Yes", "No", "Yes"],
    })

    with pytest.raises(
        ValueError,
        match="at least one feature column",
    ):
        validate_target_column(
            df,
            "target",
        )


# ==========================================
# PARTIAL MISSING TARGET
# ==========================================

def test_partial_missing_target_is_valid():

    df = pd.DataFrame({
        "feature": [10, 20, 30, 40],
        "target": ["Yes", "No", None, "Yes"],
    })

    result = validate_target_column(
        df,
        "target",
    )

    assert result is True


# ==========================================
# REGRESSION CONFIGURATION
# ==========================================

def test_regression_has_no_class_configuration():

    y = pd.Series([
        100.5,
        200.2,
        300.8,
    ])

    result = get_class_configuration(
        y,
        "Regression",
    )

    assert result == {
        "classes": None,
        "classification_type": None,
        "positive_class": None,
    }


# ==========================================
# BINARY CLASSIFICATION
# ==========================================

def test_binary_classification_configuration():

    y = pd.Series([
        "Yes",
        "No",
        "Yes",
        "No",
    ])

    result = get_class_configuration(
        y,
        "Classification",
    )

    assert set(result["classes"]) == {
        "Yes",
        "No",
    }

    assert (
        result["classification_type"]
        == "Binary Classification"
    )

    assert result["positive_class"] is None


# ==========================================
# BINARY WITH POSITIVE CLASS
# ==========================================

def test_binary_classification_positive_class():

    y = pd.Series([
        "Yes",
        "No",
        "Yes",
        "No",
    ])

    result = get_class_configuration(
        y,
        "Classification",
        positive_class="Yes",
    )

    assert result["positive_class"] == "Yes"

    assert (
        result["classification_type"]
        == "Binary Classification"
    )


# ==========================================
# INVALID POSITIVE CLASS
# ==========================================

def test_invalid_positive_class_raises_error():

    y = pd.Series([
        "Yes",
        "No",
        "Yes",
        "No",
    ])

    with pytest.raises(
        ValueError,
        match="is not present in target",
    ):
        get_class_configuration(
            y,
            "Classification",
            positive_class="Maybe",
        )


# ==========================================
# MULTICLASS CLASSIFICATION
# ==========================================

def test_multiclass_configuration():

    y = pd.Series([
        "Low",
        "Medium",
        "High",
        "Low",
    ])

    result = get_class_configuration(
        y,
        "Classification",
    )

    assert set(result["classes"]) == {
        "Low",
        "Medium",
        "High",
    }

    assert (
        result["classification_type"]
        == "Multiclass Classification"
    )

    assert result["positive_class"] is None


# ==========================================
# CLASSIFICATION WITH ONE CLASS
# ==========================================

def test_single_class_classification_raises_error():

    y = pd.Series([
        "Yes",
        "Yes",
        "Yes",
    ])

    with pytest.raises(
        ValueError,
        match="at least 2 classes",
    ):
        get_class_configuration(
            y,
            "Classification",
        )


# ==========================================
# MISSING VALUES IN CLASS CONFIGURATION
# ==========================================

def test_class_configuration_ignores_missing_values():

    y = pd.Series([
        "Yes",
        None,
        "No",
        "Yes",
    ])

    result = get_class_configuration(
        y,
        "Classification",
        positive_class="Yes",
    )

    assert set(result["classes"]) == {
        "Yes",
        "No",
    }

    assert result["positive_class"] == "Yes"