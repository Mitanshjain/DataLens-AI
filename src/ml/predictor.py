# ==========================================
# DATALENS AI - MODEL PREDICTOR
# ==========================================


def make_predictions(
    trained_model,
    X_test
):

    """
    Generate predictions using
    the trained ML pipeline.
    """

    print("\n================================")
    print("MODEL PREDICTION")
    print("================================")


    # ------------------------------------------
    # MAKE PREDICTIONS
    # ------------------------------------------

    predictions = trained_model.predict(
        X_test
    )


    print(
        "✓ Predictions generated successfully."
    )


    # ------------------------------------------
    # DISPLAY PREDICTIONS
    # ------------------------------------------

    print(
        f"Predictions: "
        f"{predictions.tolist()}"
    )


    return predictions