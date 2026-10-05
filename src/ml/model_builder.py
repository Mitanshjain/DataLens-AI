# ==========================================
# DATALENS AI - ML MODEL BUILDER
# ==========================================

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


def build_classification_model(
    preprocessor
):

    """
    Build a complete classification pipeline
    containing preprocessing and the model.
    """

    print("\n================================")
    print("BUILDING CLASSIFICATION MODEL")
    print("================================")


    # ------------------------------------------
    # CREATE CLASSIFIER
    # ------------------------------------------

    classifier = LogisticRegression(
        max_iter=1000
    )


    # ------------------------------------------
    # CREATE COMPLETE ML PIPELINE
    # ------------------------------------------

    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                classifier
            )
        ]
    )


    print(
        "✓ Logistic Regression created."
    )

    print(
        "✓ Preprocessing connected to model."
    )

    print(
        "✓ Classification pipeline created."
    )


    return model_pipeline