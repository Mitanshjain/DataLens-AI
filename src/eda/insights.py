# ==========================================
# DATALENS AI - AUTOMATIC EDA INSIGHTS
# ==========================================

import pandas as pd


def generate_eda_insights(df: pd.DataFrame):

    """
    Generate automatic observations
    from EDA statistics.
    """

    print("\n================================")
    print("AUTOMATIC EDA INSIGHTS")
    print("================================")


    insights_found = False


    # ------------------------------------------
    # SELECT NUMERICAL FEATURES
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    analysis_columns = []


    for column in numerical_columns:

        column_name = column.lower()

        # Skip identifier columns
        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue

        analysis_columns.append(column)


    # ------------------------------------------
    # INSIGHT 1: SKEWNESS
    # ------------------------------------------

    for column in analysis_columns:

        series = df[column].dropna()

        if len(series) < 3:
            continue


        skewness = series.skew()


        if skewness > 1:

            print(
                f"⚠ {column} is strongly "
                f"right-skewed "
                f"(skewness: {skewness:.2f})."
            )

            insights_found = True


        elif skewness < -1:

            print(
                f"⚠ {column} is strongly "
                f"left-skewed "
                f"(skewness: {skewness:.2f})."
            )

            insights_found = True


    # ------------------------------------------
    # INSIGHT 2: STRONG CORRELATIONS
    # ------------------------------------------

    if len(analysis_columns) >= 2:

        correlation_matrix = df[
            analysis_columns
        ].corr()


        for i in range(len(analysis_columns)):

            for j in range(i + 1, len(analysis_columns)):

                column_1 = analysis_columns[i]

                column_2 = analysis_columns[j]

                correlation = correlation_matrix.loc[
                    column_1,
                    column_2
                ]


                if pd.isna(correlation):
                    continue


                if abs(correlation) >= 0.8:

                    direction = (
                        "positive"
                        if correlation > 0
                        else "negative"
                    )

                    print(
                        f"⚠ {column_1} and {column_2} "
                        f"have a strong {direction} "
                        f"correlation "
                        f"({correlation:.2f})."
                    )

                    insights_found = True


    # ------------------------------------------
    # NO INSIGHTS
    # ------------------------------------------

    if not insights_found:

        print(
            "✓ No major EDA patterns "
            "detected."
        )