# ==========================================
# DATALENS AI - REGRESSION ENGINE V2
# ==========================================

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import (
    KFold,
    cross_validate
)

from src.ml.regression_diagnostics import (
    run_regression_diagnostics
)


def run_regression_engine(
    preprocessor,
    X_train,
    X_test,
    y_train,
    y_test,
    X,
    y,
    n_splits=5
):

    """
    Train, evaluate, diagnose and cross-validate
    multiple regression models.

    Returns:
        results_df
        cv_results_df
        trained_models
        diagnostics_results
    """

    print("\n================================")
    print("REGRESSION ENGINE")
    print("================================")


    # ==========================================
    # DEFINE REGRESSION MODELS
    # ==========================================

    models = {

        "Linear Regression":
            LinearRegression(),

        "Decision Tree Regressor":
            DecisionTreeRegressor(
                random_state=42
            ),

        "Random Forest Regressor":
            RandomForestRegressor(
                n_estimators=100,
                random_state=42
            ),

        "K-Nearest Neighbors Regressor":
            KNeighborsRegressor(
                n_neighbors=5
            )
    }


    # ==========================================
    # STORAGE
    # ==========================================

    results = []

    cv_results = []

    trained_models = {}

    diagnostics_results = {}


    # ==========================================
    # CROSS-VALIDATION STRATEGY
    # ==========================================

    cv = KFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=42
    )


    # ==========================================
    # TRAIN EACH MODEL
    # ==========================================

    for model_name, model in models.items():

        print(
            f"\nTraining: {model_name}"
        )


        # --------------------------------------
        # BUILD PIPELINE
        # --------------------------------------

        model_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    clone(preprocessor)
                ),
                (
                    "model",
                    model
                )
            ]
        )


        # --------------------------------------
        # TRAIN MODEL
        # --------------------------------------

        model_pipeline.fit(
            X_train,
            y_train
        )


        # --------------------------------------
        # TEST PREDICTIONS
        # --------------------------------------

        predictions = model_pipeline.predict(
            X_test
        )


        # --------------------------------------
        # REGRESSION METRICS
        # --------------------------------------

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        mse = mean_squared_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mse
        )

        r2 = r2_score(
            y_test,
            predictions
        )


        # --------------------------------------
        # STORE TEST RESULTS
        # --------------------------------------

        results.append(
            {
                "Model":
                    model_name,

                "MAE":
                    mae,

                "MSE":
                    mse,

                "RMSE":
                    rmse,

                "R2 Score":
                    r2
            }
        )


        # --------------------------------------
        # STORE TRAINED MODEL
        # --------------------------------------

        trained_models[
            model_name
        ] = model_pipeline


        print(
            f"✓ {model_name} trained and evaluated."
        )


        # ======================================
        # MODEL DIAGNOSTICS
        # ======================================

        diagnostics_results[
            model_name
        ] = run_regression_diagnostics(
            model_pipeline,
            X_test,
            y_test
        )


        # ======================================
        # CROSS-VALIDATION
        # ======================================

        print(
            f"  Cross-validating: {model_name}"
        )


        cv_pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    clone(preprocessor)
                ),
                (
                    "model",
                    clone(model)
                )
            ]
        )


        scores = cross_validate(
            cv_pipeline,
            X,
            y,
            cv=cv,
            scoring={
                "mae":
                    "neg_mean_absolute_error",

                "mse":
                    "neg_mean_squared_error",

                "r2":
                    "r2"
            },
            n_jobs=-1
        )


        cv_mae = (
            -scores["test_mae"]
        )

        cv_mse = (
            -scores["test_mse"]
        )

        cv_rmse = np.sqrt(
            cv_mse
        )

        cv_r2 = (
            scores["test_r2"]
        )


        # --------------------------------------
        # STORE CROSS-VALIDATION RESULTS
        # --------------------------------------

        cv_results.append(
            {
                "Model":
                    model_name,

                "CV MAE":
                    cv_mae.mean(),

                "CV RMSE":
                    cv_rmse.mean(),

                "CV R2":
                    cv_r2.mean(),

                "MAE Std":
                    cv_mae.std(),

                "RMSE Std":
                    cv_rmse.std(),

                "R2 Std":
                    cv_r2.std()
            }
        )


        print(
            f"✓ {model_name} completed "
            f"{n_splits}-fold cross-validation."
        )


    # ==========================================
    # CREATE RESULT DATAFRAMES
    # ==========================================

    results_df = pd.DataFrame(
        results
    )

    cv_results_df = pd.DataFrame(
        cv_results
    )


    # ==========================================
    # SORT FOR INSPECTION
    # ==========================================
    #
    # Lower RMSE = smaller prediction error.
    #
    # Sorting is used only for inspection.
    # It does NOT permanently declare a
    # production model.
    # ==========================================

    results_df = (
        results_df
        .sort_values(
            by="RMSE"
        )
        .reset_index(
            drop=True
        )
    )


    cv_results_df = (
        cv_results_df
        .sort_values(
            by="CV RMSE"
        )
        .reset_index(
            drop=True
        )
    )


    # ==========================================
    # DISPLAY TEST RESULTS
    # ==========================================

    print("\n================================")
    print("REGRESSION MODEL COMPARISON")
    print("================================")


    display_results = (
        results_df.copy()
    )


    numeric_columns = [
        "MAE",
        "MSE",
        "RMSE",
        "R2 Score"
    ]


    display_results[
        numeric_columns
    ] = (
        display_results[
            numeric_columns
        ].round(4)
    )


    print(
        display_results.to_string(
            index=False
        )
    )


    # ==========================================
    # DISPLAY CV RESULTS
    # ==========================================

    print("\n================================")
    print("REGRESSION CROSS-VALIDATION")
    print("================================")


    display_cv = (
        cv_results_df.copy()
    )


    cv_numeric_columns = [
        "CV MAE",
        "CV RMSE",
        "CV R2",
        "MAE Std",
        "RMSE Std",
        "R2 Std"
    ]


    display_cv[
        cv_numeric_columns
    ] = (
        display_cv[
            cv_numeric_columns
        ].round(4)
    )


    print(
        display_cv.to_string(
            index=False
        )
    )


    # ==========================================
    # DIAGNOSTICS SUMMARY
    # ==========================================

    print("\n================================")
    print("REGRESSION DIAGNOSTICS SUMMARY")
    print("================================")

    print(
        f"Models Diagnosed: "
        f"{len(diagnostics_results)}"
    )

    print(
        "✓ Regression diagnostics generated "
        "for all trained models."
    )


    # ==========================================
    # RETURN RESULTS
    # ==========================================

    return (
        results_df,
        cv_results_df,
        trained_models,
        diagnostics_results
    )