# ==========================================
# DATALENS AI - SEGMENT ANALYSIS ENGINE V1
# ==========================================

import pandas as pd
import numpy as np


def analyze_segments(
    df,
    target_column=None,
    max_categories=20
):
    """
    Analyze important business segments.

    For categorical columns:
        - Record count
        - Record percentage

    If target is numerical:
        - Target mean
        - Target median
        - Target min/max

    If target is categorical:
        - Target distribution within
          each segment

    High-cardinality columns such as IDs
    are skipped.
    """

    print("\n================================")
    print("BUSINESS SEGMENT ANALYSIS")
    print("================================")


    # ==========================================
    # DETECT CATEGORICAL COLUMNS
    # ==========================================

    categorical_columns = (
        df.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        )
        .columns
        .tolist()
    )


    # Target should not analyze itself
    # as a segment.

    if target_column in categorical_columns:

        categorical_columns.remove(
            target_column
        )


    segment_results = {}


    # ==========================================
    # ANALYZE EACH SEGMENT
    # ==========================================

    for column in categorical_columns:

        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )


        # --------------------------------------
        # SKIP HIGH-CARDINALITY COLUMNS
        # --------------------------------------

        if unique_count > max_categories:

            print(
                f"\nSkipping {column}: "
                f"{unique_count} categories "
                f"(high cardinality)"
            )

            continue


        print(
            f"\nSegment: {column}"
        )


        # ======================================
        # BASIC SEGMENT DISTRIBUTION
        # ======================================

        counts = (
            df[column]
            .value_counts(
                dropna=False
            )
        )


        percentages = (
            df[column]
            .value_counts(
                dropna=False,
                normalize=True
            )
            .mul(100)
        )


        segment_summary = pd.DataFrame(
            {
                "Count":
                    counts,

                "Percentage":
                    percentages
            }
        )


        segment_summary[
            "Percentage"
        ] = (
            segment_summary[
                "Percentage"
            ].round(2)
        )


        # ======================================
        # TARGET ANALYSIS
        # ======================================

        target_analysis = None


        if (
            target_column is not None
            and target_column in df.columns
        ):

            target_series = (
                df[target_column]
            )


            # ----------------------------------
            # NUMERICAL TARGET
            # ----------------------------------

            if pd.api.types.is_numeric_dtype(
                target_series
            ):

                target_analysis = (
                    df.groupby(
                        column,
                        dropna=False
                    )[target_column]
                    .agg(
                        [
                            "count",
                            "mean",
                            "median",
                            "min",
                            "max"
                        ]
                    )
                    .round(2)
                    .sort_values(
                        by="mean",
                        ascending=False
                    )
                )


                print(
                    f"\n{target_column} "
                    f"by {column}:"
                )

                print(
                    target_analysis
                    .to_string()
                )


            # ----------------------------------
            # CATEGORICAL TARGET
            # ----------------------------------

            else:

                target_analysis = (
                    pd.crosstab(
                        df[column],
                        df[target_column],
                        normalize="index",
                        dropna=False
                    )
                    .mul(100)
                    .round(2)
                )


                print(
                    f"\n{target_column} "
                    f"distribution by {column} (%):"
                )

                print(
                    target_analysis
                    .to_string()
                )


        # ======================================
        # STORE RESULT
        # ======================================

        segment_results[
            column
        ] = {

            "distribution":
                segment_summary,

            "target_analysis":
                target_analysis
        }


    # ==========================================
    # NO SEGMENTS FOUND
    # ==========================================

    if not segment_results:

        print(
            "\n⚠ No suitable categorical "
            "segments found."
        )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    return segment_results