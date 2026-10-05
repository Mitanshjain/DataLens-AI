# ==========================================
# DATALENS AI - KPI ENGINE V1
# ==========================================

import pandas as pd
import numpy as np


def generate_kpi_summary(
    df,
    target_column=None
):
    """
    Generate general business-level KPIs
    from the uploaded dataset.

    This module only calculates factual
    metrics from the data.

    It does NOT generate AI interpretations.
    """

    print("\n================================")
    print("BUSINESS KPI SUMMARY")
    print("================================")


    # ==========================================
    # BASIC DATASET KPIs
    # ==========================================

    total_rows = len(df)

    total_columns = len(
        df.columns
    )

    missing_values = int(
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = int(
        df.duplicated()
        .sum()
    )


    print(
        f"Total Records: {total_rows}"
    )

    print(
        f"Total Features: {total_columns}"
    )

    print(
        f"Missing Values: {missing_values}"
    )

    print(
        f"Duplicate Records: {duplicate_rows}"
    )


    # ==========================================
    # NUMERICAL KPIs
    # ==========================================

    numerical_columns = (
        df.select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )


    numerical_kpis = {}


    print("\nNumerical KPIs:")


    for column in numerical_columns:

        # Skip obvious ID columns

        column_lower = (
            column.lower()
        )

        if (
            column_lower == "id"
            or column_lower.endswith("_id")
            or column_lower.startswith("id_")
        ):
            continue


        series = (
            df[column]
            .dropna()
        )


        if series.empty:
            continue


        column_kpis = {

            "mean":
                float(series.mean()),

            "median":
                float(series.median()),

            "minimum":
                float(series.min()),

            "maximum":
                float(series.max()),

            "sum":
                float(series.sum())
        }


        numerical_kpis[
            column
        ] = column_kpis


        print(
            f"\n{column}:"
        )

        print(
            f"  Average: "
            f"{column_kpis['mean']:.2f}"
        )

        print(
            f"  Median: "
            f"{column_kpis['median']:.2f}"
        )

        print(
            f"  Minimum: "
            f"{column_kpis['minimum']:.2f}"
        )

        print(
            f"  Maximum: "
            f"{column_kpis['maximum']:.2f}"
        )


    # ==========================================
    # CATEGORICAL KPIs
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


    categorical_kpis = {}


    print("\nCategorical KPIs:")


    for column in categorical_columns:

        value_counts = (
            df[column]
            .value_counts(
                dropna=False
            )
        )


        if value_counts.empty:
            continue


        top_value = (
            value_counts.index[0]
        )

        top_count = int(
            value_counts.iloc[0]
        )

        top_percentage = (
            top_count
            / total_rows
            * 100
        )


        categorical_kpis[
            column
        ] = {

            "unique_values":
                int(
                    df[column]
                    .nunique(
                        dropna=True
                    )
                ),

            "top_value":
                str(top_value),

            "top_count":
                top_count,

            "top_percentage":
                float(top_percentage)
        }


        print(
            f"\n{column}:"
        )

        print(
            f"  Unique Values: "
            f"{categorical_kpis[column]['unique_values']}"
        )

        print(
            f"  Most Common: "
            f"{top_value}"
        )

        print(
            f"  Share: "
            f"{top_percentage:.2f}%"
        )


    # ==========================================
    # TARGET KPI
    # ==========================================

    target_kpi = None


    if (
        target_column is not None
        and target_column in df.columns
    ):

        print(
            "\nTarget KPI:"
        )

        target_series = (
            df[target_column]
        )


        # --------------------------------------
        # NUMERICAL TARGET
        # --------------------------------------

        if pd.api.types.is_numeric_dtype(
            target_series
        ):

            clean_target = (
                target_series
                .dropna()
            )


            if not clean_target.empty:

                target_kpi = {

                    "type":
                        "numerical",

                    "mean":
                        float(
                            clean_target.mean()
                        ),

                    "median":
                        float(
                            clean_target.median()
                        ),

                    "minimum":
                        float(
                            clean_target.min()
                        ),

                    "maximum":
                        float(
                            clean_target.max()
                        )
                }


                print(
                    f"  Target: "
                    f"{target_column}"
                )

                print(
                    f"  Average: "
                    f"{target_kpi['mean']:.2f}"
                )

                print(
                    f"  Median: "
                    f"{target_kpi['median']:.2f}"
                )


        # --------------------------------------
        # CATEGORICAL TARGET
        # --------------------------------------

        else:

            target_distribution = (
                target_series
                .value_counts(
                    dropna=False,
                    normalize=True
                )
                .mul(100)
                .round(2)
                .to_dict()
            )


            target_kpi = {

                "type":
                    "categorical",

                "distribution":
                    {
                        str(key):
                            float(value)

                        for key, value
                        in target_distribution.items()
                    }
            }


            print(
                f"  Target: "
                f"{target_column}"
            )

            print(
                "  Distribution:"
            )


            for (
                target_value,
                percentage
            ) in (
                target_kpi[
                    "distribution"
                ].items()
            ):

                print(
                    f"    {target_value}: "
                    f"{percentage:.2f}%"
                )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    return {

        "dataset_kpis": {

            "total_records":
                total_rows,

            "total_columns":
                total_columns,

            "missing_values":
                missing_values,

            "duplicate_rows":
                duplicate_rows
        },

        "numerical_kpis":
            numerical_kpis,

        "categorical_kpis":
            categorical_kpis,

        "target_kpi":
            target_kpi
    }