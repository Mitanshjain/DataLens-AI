# ==========================================
# DATALENS AI - EDA VISUALIZATIONS
# ==========================================

import os

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def generate_numerical_histograms(df: pd.DataFrame):

    """
    Generate histogram plots for
    numerical features.
    """

    print("\n================================")
    print("GENERATING EDA VISUALIZATIONS")
    print("================================")


    # ------------------------------------------
    # CREATE REPORT FOLDER
    # ------------------------------------------

    output_folder = "reports/eda"

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # ------------------------------------------
    # SELECT NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    for column in numerical_columns:

        column_name = column.lower()


        # --------------------------------------
        # SKIP IDENTIFIER COLUMNS
        # --------------------------------------

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue


        # --------------------------------------
        # REMOVE MISSING VALUES
        # --------------------------------------

        data = df[column].dropna()

        if data.empty:
            continue


        # --------------------------------------
        # CREATE HISTOGRAM
        # --------------------------------------

        plt.figure(figsize=(8, 5))

        plt.hist(
            data,
            bins=10,
            edgecolor="black"
        )

        plt.title(
            f"Distribution of {column}"
        )

        plt.xlabel(column)

        plt.ylabel("Frequency")

        plt.tight_layout()


        # --------------------------------------
        # SAVE IMAGE
        # --------------------------------------

        file_path = os.path.join(
            output_folder,
            f"{column}_histogram.png"
        )

        plt.savefig(file_path)

        plt.close()


        print(
            f"✓ Created: {file_path}"
        )

def generate_correlation_heatmap(df: pd.DataFrame):

    """
    Generate a correlation heatmap
    for numerical features.
    """

    print("\n================================")
    print("GENERATING CORRELATION HEATMAP")
    print("================================")


    output_folder = "reports/eda"

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # ------------------------------------------
    # SELECT NUMERICAL COLUMNS
    # ------------------------------------------

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()


    # ------------------------------------------
    # REMOVE IDENTIFIER COLUMNS
    # ------------------------------------------

    analysis_columns = []

    for column in numerical_columns:

        column_name = column.lower()

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.startswith("id_")
        ):
            continue

        analysis_columns.append(column)


    # ------------------------------------------
    # NEED AT LEAST TWO FEATURES
    # ------------------------------------------

    if len(analysis_columns) < 2:

        print(
            "Not enough numerical features "
            "for correlation heatmap."
        )

        return


    # ------------------------------------------
    # CREATE CORRELATION MATRIX
    # ------------------------------------------

    correlation_matrix = df[
        analysis_columns
    ].corr()


    # ------------------------------------------
    # CREATE HEATMAP
    # ------------------------------------------

    plt.figure(
        figsize=(8, 6)
    )

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f"
    )

    plt.title(
        "Feature Correlation Heatmap"
    )

    plt.tight_layout()


    # ------------------------------------------
    # SAVE HEATMAP
    # ------------------------------------------

    file_path = os.path.join(
        output_folder,
        "correlation_heatmap.png"
    )

    plt.savefig(file_path)

    plt.close()


    print(
        f"✓ Created: {file_path}"
    )