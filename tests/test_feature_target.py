# ==========================================
# DATALENS AI - FEATURE TARGET TESTS
# ==========================================

import pandas as pd
import pytest

from src.ml.feature_target import (
    detect_identifier_columns,
    separate_features_target,
)


# ==========================================
# IDENTIFIER DETECTION
# ==========================================

def test_detect_exact_id_column():

    X = pd.DataFrame({
        "id": [1, 2, 3],
        "age": [22, 30, 40],
    })

    result = detect_identifier_columns(X)

    assert result == ["id"]


def test_detect_column_ending_with_id():

    X = pd.DataFrame({
        "customer_id": [101, 102, 103],
        "income": [30000, 40000, 50000],
    })

    result = detect_identifier_columns(X)

    assert result == ["customer_id"]


def test_detect_column_starting_with_id():

    X = pd.DataFrame({
        "id_customer": [101, 102, 103],
        "income": [30000, 40000, 50000],
    })

    result = detect_identifier_columns(X)

    assert result == ["id_customer"]


def test_identifier_detection_is_case_insensitive():

    X = pd.DataFrame({
        "Customer_ID": [1, 2, 3],
        "AGE": [20, 30, 40],
    })

    result = detect_identifier_columns(X)

    assert result == ["Customer_ID"]


def test_high_cardinality_column_is_not_automatically_identifier():

    X = pd.DataFrame({
        "email": [
            "a@test.com",
            "b@test.com",
            "c@test.com",
        ],
        "age": [20, 30, 40],
    })

    result = detect_identifier_columns(X)

    assert result == []


# ==========================================
# BASIC FEATURE TARGET SEPARATION
# ==========================================

def test_separate_features_and_target():

    df = pd.DataFrame({
        "age": [22, 25, 30, 35],
        "income": [30000, 40000, 50000, 60000],
        "purchased": ["Yes", "No", "Yes", "No"],
    })

    X, y = separate_features_target(
        df,
        "purchased",
    )

    assert X.columns.tolist() == [
        "age",
        "income",
    ]

    assert y.name == "purchased"

    assert len(X) == 4
    assert len(y) == 4


# ==========================================
# TARGET MUST NOT REMAIN IN FEATURES
# ==========================================

def test_target_is_removed_from_features():

    df = pd.DataFrame({
        "age": [20, 30, 40, 50],
        "target": [0, 1, 0, 1],
    })

    X, _ = separate_features_target(
        df,
        "target",
    )

    assert "target" not in X.columns


# ==========================================
# IDENTIFIER REMOVAL
# ==========================================

def test_identifier_column_is_removed():

    df = pd.DataFrame({
        "customer_id": [101, 102, 103, 104],
        "age": [20, 30, 40, 50],
        "target": [0, 1, 0, 1],
    })

    X, y = separate_features_target(
        df,
        "target",
    )

    assert "customer_id" not in X.columns
    assert X.columns.tolist() == ["age"]
    assert len(X) == len(y)


def test_multiple_identifier_columns_are_removed():

    df = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "customer_id": [101, 102, 103, 104],
        "id_order": [501, 502, 503, 504],
        "age": [20, 30, 40, 50],
        "target": [0, 1, 0, 1],
    })

    X, _ = separate_features_target(
        df,
        "target",
    )

    assert X.columns.tolist() == ["age"]


# ==========================================
# MISSING TARGET ROWS
# ==========================================

def test_missing_target_rows_are_removed():

    df = pd.DataFrame({
        "age": [20, 30, 40, 50],
        "target": [0, 1, None, 0],
    })

    X, y = separate_features_target(
        df,
        "target",
    )

    assert len(X) == 3
    assert len(y) == 3

    assert y.isna().sum() == 0

    assert X.index.tolist() == [
        0,
        1,
        3,
    ]

    assert y.index.tolist() == [
        0,
        1,
        3,
    ]


# ==========================================
# MISSING FEATURE VALUES
# ==========================================

def test_missing_feature_values_are_preserved():

    df = pd.DataFrame({
        "age": [20, None, 40, 50],
        "income": [
            30000,
            40000,
            None,
            60000,
        ],
        "target": [0, 1, 0, 1],
    })

    X, _ = separate_features_target(
        df,
        "target",
    )

    assert X["age"].isna().sum() == 1
    assert X["income"].isna().sum() == 1


# ==========================================
# MISSING TARGET COLUMN
# ==========================================

def test_missing_target_column_raises_error():

    df = pd.DataFrame({
        "age": [20, 30, 40],
        "income": [30000, 40000, 50000],
    })

    with pytest.raises(
        ValueError,
        match="was not found",
    ):
        separate_features_target(
            df,
            "target",
        )


# ==========================================
# ALL TARGET VALUES MISSING
# ==========================================

def test_all_missing_target_rows_raise_error():

    df = pd.DataFrame({
        "age": [20, 30, 40],
        "target": [None, None, None],
    })

    with pytest.raises(
        ValueError,
        match="No usable rows remain",
    ):
        separate_features_target(
            df,
            "target",
        )


# ==========================================
# ONLY TARGET COLUMN
# ==========================================

def test_no_feature_columns_raise_error():

    df = pd.DataFrame({
        "target": [0, 1, 0, 1],
    })

    with pytest.raises(
        ValueError,
        match="No feature columns are available",
    ):
        separate_features_target(
            df,
            "target",
        )


# ==========================================
# ONLY IDENTIFIER FEATURES
# ==========================================

def test_only_identifier_features_raise_error():

    df = pd.DataFrame({
        "customer_id": [101, 102, 103, 104],
        "target": [0, 1, 0, 1],
    })

    with pytest.raises(
        ValueError,
        match="No usable feature columns remain",
    ):
        separate_features_target(
            df,
            "target",
        )


# ==========================================
# TARGET BECOMES CONSTANT AFTER
# REMOVING MISSING TARGET ROWS
# ==========================================

def test_constant_target_after_missing_removal_raises_error():

    df = pd.DataFrame({
        "age": [20, 30, 40, 50],
        "target": [
            "Yes",
            "Yes",
            None,
            None,
        ],
    })

    with pytest.raises(
        ValueError,
        match="at least 2 unique values",
    ):
        separate_features_target(
            df,
            "target",
        )


# ==========================================
# X AND Y INDEX ALIGNMENT
# ==========================================

def test_features_and_target_remain_aligned():

    df = pd.DataFrame(
        {
            "age": [20, 30, 40, 50],
            "target": [0, None, 1, 0],
        },
        index=[10, 20, 30, 40],
    )

    X, y = separate_features_target(
        df,
        "target",
    )

    assert X.index.tolist() == [
        10,
        30,
        40,
    ]

    assert y.index.tolist() == [
        10,
        30,
        40,
    ]

    assert X.index.equals(y.index)