# ==========================================
# DATALENS AI - TRAIN TEST SPLITTER
# ==========================================

import pandas as pd

from sklearn.model_selection import train_test_split


def split_dataset(
    X: pd.DataFrame,
    y: pd.Series
):

    """
    Split features and target into
    training and testing datasets.
    """

    print("\n================================")
    print("TRAIN TEST SPLIT")
    print("================================")


    # ------------------------------------------
    # SPLIT DATASET
    # ------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )


    # ------------------------------------------
    # DISPLAY SPLIT INFORMATION
    # ------------------------------------------

    print(
        f"Total Records: {len(X)}"
    )

    print(
        f"Training Records: {len(X_train)}"
    )

    print(
        f"Testing Records: {len(X_test)}"
    )

    print(
        f"X_train Shape: {X_train.shape}"
    )

    print(
        f"X_test Shape: {X_test.shape}"
    )

    print(
        f"y_train Shape: {y_train.shape}"
    )

    print(
        f"y_test Shape: {y_test.shape}"
    )


    return (
        X_train,
        X_test,
        y_train,
        y_test
    )