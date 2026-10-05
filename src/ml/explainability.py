# ==========================================
# DATALENS AI - EXPLAINABILITY ENGINE V2
# GLOBAL + LOCAL EXPLANATIONS
# ==========================================

import numpy as np
import pandas as pd


# ==========================================
# HELPER: PYTHON VALUE
# ==========================================

def _python_value(value):

    if isinstance(value, np.generic):
        return value.item()

    return value


# ==========================================
# HELPER: CLEAN FEATURE NAMES
# ==========================================

def _clean_feature_names(feature_names):

    clean_names = []

    for feature in feature_names:

        feature = str(feature)

        if "__" in feature:
            feature = feature.split("__", 1)[1]

        clean_names.append(feature)

    return clean_names


# ==========================================
# HELPER: GET PIPELINE COMPONENTS
# ==========================================

def _get_pipeline_components(
    trained_pipeline
):

    if not hasattr(
        trained_pipeline,
        "named_steps"
    ):
        return None, None

    if (
        "preprocessor"
        not in trained_pipeline.named_steps
    ):
        return None, None

    if (
        "model"
        not in trained_pipeline.named_steps
    ):
        return None, None

    return (
        trained_pipeline.named_steps[
            "preprocessor"
        ],
        trained_pipeline.named_steps[
            "model"
        ]
    )


# ==========================================
# HELPER: GET FEATURE NAMES
# ==========================================

def _get_feature_names(
    preprocessor
):

    try:

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

        return _clean_feature_names(
            feature_names
        )

    except Exception as error:

        print(
            "⚠ Could not extract "
            "transformed feature names."
        )

        print(
            f"Reason: {error}"
        )

        return None


# ==========================================
# GLOBAL TREE EXPLANATION
# ==========================================

