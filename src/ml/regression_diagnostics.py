# ==========================================
# DATALENS AI
# REGRESSION MODEL DIAGNOSTICS V1
# ==========================================

import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def run_regression_diagnostics(
    trained_model,
    X_test,
    y_test
):
    """
    Generate diagnostics for a trained
    regression model.

    Includes:
        residual analysis
        prediction-error analysis
        residual statistics
        error distribution information
    """

    print("\n================================")
    print("REGRESSION DIAGNOSTICS")
    print("================================")

    # ==========================================
    # PREDICTIONS
    # ==========================================

    predictions = (
        trained_model.predict(
            X_test
        )
    )

    actual = np.asarray(
        y_test,
        dtype=float
    )

    predicted = np.asarray(
        predictions,
        dtype=float
    )

    # ==========================================
    # RESIDUALS
    # ==========================================
    #
    # Residual:
    #
    # actual - predicted
    #
    # Positive residual:
    # model predicted too low.
    #
    # Negative residual:
    # model predicted too high.
    # ==========================================

    residuals = (
        actual
        - predicted
    )

    absolute_errors = (
        np.abs(residuals)
    )

    squared_errors = (
        residuals ** 2
    )

    # ==========================================
    # CORE METRICS
    # ==========================================

    mae = mean_absolute_error(
        actual,
        predicted
    )

    mse = mean_squared_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mse
    )

    r2 = r2_score(
        actual,
        predicted
    )

    # ==========================================
    # RESIDUAL STATISTICS
    # ==========================================

    if len(residuals) > 0:

        residual_mean = float(
            np.mean(residuals)
        )

        residual_median = float(
            np.median(residuals)
        )

        residual_std = float(
            np.std(residuals)
        )

        residual_min = float(
            np.min(residuals)
        )

        residual_max = float(
            np.max(residuals)
        )

        residual_q25 = float(
            np.percentile(
                residuals,
                25
            )
        )

        residual_q75 = float(
            np.percentile(
                residuals,
                75
            )
        )

    else:

        residual_mean = 0.0
        residual_median = 0.0
        residual_std = 0.0
        residual_min = 0.0
        residual_max = 0.0
        residual_q25 = 0.0
        residual_q75 = 0.0

    # ==========================================
    # ERROR DIRECTION
    # ==========================================

    under_predictions = int(
        np.sum(
            residuals > 0
        )
    )

    over_predictions = int(
        np.sum(
            residuals < 0
        )
    )

    exact_predictions = int(
        np.sum(
            np.isclose(
                residuals,
                0.0
            )
        )
    )

    # ==========================================
    # LARGEST ERRORS
    # ==========================================

    largest_error_indices = (
        np.argsort(
            absolute_errors
        )[::-1][:10]
    )

    largest_errors = []

    for index in largest_error_indices:

        largest_errors.append(
            {
                "sample_index":
                    int(index),

                "actual":
                    float(
                        actual[index]
                    ),

                "predicted":
                    float(
                        predicted[index]
                    ),

                "residual":
                    float(
                        residuals[index]
                    ),

                "absolute_error":
                    float(
                        absolute_errors[index]
                    )
            }
        )

    # ==========================================
    # PLOT DATA
    # ==========================================
    #
    # The backend returns raw values.
    # The frontend can later create:
    #
    # Actual vs Predicted plot
    # Residual plot
    # Residual histogram
    # ==========================================

    plot_data = {
        "actual": [
            float(value)
            for value in actual
        ],

        "predicted": [
            float(value)
            for value in predicted
        ],

        "residuals": [
            float(value)
            for value in residuals
        ],

        "absolute_errors": [
            float(value)
            for value in absolute_errors
        ]
    }

    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    results = {
        "diagnostic_type":
            "regression",

        "sample_count":
            int(len(actual)),

        "metrics": {
            "mae":
                float(mae),

            "mse":
                float(mse),

            "rmse":
                float(rmse),

            "r2":
                float(r2)
        },

        "residual_statistics": {
            "mean":
                residual_mean,

            "median":
                residual_median,

            "standard_deviation":
                residual_std,

            "minimum":
                residual_min,

            "maximum":
                residual_max,

            "q25":
                residual_q25,

            "q75":
                residual_q75
        },

        "prediction_direction": {
            "under_predictions":
                under_predictions,

            "over_predictions":
                over_predictions,

            "exact_predictions":
                exact_predictions
        },

        "largest_errors":
            largest_errors,

        "plot_data":
            plot_data
    }

    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print(
        f"Samples: {len(actual)}"
    )

    print(
        f"MAE:  {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"R²:   {r2:.4f}"
    )

    print(
        f"Mean Residual: "
        f"{residual_mean:.4f}"
    )

    print(
        f"Residual Std: "
        f"{residual_std:.4f}"
    )

    print(
        f"Under-Predictions: "
        f"{under_predictions}"
    )

    print(
        f"Over-Predictions: "
        f"{over_predictions}"
    )

    print(
        "✓ Regression diagnostics complete."
    )

    return results