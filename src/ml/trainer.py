# ==========================================
# DATALENS AI - MODEL TRAINER
# ==========================================


def train_model(
    model_pipeline,
    X_train,
    y_train
):

    """
    Train the complete ML pipeline
    using the training dataset.
    """

    print("\n================================")
    print("MODEL TRAINING")
    print("================================")


    # ------------------------------------------
    # TRAIN MODEL
    # ------------------------------------------

    model_pipeline.fit(
        X_train,
        y_train
    )


    print(
        "✓ Preprocessing fitted on training data."
    )

    print(
        "✓ Logistic Regression trained successfully."
    )


    return model_pipeline