def _tree_global_explanation(
    model,
    model_name,
    feature_names,
    top_n
):

    importance_values = np.asarray(
        model.feature_importances_
    )

    if (
        len(feature_names)
        != len(importance_values)
    ):

        return {
            "model": model_name,
            "supported": False,
            "explanation_type":
                "feature_importance",
            "reason":
                "Feature name/value length mismatch.",
            "global_explanation": None,
            "local_explanation": None
        }

    explanation_df = pd.DataFrame(
        {
            "Feature":
                feature_names,

            "Importance":
                importance_values
        }
    )

    explanation_df = (
        explanation_df
        .sort_values(
            by="Importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    explanation_df[
        "Importance"
    ] = (
        explanation_df[
            "Importance"
        ].round(6)
    )

    top_features = (
        explanation_df
        .head(top_n)
        .copy()
    )

    print(
        "\nExplanation Type: "
        "Tree Feature Importance"
    )

    print(
        top_features.to_string(
            index=False
        )
    )

    return {
        "model":
            model_name,

        "supported":
            True,

        "explanation_type":
            "feature_importance",

        "explanation_scope":
            "global",

        "global_explanation": {
            "method":
                "model_native_feature_importance",

            "top_features":
                top_features,

            "all_features":
                explanation_df
        },

        "local_explanation":
            None,

        "interpretation": {
            "importance_direction_available":
                False,

            "importance_is_causal":
                False,

            "description":
                (
                    "Feature importance describes "
                    "model reliance and does not "
                    "establish causation."
                )
        },

        "features":
            explanation_df
    }


# ==========================================
# GLOBAL COEFFICIENT EXPLANATION
# ==========================================

def _coefficient_global_explanation(
    model,
    model_name,
    feature_names,
    coefficients,
    top_n
):

    coefficients = np.asarray(
        coefficients
    )

    if (
        len(feature_names)
        != len(coefficients)
    ):

        return {
            "model": model_name,
            "supported": False,
            "explanation_type":
                "coefficients",
            "reason":
                "Feature name/value length mismatch.",
            "global_explanation": None,
            "local_explanation": None
        }

    explanation_df = pd.DataFrame(
        {
            "Feature":
                feature_names,

            "Coefficient":
                coefficients,

            "Absolute Coefficient":
                np.abs(coefficients)
        }
    )

    explanation_df = (
        explanation_df
        .sort_values(
            by="Absolute Coefficient",
            ascending=False
        )
        .reset_index(drop=True)
    )

    explanation_df[
        [
            "Coefficient",
            "Absolute Coefficient"
        ]
    ] = (
        explanation_df[
            [
                "Coefficient",
                "Absolute Coefficient"
            ]
        ].round(6)
    )

    explanation_df[
        "Direction"
    ] = np.where(
        explanation_df[
            "Coefficient"
        ] > 0,
        "positive",
        np.where(
            explanation_df[
                "Coefficient"
            ] < 0,
            "negative",
            "neutral"
        )
    )

    top_features = (
        explanation_df
        .head(top_n)
        .copy()
    )

    positive_features = (
        explanation_df[
            explanation_df[
                "Coefficient"
            ] > 0
        ]
        .sort_values(
            by="Coefficient",
            ascending=False
        )
        .head(top_n)
        .copy()
    )

    negative_features = (
        explanation_df[
            explanation_df[
                "Coefficient"
            ] < 0
        ]
        .sort_values(
            by="Coefficient",
            ascending=True
        )
        .head(top_n)
        .copy()
    )

    print(
        "\nExplanation Type: "
        "Model Coefficients"
    )

    print(
        top_features.to_string(
            index=False
        )
    )

    return {
        "model":
            model_name,

        "supported":
            True,

        "explanation_type":
            "coefficients",

        "explanation_scope":
            "global",

        "global_explanation": {
            "method":
                "model_native_coefficients",

            "top_features":
                top_features,

            "positive_features":
                positive_features,

            "negative_features":
                negative_features,

            "all_features":
                explanation_df
        },

        "local_explanation":
            None,

        "interpretation": {
            "direction_available":
                True,

            "coefficients_are_causal":
                False,

            "features_may_be_scaled_or_encoded":
                True,

            "per_unit_real_world_interpretation_allowed":
                False
        },

        "features":
            explanation_df
    }


# ==========================================
# MULTICLASS GLOBAL EXPLANATION
# ==========================================

def _multiclass_global_explanation(
    model,
    model_name,
    feature_names,
    coefficients,
    top_n
):

    class_results = {}

    print(
        "\nExplanation Type: "
        "Multiclass Coefficients"
    )

    for (
        class_index,
        class_label
    ) in enumerate(
        model.classes_
    ):

        class_coefficients = (
            coefficients[
                class_index
            ]
        )

        if (
            len(feature_names)
            != len(class_coefficients)
        ):
            continue

        class_df = pd.DataFrame(
            {
                "Feature":
                    feature_names,

                "Coefficient":
                    class_coefficients,

                "Absolute Coefficient":
                    np.abs(
                        class_coefficients
                    )
            }
        )

        class_df = (
            class_df
            .sort_values(
                by="Absolute Coefficient",
                ascending=False
            )
            .reset_index(drop=True)
        )

        class_df[
            [
                "Coefficient",
                "Absolute Coefficient"
            ]
        ] = (
            class_df[
                [
                    "Coefficient",
                    "Absolute Coefficient"
                ]
            ].round(6)
        )

        class_df[
            "Direction"
        ] = np.where(
            class_df[
                "Coefficient"
            ] > 0,
            "positive",
            np.where(
                class_df[
                    "Coefficient"
                ] < 0,
                "negative",
                "neutral"
            )
        )

        class_key = str(
            _python_value(
                class_label
            )
        )

        class_results[
            class_key
        ] = {
            "top_features":
                class_df.head(
                    top_n
                ).copy(),

            "all_features":
                class_df
        }

        print(
            f"\nClass: {class_label}"
        )

        print(
            class_df
            .head(top_n)
            .to_string(
                index=False
            )
        )

    return {
        "model":
            model_name,

        "supported":
            True,

        "explanation_type":
            "multiclass_coefficients",

        "explanation_scope":
            "global",

        "global_explanation": {
            "method":
                "class_specific_model_coefficients",

            "classes":
                class_results
        },

        "local_explanation":
            None,

        "interpretation": {
            "direction_available":
                True,

            "coefficients_are_causal":
                False,

            "features_may_be_scaled_or_encoded":
                True
        },

        "classes": {
            class_name:
                class_data[
                    "all_features"
                ]

            for (
                class_name,
                class_data
            ) in class_results.items()
        }
    }


# ==========================================
# LOCAL COEFFICIENT EXPLANATION
# ==========================================

def _local_coefficient_explanation(
    trained_pipeline,
    preprocessor,
    model,
    feature_names,
    X_explain,
    top_n
):
    """
    Explain individual predictions for models
    where additive coefficient contributions
    can be calculated directly.

    Contribution:

        transformed feature value
        ×
        model coefficient
    """

    if X_explain is None:
        return None

    if len(X_explain) == 0:
        return None


    # ==========================================
    # USE FIRST TEST SAMPLE
    # ==========================================

    sample = (
        X_explain
        .iloc[[0]]
        .copy()
    )


    # ==========================================
    # TRANSFORM SAMPLE
    # ==========================================

    transformed = (
        preprocessor
        .transform(sample)
    )


    if hasattr(
        transformed,
        "toarray"
    ):
        transformed = (
            transformed.toarray()
        )


    transformed = np.asarray(
        transformed
    )


    if transformed.ndim == 2:
        transformed_values = (
            transformed[0]
        )

    else:
        transformed_values = (
            transformed
        )


    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = (
        trained_pipeline
        .predict(sample)[0]
    )


    prediction = _python_value(
        prediction
    )


    # ==========================================
    # DETERMINE COEFFICIENT VECTOR
    # ==========================================

    coefficients = np.asarray(
        model.coef_
    )


    explained_class = None


    # ------------------------------------------
    # REGRESSION
    # ------------------------------------------

    if coefficients.ndim == 1:

        coefficient_values = (
            coefficients
        )


    # ------------------------------------------
    # BINARY CLASSIFICATION
    # ------------------------------------------

    elif (
        coefficients.ndim == 2
        and coefficients.shape[0] == 1
    ):

        coefficient_values = (
            coefficients[0]
        )

        if hasattr(
            model,
            "classes_"
        ):

            explained_class = (
                _python_value(
                    model.classes_[1]
                )
            )


    # ------------------------------------------
    # MULTICLASS CLASSIFICATION
    # ------------------------------------------

    elif (
        coefficients.ndim == 2
        and hasattr(
            model,
            "classes_"
        )
    ):

        class_labels = list(
            model.classes_
        )

        try:

            predicted_class_index = (
                class_labels.index(
                    prediction
                )
            )

        except ValueError:

            return None


        coefficient_values = (
            coefficients[
                predicted_class_index
            ]
        )

        explained_class = (
            prediction
        )


    else:

        return None


    # ==========================================
    # VALIDATE LENGTHS
    # ==========================================

    if not (
        len(feature_names)
        ==
        len(transformed_values)
        ==
        len(coefficient_values)
    ):

        print(
            "⚠ Local explanation skipped "
            "because transformed feature "
            "lengths do not match."
        )

        return None


    # ==========================================
    # CONTRIBUTIONS
    # ==========================================

    contributions = (
        transformed_values
        *
        coefficient_values
    )


    local_df = pd.DataFrame(
        {
            "Feature":
                feature_names,

            "Transformed Value":
                transformed_values,

            "Coefficient":
                coefficient_values,

            "Contribution":
                contributions,

            "Absolute Contribution":
                np.abs(
                    contributions
                )
        }
    )


    local_df = (
        local_df
        .sort_values(
            by="Absolute Contribution",
            ascending=False
        )
        .reset_index(drop=True)
    )


    numeric_columns = [
        "Transformed Value",
        "Coefficient",
        "Contribution",
        "Absolute Contribution"
    ]


    local_df[
        numeric_columns
    ] = (
        local_df[
            numeric_columns
        ].round(6)
    )


    local_df[
        "Direction"
    ] = np.where(
        local_df[
            "Contribution"
        ] > 0,
        "positive",
        np.where(
            local_df[
                "Contribution"
            ] < 0,
            "negative",
            "neutral"
        )
    )


    top_contributions = (
        local_df
        .head(top_n)
        .copy()
    )


    # ==========================================
    # INTERCEPT
    # ==========================================

    intercept = getattr(
        model,
        "intercept_",
        None
    )


    if intercept is not None:

        intercept_array = (
            np.asarray(
                intercept
            )
        )


        if intercept_array.ndim == 0:

            intercept_value = float(
                intercept_array
            )


        elif (
            intercept_array.size == 1
        ):

            intercept_value = float(
                intercept_array.flat[0]
            )


        elif (
            explained_class is not None
            and hasattr(
                model,
                "classes_"
            )
        ):

            class_labels = list(
                model.classes_
            )

            try:

                class_index = (
                    class_labels.index(
                        explained_class
                    )
                )

                intercept_value = float(
                    intercept_array[
                        class_index
                    ]
                )

            except (
                ValueError,
                IndexError
            ):

                intercept_value = None


        else:

            intercept_value = None


    else:

        intercept_value = None


    # ==========================================
    # RAW INPUT SAMPLE
    # ==========================================

    raw_sample = {}

    for column in sample.columns:

        raw_sample[
            str(column)
        ] = _python_value(
            sample.iloc[0][
                column
            ]
        )


    print(
        "\nLocal Prediction Explanation"
    )

    print(
        f"Prediction: {prediction}"
    )


    if explained_class is not None:

        print(
            f"Explained Class: "
            f"{explained_class}"
        )


    print(
        f"\nTop {top_n} "
        "Local Contributions:"
    )

    print(
        top_contributions.to_string(
            index=False
        )
    )


    return {
        "method":
            "coefficient_contribution",

        "sample_position":
            0,

        "raw_sample":
            raw_sample,

        "prediction":
            prediction,

        "explained_class":
            explained_class,

        "intercept":
            intercept_value,

        "top_contributions":
            top_contributions,

        "all_contributions":
            local_df,

        "formula":
            (
                "transformed_feature_value "
                "x coefficient"
            ),

        "causal_interpretation_allowed":
            False
    }


# ==========================================
# MAIN EXPLAINABILITY ENGINE
# ==========================================

def explain_model(
    trained_pipeline,
    X_explain=None,
    top_n=10
):
    """
    DataLens Explainability V2.

    Provides:

        GLOBAL EXPLANATION
            - Tree feature importance
            - Linear coefficients
            - Logistic coefficients
            - Multiclass coefficients

        LOCAL EXPLANATION
            - Individual coefficient-based
              prediction contributions

    Local explanation currently uses the first
    supplied observation.

    Tree models receive global model-native
    importance only in this version.

    Feature importance and coefficients describe
    model behavior and do NOT establish causality.
    """

    print("\n================================")
    print("MODEL EXPLAINABILITY V2")
    print("================================")


    # ==========================================
    # VALIDATE TOP N
    # ==========================================

    try:

        top_n = int(
            top_n
        )

    except (
        TypeError,
        ValueError
    ):

        top_n = 10


    top_n = max(
        1,
        top_n
    )


    # ==========================================
    # GET COMPONENTS
    # ==========================================

    (
        preprocessor,
        model

    ) = _get_pipeline_components(
        trained_pipeline
    )


    if (
        preprocessor is None
        or model is None
    ):

        return {
            "model": None,
            "supported": False,
            "explanation_type":
                "unsupported",
            "reason":
                (
                    "Expected a fitted sklearn "
                    "Pipeline containing "
                    "'preprocessor' and 'model'."
                ),
            "global_explanation": None,
            "local_explanation": None,
            "explainability_version":
                "2.0"
        }


    model_name = (
        model.__class__.__name__
    )


    print(
        f"Model: {model_name}"
    )


    # ==========================================
    # FEATURE NAMES
    # ==========================================

    feature_names = (
        _get_feature_names(
            preprocessor
        )
    )


    if feature_names is None:

        return {
            "model":
                model_name,

            "supported":
                False,

            "explanation_type":
                "unsupported",

            "reason":
                (
                    "Transformed feature names "
                    "could not be extracted."
                ),

            "global_explanation":
                None,

            "local_explanation":
                None,

            "explainability_version":
                "2.0"
        }


    print(
        f"Transformed Features: "
        f"{len(feature_names)}"
    )


    # ==========================================
    # TREE MODELS
    # ==========================================

    if hasattr(
        model,
        "feature_importances_"
    ):

        result = (
            _tree_global_explanation(
                model,
                model_name,
                feature_names,
                top_n
            )
        )


        # --------------------------------------
        # Tree feature_importances_ are global.
        #
        # We deliberately do NOT fabricate
        # per-row tree contributions.
        # --------------------------------------

        result[
            "local_explanation"
        ] = None


        result[
            "local_explanation_status"
        ] = (
            "Model-native local contribution "
            "is not implemented for tree models "
            "in Explainability V2."
        )


    # ==========================================
    # COEFFICIENT MODELS
    # ==========================================

    elif hasattr(
        model,
        "coef_"
    ):

        coefficients = np.asarray(
            model.coef_
        )


        # --------------------------------------
        # LINEAR REGRESSION
        # --------------------------------------

        if coefficients.ndim == 1:

            result = (
                _coefficient_global_explanation(
                    model,
                    model_name,
                    feature_names,
                    coefficients,
                    top_n
                )
            )


        # --------------------------------------
        # BINARY LOGISTIC REGRESSION
        # --------------------------------------

        elif (
            coefficients.ndim == 2
            and coefficients.shape[0] == 1
        ):

            result = (
                _coefficient_global_explanation(
                    model,
                    model_name,
                    feature_names,
                    coefficients[0],
                    top_n
                )
            )


            if (
                hasattr(
                    model,
                    "classes_"
                )
                and len(
                    model.classes_
                ) == 2
            ):

                result[
                    "class_direction"
                ] = {
                    "negative_class":
                        _python_value(
                            model.classes_[0]
                        ),

                    "positive_class":
                        _python_value(
                            model.classes_[1]
                        ),

                    "positive_coefficient_direction":
                        "toward_positive_class",

                    "negative_coefficient_direction":
                        "toward_negative_class"
                }


        # --------------------------------------
        # MULTICLASS
        # --------------------------------------

        else:

            if hasattr(
                model,
                "classes_"
            ):

                result = (
                    _multiclass_global_explanation(
                        model,
                        model_name,
                        feature_names,
                        coefficients,
                        top_n
                    )
                )

            else:

                result = {
                    "model":
                        model_name,

                    "supported":
                        False,

                    "explanation_type":
                        "unsupported",

                    "reason":
                        (
                            "Multiple coefficient "
                            "vectors found without "
                            "class labels."
                        ),

                    "global_explanation":
                        None,

                    "local_explanation":
                        None
                }


        # ======================================
        # LOCAL EXPLANATION
        # ======================================

        if result.get(
            "supported"
        ):

            local_explanation = (
                _local_coefficient_explanation(
                    trained_pipeline,
                    preprocessor,
                    model,
                    feature_names,
                    X_explain,
                    top_n
                )
            )


            result[
                "local_explanation"
            ] = local_explanation


            if local_explanation is not None:

                result[
                    "explanation_scope"
                ] = "global_and_local"

            else:

                result[
                    "local_explanation_status"
                ] = (
                    "No observation was available "
                    "for local explanation."
                )


    # ==========================================
    # UNSUPPORTED MODEL
    # ==========================================

    else:

        print(
            "⚠ Direct model-native explanation "
            "is not available for this model."
        )


        result = {
            "model":
                model_name,

            "supported":
                False,

            "explanation_type":
                "unsupported",

            "reason":
                (
                    "Estimator does not expose "
                    "feature_importances_ or coef_."
                ),

            "global_explanation":
                None,

            "local_explanation":
                None,

            "features":
                None
        }


    # ==========================================
    # VERSION + SAFETY METADATA
    # ==========================================

    result[
        "explainability_version"
    ] = "2.0"


    result[
        "causal_interpretation_allowed"
    ] = False


    print(
        "\n✓ Global model explanation complete."
    )


    if (
        result.get(
            "local_explanation"
        )
        is not None
    ):

        print(
            "✓ Local prediction explanation complete."
        )


    return result