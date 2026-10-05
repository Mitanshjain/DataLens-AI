# ==========================================
# DATALENS AI - PROBLEM DETECTOR TESTS
# ==========================================

import pandas as pd
import pytest

from src.ml.problem_detector import detect_problem_type


# ==========================================
# TEST 1: STRING TARGET
# ==========================================

def test_string_target_is_classification():

    df = pd.DataFrame({
        "age": [22, 25, 30, 35],
        "purchased": ["Yes", "No", "Yes", "No"]
    })

    result = detect_problem_type(
        df,
        "purchased"
    )

    assert result == "Classification"


# ==========================================
# TEST 2: BOOLEAN TARGET
# ==========================================

def test_boolean_target_is_classification():

    df = pd.DataFrame({
        "age": [22, 25, 30, 35],
        "approved": [True, False, True, False]
    })

    result = detect_problem_type(
        df,
        "approved"
    )

    assert result == "Classification"


# ==========================================
# TEST 3: ENCODED NUMERIC CLASSES
# ==========================================

def test_low_cardinality_integer_target_is_classification():

    df = pd.DataFrame({
        "feature": [10, 20, 30, 40, 50, 60],
        "target": [0, 1, 0, 1, 0, 1]
    })

    result = detect_problem_type(
        df,
        "target"
    )

    assert result == "Classification"


# ==========================================
# TEST 4: MULTI-CLASS NUMERIC TARGET
# ==========================================

def test_multiclass_integer_target_is_classification():

    df = pd.DataFrame({
        "feature": [10, 20, 30, 40, 50, 60],
        "target": [1, 2, 3, 1, 2, 3]
    })

    result = detect_problem_type(
        df,
        "target"
    )

    assert result == "Classification"


# ==========================================
# TEST 5: CONTINUOUS NUMERIC TARGET
# ==========================================

def test_continuous_numeric_target_is_regression():

    df = pd.DataFrame({
        "experience": [1, 2, 3, 4, 5],
        "salary": [
            32000.5,
            41000.8,
            52500.2,
            63000.7,
            74500.4
        ]
    })

    result = detect_problem_type(
        df,
        "salary"
    )

    assert result == "Regression"


# ==========================================
# TEST 6: LARGE INTEGER VALUES
# ==========================================

def test_large_integer_numeric_target_is_regression():

    df = pd.DataFrame({
        "experience": [1, 2, 3, 4, 5],
        "salary": [
            30000,
            40000,
            50000,
            60000,
            70000
        ]
    })

    result = detect_problem_type(
        df,
        "salary"
    )

    assert result == "Regression"


# ==========================================
# TEST 7: MISSING TARGET COLUMN
# ==========================================

def test_missing_target_column_raises_error():

    df = pd.DataFrame({
        "age": [22, 25, 30],
        "city": ["Jaipur", "Delhi", "Mumbai"]
    })

    with pytest.raises(
        ValueError,
        match="Target column"
    ):
        detect_problem_type(
            df,
            "purchased"
        )


# ==========================================
# TEST 8: ALL TARGET VALUES MISSING
# ==========================================

def test_all_missing_target_values_raise_error():

    df = pd.DataFrame({
        "feature": [1, 2, 3],
        "target": [None, None, None]
    })

    with pytest.raises(
        ValueError,
        match="does not contain usable values"
    ):
        detect_problem_type(
            df,
            "target"
        )


# ==========================================
# TEST 9: PARTIAL MISSING TARGET VALUES
# ==========================================

def test_missing_values_are_ignored_during_detection():

    df = pd.DataFrame({
        "feature": [10, 20, 30, 40, 50],
        "target": [0, 1, None, 0, 1]
    })

    result = detect_problem_type(
        df,
        "target"
    )

    assert result == "Classification"


# ==========================================
# TEST 10: FEW UNIQUE BUT LARGE RANGE
# ==========================================

def test_low_cardinality_large_range_is_regression():

    df = pd.DataFrame({
        "feature": [1, 2, 3, 4, 5, 6],
        "target": [
            100,
            500,
            1000,
            100,
            500,
            1000
        ]
    })

    result = detect_problem_type(
        df,
        "target"
    )

    assert result == "Regression"