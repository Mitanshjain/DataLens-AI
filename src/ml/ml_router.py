# ==========================================
# DATALENS AI - DYNAMIC ML ROUTER V2
# ==========================================

from src.ml.model_builder import (
    build_classification_model
)

from src.ml.trainer import (
    train_model
)

from src.ml.predictor import (
    make_predictions
)

from src.ml.evaluator import (
    evaluate_classification_model
)

from src.ml.class_performance import (
    analyze_class_performance
)

from src.ml.model_comparison import (
    compare_classification_models
)

from src.ml.cross_validator import (
    cross_validate_classification_models
)

from src.ml.imbalance_handler import (
    compare_imbalance_strategies
)

from src.ml.regression_engine import (
    run_regression_engine
)

from src.ml.explainability import (
    explain_model
)

from src.ml.classification_diagnostics import (
    run_classification_diagnostics
)


def run_ml_engine(
    problem_type,
    preprocessor,
    X,
    y,
    X_train,
    X_test,
    y_train,
    y_test,
    positive_class=None
):

    """
    Dynamically route the dataset to the
    correct Machine Learning workflow.

    Supported:
        Classification
        Regression
    """

    print("\n================================")
    print("DYNAMIC ML ENGINE")
    print("================================")

    print(
        f"Detected Problem Type: "
        f"{problem_type}"
    )


    # ==========================================
    # CLASSIFICATION
    # ==========================================

    if problem_type == "Classification":

        print(
            "✓ Starting classification workflow."
        )


        # ======================================
        # BUILD BASE MODEL
        # ======================================

        model_pipeline = (
            build_classification_model(
                preprocessor
            )
        )


        # ======================================
        # TRAIN BASE MODEL
        # ======================================

        trained_model = train_model(
            model_pipeline,
            X_train,
            y_train
        )


        # ======================================
        # PREDICT
        # ======================================

        predictions = make_predictions(
            trained_model,
            X_test
        )


        # ======================================
        # CLASS LABELS
        # ======================================

        class_labels = (
            trained_model
            .named_steps["model"]
            .classes_
        )


        # ======================================
        # GENERAL EVALUATION
        # ======================================

        evaluation_results = (
            evaluate_classification_model(
                y_test,
                predictions,
                class_labels
            )
        )


        # ======================================
        # CLASSIFICATION DIAGNOSTICS
        # ======================================

        classification_diagnostics = (
            run_classification_diagnostics(
                trained_model,
                X_test,
                y_test,
                positive_class=
                    positive_class
            )
        )


        # ======================================
        # POSITIVE CLASS ANALYSIS
        # ======================================

        class_performance_results = None

        imbalance_results = None

        imbalance_models = None


        if (
            len(class_labels) == 2
            and positive_class is not None
        ):

            class_performance_results = (
                analyze_class_performance(
                    y_test,
                    predictions,
                    positive_class
                )
            )


            (
                imbalance_results,
                imbalance_models

            ) = compare_imbalance_strategies(

                preprocessor,

                X_train,
                X_test,

                y_train,
                y_test,

                positive_class
            )


        # ======================================
        # MODEL COMPARISON
        # ======================================

        (
            comparison_results,
            trained_models

        ) = compare_classification_models(

            preprocessor,

            X_train,
            X_test,

            y_train,
            y_test
        )


        # ======================================
        # CROSS-VALIDATION
        # ======================================

        cv_results = (
            cross_validate_classification_models(
                preprocessor,
                X,
                y,
                n_splits=5
            )
        )


        # ======================================
        # EXPLAINABILITY V2
        # ======================================
        #
        # X_test is supplied so DataLens can
        # explain an actual test observation.
        #
        # The first test observation is used
        # for local explanation in V2.
        # ======================================

        explanation_results = (
            explain_model(
                trained_model,
                X_explain=X_test,
                top_n=10
            )
        )


        # ======================================
        # STRUCTURED OUTPUT
        # ======================================

        return {

            "problem_type":
                "Classification",

            "base_model":
                trained_model,

            "predictions":
                predictions,

            "evaluation":
                evaluation_results,

            "diagnostics":
                classification_diagnostics,

            "class_performance":
                class_performance_results,

            "model_comparison":
                comparison_results,

            "cross_validation":
                cv_results,

            "imbalance_results":
                imbalance_results,

            "trained_models":
                trained_models,

            "imbalance_models":
                imbalance_models,

            "explainability":
                explanation_results
        }


    # ==========================================
    # REGRESSION
    # ==========================================

    elif problem_type == "Regression":

        print(
            "✓ Starting regression workflow."
        )


        # ======================================
        # RUN REGRESSION ENGINE
        # ======================================

        (
            regression_results,
            regression_cv_results,
            regression_models,
            regression_diagnostics

        ) = run_regression_engine(

            preprocessor,

            X_train,
            X_test,

            y_train,
            y_test,

            X,
            y,

            n_splits=5
        )


        # ======================================
        # SELECT INSPECTION MODEL
        # ======================================

        inspection_model_name = (
            regression_results
            .iloc[0]["Model"]
        )


        inspection_model = (
            regression_models[
                inspection_model_name
            ]
        )


        print(
            "\n================================"
        )

        print(
            "REGRESSION INSPECTION MODEL"
        )

        print(
            "================================"
        )

        print(
            f"Inspection Model: "
            f"{inspection_model_name}"
        )


        # ======================================
        # EXPLAINABILITY V2
        # ======================================

        explanation_results = (
            explain_model(
                inspection_model,
                X_explain=X_test,
                top_n=10
            )
        )


        # ======================================
        # STRUCTURED OUTPUT
        # ======================================

        return {

            "problem_type":
                "Regression",

            "model_comparison":
                regression_results,

            "cross_validation":
                regression_cv_results,

            "trained_models":
                regression_models,

            "inspection_model":
                inspection_model_name,

            "diagnostics":
                regression_diagnostics,

            "explainability":
                explanation_results
        }


    # ==========================================
    # UNSUPPORTED PROBLEM
    # ==========================================

    else:

        raise ValueError(
            f"Unsupported ML problem type: "
            f"{problem_type}"
        )