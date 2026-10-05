# ==========================================
# DATALENS AI - BUSINESS FINDINGS ENGINE V1
# ==========================================

import pandas as pd
import numpy as np


def generate_business_findings(
    df,
    target_column=None,
    max_categories=20
):
    """
    Generate factual business findings
    directly from the dataset.

    This engine does NOT use an LLM.

    It identifies:
        - Dataset-level observations
        - Numerical target findings
        - Categorical target findings
        - Segment-level differences
        - Strong numerical relationships

    All findings are calculated from data.
    """

    print("\n================================")
    print("BUSINESS FINDINGS")
    print("================================")


    findings = []


    # ==========================================
    # DATASET-LEVEL FINDINGS
    # ==========================================

    total_records = len(df)

    missing_values = int(
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = int(
        df.duplicated()
        .sum()
    )


    findings.append(
        f"Dataset contains "
        f"{total_records} records."
    )


    if missing_values > 0:

        findings.append(
            f"Dataset contains "
            f"{missing_values} missing values."
        )

    else:

        findings.append(
            "No missing values were detected."
        )


    if duplicate_rows > 0:

        findings.append(
            f"Dataset contains "
            f"{duplicate_rows} duplicate records."
        )

    else:

        findings.append(
            "No duplicate records were detected."
        )


    # ==========================================
    # TARGET ANALYSIS
    # ==========================================

    if (
        target_column is not None
        and target_column in df.columns
    ):

        target_series = df[
            target_column
        ]


        # ======================================
        # NUMERICAL TARGET
        # ======================================

        if pd.api.types.is_numeric_dtype(
            target_series
        ):

            clean_target = (
                target_series
                .dropna()
            )


            if not clean_target.empty:

                target_mean = (
                    clean_target.mean()
                )

                target_median = (
                    clean_target.median()
                )


                findings.append(
                    f"Average {target_column} "
                    f"is {target_mean:.2f}."
                )

                findings.append(
                    f"Median {target_column} "
                    f"is {target_median:.2f}."
                )


            # ==================================
            # SEGMENT TARGET ANALYSIS
            # ==================================

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


            for column in categorical_columns:

                if column == target_column:
                    continue


                unique_count = (
                    df[column]
                    .nunique(
                        dropna=True
                    )
                )


                if (
                    unique_count < 2
                    or unique_count > max_categories
                ):

                    continue


                segment_means = (
                    df.groupby(
                        column,
                        dropna=False
                    )[target_column]
                    .mean()
                    .dropna()
                    .sort_values(
                        ascending=False
                    )
                )


                if len(segment_means) < 2:
                    continue


                highest_segment = (
                    segment_means.index[0]
                )

                highest_value = float(
                    segment_means.iloc[0]
                )


                lowest_segment = (
                    segment_means.index[-1]
                )

                lowest_value = float(
                    segment_means.iloc[-1]
                )


                findings.append(
                    f"For {column}, "
                    f"'{highest_segment}' has the "
                    f"highest average {target_column} "
                    f"at {highest_value:.2f}, while "
                    f"'{lowest_segment}' has the "
                    f"lowest average at "
                    f"{lowest_value:.2f}."
                )


        # ======================================
        # CATEGORICAL TARGET
        # ======================================

        else:

            distribution = (
                target_series
                .value_counts(
                    normalize=True,
                    dropna=False
                )
                .mul(100)
            )


            for value, percentage in (
                distribution.items()
            ):

                findings.append(
                    f"{target_column} = "
                    f"'{value}' represents "
                    f"{percentage:.2f}% "
                    f"of records."
                )


            # ==================================
            # SEGMENT TARGET DISTRIBUTIONS
            # ==================================

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


            if target_column in categorical_columns:

                categorical_columns.remove(
                    target_column
                )


            for column in categorical_columns:

                unique_count = (
                    df[column]
                    .nunique(
                        dropna=True
                    )
                )


                if (
                    unique_count < 2
                    or unique_count > max_categories
                ):

                    continue


                segment_distribution = (
                    pd.crosstab(
                        df[column],
                        df[target_column],
                        normalize="index",
                        dropna=False
                    )
                    .mul(100)
                    .round(2)
                )


                if segment_distribution.empty:
                    continue


                # Store a compact factual finding
                # for the most represented target
                # class within each segment.

                for segment_name, row in (
                    segment_distribution.iterrows()
                ):

                    if row.empty:
                        continue


                    top_class = (
                        row.idxmax()
                    )

                    top_percentage = float(
                        row.max()
                    )


                    findings.append(
                        f"In {column} = "
                        f"'{segment_name}', "
                        f"the most common "
                        f"{target_column} class is "
                        f"'{top_class}' at "
                        f"{top_percentage:.2f}%."
                    )


    # ==========================================
    # NUMERICAL RELATIONSHIPS
    # ==========================================

    numerical_df = (
        df.select_dtypes(
            include=np.number
        )
        .copy()
    )


    # Remove obvious identifier columns.

    identifier_columns = []

    for column in numerical_df.columns:

        column_lower = (
            column.lower()
        )

        if (
            column_lower == "id"
            or column_lower.endswith("_id")
            or column_lower.startswith("id_")
        ):

            identifier_columns.append(
                column
            )


    numerical_df = (
        numerical_df.drop(
            columns=identifier_columns,
            errors="ignore"
        )
    )


    if numerical_df.shape[1] >= 2:

        correlation_matrix = (
            numerical_df.corr()
        )


        processed_pairs = set()


        for column_a in correlation_matrix.columns:

            for column_b in correlation_matrix.columns:

                if column_a == column_b:
                    continue


                pair = tuple(
                    sorted(
                        [
                            column_a,
                            column_b
                        ]
                    )
                )


                if pair in processed_pairs:
                    continue


                processed_pairs.add(
                    pair
                )


                correlation = (
                    correlation_matrix.loc[
                        column_a,
                        column_b
                    ]
                )


                if pd.isna(correlation):
                    continue


                # Only report strong linear
                # relationships in V1.

                if abs(correlation) >= 0.70:

                    direction = (
                        "positive"
                        if correlation > 0
                        else "negative"
                    )


                    findings.append(
                        f"{column_a} and "
                        f"{column_b} show a strong "
                        f"{direction} correlation "
                        f"({correlation:.2f})."
                    )


    # ==========================================
    # PRINT FINDINGS
    # ==========================================

    if findings:

        for index, finding in enumerate(
            findings,
            start=1
        ):

            print(
                f"{index}. {finding}"
            )

    else:

        print(
            "No significant business findings "
            "were generated."
        )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    return {
        "total_findings":
            len(findings),

        "findings":
            findings
    }