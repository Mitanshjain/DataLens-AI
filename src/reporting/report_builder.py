# ==========================================
# DATALENS AI - REPORT BUILDER V3
# ==========================================

from datetime import datetime

import numpy as np
import pandas as pd


# ==========================================
# CLEAN DISPLAY LABEL
# ==========================================

def clean_display_value(value):
    """
    Prepare values for report presentation.

    This does NOT modify the original dataset.

    Missing index labels are represented as
    'Missing' only in the presentation layer.
    """

    if pd.isna(value):
        return "Missing"

    return value


# ==========================================
# DATAFRAME TO REPORT RECORDS
# ==========================================

def dataframe_to_report_records(df):
    """
    Convert a Pandas DataFrame into report-safe
    records while preserving meaningful indexes.
    """

    report_df = df.copy()

    if not isinstance(
        report_df.index,
        pd.RangeIndex
    ):

        index_name = (
            report_df.index.name
            or "group"
        )

        report_df = (
            report_df
            .reset_index()
        )

        first_column = (
            report_df.columns[0]
        )

        if first_column == "index":

            report_df = (
                report_df.rename(
                    columns={
                        "index": index_name
                    }
                )
            )

    report_df = report_df.map(
        clean_display_value
    )

    return report_df.to_dict(
        orient="records"
    )


# ==========================================
# REPORT-SAFE CONVERTER
# ==========================================

def make_report_safe(value):
    """
    Convert Python, NumPy and Pandas objects
    into report-safe structures.

    Trained model objects and unnecessary raw
    prediction arrays are excluded from the
    presentation report.
    """

    if value is None:
        return None

    if isinstance(
        value,
        (str, int, float, bool)
    ):
        return value

    if isinstance(
        value,
        np.generic
    ):
        return value.item()

    if isinstance(
        value,
        np.ndarray
    ):
        return [
            make_report_safe(item)
            for item in value.tolist()
        ]

    if isinstance(
        value,
        pd.DataFrame
    ):
        return dataframe_to_report_records(
            value
        )

    if isinstance(
        value,
        pd.Series
    ):

        safe_series = {}

        for key, item in value.items():

            safe_key = (
                "Missing"
                if pd.isna(key)
                else str(key)
            )

            safe_series[
                safe_key
            ] = make_report_safe(
                item
            )

        return safe_series

    if isinstance(
        value,
        dict
    ):

        safe_dictionary = {}

        for key, item in value.items():

            if key in {
                "base_model",
                "trained_models",
                "imbalance_models"
            }:
                continue

            if key == "predictions":
                continue

            safe_key = (
                "Missing"
                if pd.isna(key)
                else str(key)
            )

            safe_dictionary[
                safe_key
            ] = make_report_safe(
                item
            )

        return safe_dictionary

    if isinstance(
        value,
        (list, tuple, set)
    ):
        return [
            make_report_safe(item)
            for item in value
        ]

    return str(value)


# ==========================================
# DATASET OVERVIEW
# ==========================================

def build_dataset_overview(
    df,
    target_column,
    problem_type
):
    """
    Build the dataset overview used in the
    final report.
    """

    return {

        "total_records":
            int(len(df)),

        "total_columns":
            int(len(df.columns)),

        "target_column":
            target_column,

        "problem_type":
            problem_type,

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            ),

        "columns":
            df.columns.tolist()
    }


# ==========================================
# BUILD FINAL REPORT DATA
# ==========================================

def build_report_data(
    df,
    target_column,
    problem_type,
    ml_results,
    business_results,
    decision_results,
    ai_results
):
    """
    Combine DataLens AI results into one
    structured presentation object.

    This function prepares report content.

    It does not generate HTML or PDF.
    """

    print("\n================================")
    print("BUILDING REPORT DATA V3")
    print("================================")

    dataset_overview = (
        build_dataset_overview(
            df=df,
            target_column=target_column,
            problem_type=problem_type
        )
    )

    safe_ml_results = (
        make_report_safe(
            ml_results
        )
    )

    safe_business_results = (
        make_report_safe(
            business_results
        )
    )

    safe_decision_results = (
        make_report_safe(
            decision_results
        )
    )

    safe_ai_results = (
        make_report_safe(
            ai_results
        )
    )

    report_metadata = {

        "report_title":
            "DataLens AI Analysis Report",

        "generated_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "report_version":
            "3.0",

        "generated_by":
            "DataLens AI"
    }

    report_data = {

        "metadata":
            report_metadata,

        "dataset_overview":
            dataset_overview,

        "machine_learning":
            safe_ml_results,

        "business_analytics":
            safe_business_results,

        "decision_insights":
            safe_decision_results,

        "ai_analyst":
            safe_ai_results
    }

    print("✓ Report metadata prepared.")
    print("✓ Dataset overview prepared.")
    print("✓ Machine Learning results added.")
    print("✓ Raw predictions excluded.")
    print("✓ Segment labels preserved.")
    print("✓ Missing display labels normalized.")
    print("✓ Business Analytics results added.")
    print("✓ Decision / Insight Engine results added.")
    print("✓ AI Analyst results added.")
    print("✓ Report data structure created.")

    return report_data
