# ==========================================
# DATALENS AI - DATASET VALIDATOR
# ==========================================

import pandas as pd


def validate_dataset(df: pd.DataFrame):

    """
    Perform basic validation checks
    before profiling the dataset.
    """

    print("\n================================")
    print("DATASET VALIDATION")
    print("================================")

    # ------------------------------------------
    # CHECK 1: Dataset exists
    # ------------------------------------------

    if df is None:
        print("❌ Dataset does not exist.")
        return False


    # ------------------------------------------
    # CHECK 2: Dataset is empty
    # ------------------------------------------

    if df.empty:
        print("❌ Dataset is empty.")
        return False

    print("✓ Dataset is not empty.")


    # ------------------------------------------
    # CHECK 3: Dataset has columns
    # ------------------------------------------

    if len(df.columns) == 0:
        print("❌ Dataset contains no columns.")
        return False

    print(f"✓ Dataset contains {len(df.columns)} columns.")


    # ------------------------------------------
    # CHECK 4: Duplicate column names
    # ------------------------------------------

    duplicate_columns = df.columns[df.columns.duplicated()].tolist()

    if duplicate_columns:
        print(f"⚠ Duplicate columns found: {duplicate_columns}")
    else:
        print("✓ No duplicate column names.")


    # ------------------------------------------
    # CHECK 5: Completely empty columns
    # ------------------------------------------

    empty_columns = df.columns[df.isna().all()].tolist()

    if empty_columns:
        print(f"⚠ Completely empty columns: {empty_columns}")
    else:
        print("✓ No completely empty columns.")


    print("\n✓ Basic dataset validation completed.")

    return True