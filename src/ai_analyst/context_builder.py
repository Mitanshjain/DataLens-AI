# ==========================================
# DATALENS AI - AI CONTEXT BUILDER V4
# ==========================================

import json

import numpy as np
import pandas as pd


# ==========================================
# CONTEXT SIZE SETTINGS
# ==========================================

MAX_LIST_ITEMS = 20

MAX_DATAFRAME_ROWS = 20

MAX_DIAGNOSTIC_ERRORS = 5

MAX_DECISION_INSIGHTS = 15


# ==========================================
# JSON-SAFE CONVERTER
# ==========================================

def make_json_safe(value):
    """
    Convert common Python / NumPy / Pandas
    objects into JSON-safe values.

    This function is intentionally conservative
    because the output may be sent to an LLM.

    Large raw arrays are truncated for AI
    context efficiency.

    Trained model objects are excluded.
    """

    if value is None:
        return None


    # ==========================================
    # BASIC PYTHON TYPES
    # ==========================================

    if isinstance(
        value,
        (str, int, float, bool)
    ):
        return value


    # ==========================================
    # NUMPY SCALARS
    # ==========================================

    if isinstance(
        value,
        np.generic
    ):
        return value.item()


    # ==========================================
    # NUMPY ARRAYS
    # ==========================================

    if isinstance(
        value,
        np.ndarray
    ):

        values = value.tolist()

        if len(values) > MAX_LIST_ITEMS:

            return values[
                :MAX_LIST_ITEMS
            ]

        return values


    # ==========================================
    # PANDAS DATAFRAME
    # ==========================================

    if isinstance(
        value,
        pd.DataFrame
    ):

        return (
            value
            .head(
                MAX_DATAFRAME_ROWS
            )
            .to_dict(
                orient="records"
            )
        )


    # ==========================================
    # PANDAS SERIES
    # ==========================================

    if isinstance(
        value,
        pd.Series
    ):

        return (
            value
            .head(
                MAX_LIST_ITEMS
            )
            .to_dict()
        )


    # ==========================================
    # DICTIONARY
    # ==========================================

    if isinstance(
        value,
        dict
    ):

        safe_dictionary = {}

        for key, item in value.items():

            # ----------------------------------
            # EXCLUDE TRAINED MODEL OBJECTS
            # ----------------------------------

            if key in {
                "base_model",
                "trained_models",
                "imbalance_models"
            }:
                continue

            safe_dictionary[
                str(key)
            ] = make_json_safe(
                item
            )

        return safe_dictionary


    # ==========================================
    # LIST / TUPLE / SET
    # ==========================================

    if isinstance(
        value,
        (list, tuple, set)
    ):

        values = list(
            value
        )

        values = values[
            :MAX_LIST_ITEMS
        ]

        return [
            make_json_safe(item)
            for item in values
        ]


    # ==========================================
    # UNKNOWN OBJECT
    # ==========================================

    return str(value)


# ==========================================
# COMPACT CLASSIFICATION DIAGNOSTICS
# ==========================================

def compact_classification_diagnostics(
    diagnostics
):
    """
    Keep useful classification diagnostic
    summaries while removing large curve arrays
    and repetitive threshold information.
    """

    if not isinstance(
        diagnostics,
        dict
    ):
        return None


    compact = {

        "diagnostic_type":
            diagnostics.get(
                "diagnostic_type"
            ),

        "class_labels":
            make_json_safe(
                diagnostics.get(
                    "class_labels"
                )
            ),

        "error_analysis":
            make_json_safe(
                diagnostics.get(
                    "error_analysis"
                )
            )
    }


    # ==========================================
    # ROC SUMMARY
    # ==========================================

    roc = diagnostics.get(
        "roc"
    )

    if isinstance(
        roc,
        dict
    ):

        compact[
            "roc"
        ] = {

            "auc":
                make_json_safe(
                    roc.get(
                        "auc"
                    )
                )
        }


    # ==========================================
    # PRECISION-RECALL SUMMARY
    # ==========================================

    precision_recall = (
        diagnostics.get(
            "precision_recall"
        )
    )

    if isinstance(
        precision_recall,
        dict
    ):

        compact[
            "precision_recall"
        ] = {

            "average_precision":
                make_json_safe(
                    precision_recall.get(
                        "average_precision"
                    )
                )
        }


    # ==========================================
    # THRESHOLD SUMMARY
    # ==========================================
    #
    # Keep only a few representative thresholds
    # instead of sending every threshold result.
    # ==========================================

    threshold_analysis = (
        diagnostics.get(
            "threshold_analysis"
        )
    )

    if isinstance(
        threshold_analysis,
        list
    ):

        representative_thresholds = []

        preferred_thresholds = {
            0.3,
            0.5,
            0.7
        }

        for item in threshold_analysis:

            if not isinstance(
                item,
                dict
            ):
                continue

            threshold = item.get(
                "threshold"
            )

            try:

                rounded_threshold = round(
                    float(threshold),
                    1
                )

            except (
                TypeError,
                ValueError
            ):
                continue

            if (
                rounded_threshold
                in preferred_thresholds
            ):

                representative_thresholds.append(
                    make_json_safe(
                        item
                    )
                )

        compact[
            "representative_thresholds"
        ] = representative_thresholds


    return compact


# ==========================================
# COMPACT REGRESSION DIAGNOSTICS
# ==========================================

def compact_regression_diagnostics(
    diagnostics
):
    """
    Keep statistical regression diagnostics
    while excluding raw plot arrays.

    Full plot data remains available in the
    normal Python/API result.

    Only the AI context is compressed.
    """

    if not isinstance(
        diagnostics,
        dict
    ):
        return None


    compact = {}


    for model_name, model_diagnostics in (
        diagnostics.items()
    ):

        if not isinstance(
            model_diagnostics,
            dict
        ):
            continue


        compact_model = {

            "diagnostic_type":
                model_diagnostics.get(
                    "diagnostic_type"
                ),

            "sample_count":
                make_json_safe(
                    model_diagnostics.get(
                        "sample_count"
                    )
                ),

            "metrics":
                make_json_safe(
                    model_diagnostics.get(
                        "metrics"
                    )
                ),

            "residual_statistics":
                make_json_safe(
                    model_diagnostics.get(
                        "residual_statistics"
                    )
                ),

            "prediction_direction":
                make_json_safe(
                    model_diagnostics.get(
                        "prediction_direction"
                    )
                )
        }


        # --------------------------------------
        # KEEP ONLY LARGEST FEW ERRORS
        # --------------------------------------

        largest_errors = (
            model_diagnostics.get(
                "largest_errors"
            )
        )

        if isinstance(
            largest_errors,
            list
        ):

            compact_model[
                "largest_errors"
            ] = make_json_safe(
                largest_errors[
                    :MAX_DIAGNOSTIC_ERRORS
                ]
            )


        # --------------------------------------
        # IMPORTANT
        # --------------------------------------
        #
        # plot_data is deliberately NOT added.
        #
        # It may contain:
        #
        # actual
        # predicted
        # residuals
        # absolute_errors
        #
        # These arrays belong to dashboard
        # visualization, not the LLM prompt.
        # --------------------------------------


        compact[
            str(model_name)
        ] = compact_model


    return compact


# ==========================================
# COMPACT EXPLAINABILITY
# ==========================================

def compact_explainability_for_ai(
    explanation
):
    """
    Keep the important global/local explanation
    information while avoiding duplicated large
    DataFrames.

    Full explainability remains available to
    Python/API/reporting.
    """

    if not isinstance(
        explanation,
        dict
    ):
        return make_json_safe(
            explanation
        )


    compact = {

        "model":
            explanation.get(
                "model"
            ),

        "supported":
            explanation.get(
                "supported"
            ),

        "explanation_type":
            explanation.get(
                "explanation_type"
            ),

        "explanation_scope":
            explanation.get(
                "explanation_scope"
            ),

        "explainability_version":
            explanation.get(
                "explainability_version"
            ),

        "causal_interpretation_allowed":
            explanation.get(
                "causal_interpretation_allowed"
            )
    }


    # ==========================================
    # INTERPRETATION METADATA
    # ==========================================

    if explanation.get(
        "interpretation"
    ) is not None:

        compact[
            "interpretation"
        ] = make_json_safe(
            explanation.get(
                "interpretation"
            )
        )


    # ==========================================
    # CLASS DIRECTION
    # ==========================================

    if explanation.get(
        "class_direction"
    ) is not None:

        compact[
            "class_direction"
        ] = make_json_safe(
            explanation.get(
                "class_direction"
            )
        )


    # ==========================================
    # GLOBAL EXPLANATION
    # ==========================================

    global_explanation = (
        explanation.get(
            "global_explanation"
        )
    )


    if isinstance(
        global_explanation,
        dict
    ):

        compact_global = {

            "method":
                global_explanation.get(
                    "method"
                )
        }


        # --------------------------------------
        # SINGLE GLOBAL TOP FEATURES
        # --------------------------------------

        top_features = (
            global_explanation.get(
                "top_features"
            )
        )

        if top_features is not None:

            compact_global[
                "top_features"
            ] = make_json_safe(
                top_features
            )


        # --------------------------------------
        # POSITIVE FEATURES
        # --------------------------------------

        positive_features = (
            global_explanation.get(
                "positive_features"
            )
        )

        if positive_features is not None:

            compact_global[
                "positive_features"
            ] = make_json_safe(
                positive_features
            )


        # --------------------------------------
        # NEGATIVE FEATURES
        # --------------------------------------

        negative_features = (
            global_explanation.get(
                "negative_features"
            )
        )

        if negative_features is not None:

            compact_global[
                "negative_features"
            ] = make_json_safe(
                negative_features
            )


        # --------------------------------------
        # MULTICLASS EXPLANATION
        # --------------------------------------

        classes = (
            global_explanation.get(
                "classes"
            )
        )

        if isinstance(
            classes,
            dict
        ):

            compact_classes = {}

            for (
                class_name,
                class_data
            ) in classes.items():

                if not isinstance(
                    class_data,
                    dict
                ):
                    continue

                compact_classes[
                    str(class_name)
                ] = {

                    "top_features":
                        make_json_safe(
                            class_data.get(
                                "top_features"
                            )
                        )
                }

            compact_global[
                "classes"
            ] = compact_classes


        compact[
            "global_explanation"
        ] = compact_global


    # ==========================================
    # LOCAL EXPLANATION
    # ==========================================

    local_explanation = (
        explanation.get(
            "local_explanation"
        )
    )


    if isinstance(
        local_explanation,
        dict
    ):

        compact_local = {

            "method":
                local_explanation.get(
                    "method"
                ),

            "prediction":
                make_json_safe(
                    local_explanation.get(
                        "prediction"
                    )
                ),

            "explained_class":
                make_json_safe(
                    local_explanation.get(
                        "explained_class"
                    )
                ),

            "intercept":
                make_json_safe(
                    local_explanation.get(
                        "intercept"
                    )
                ),

            "formula":
                local_explanation.get(
                    "formula"
                ),

            "causal_interpretation_allowed":
                local_explanation.get(
                    "causal_interpretation_allowed"
                )
        }


        top_contributions = (
            local_explanation.get(
                "top_contributions"
            )
        )

        if top_contributions is not None:

            compact_local[
                "top_contributions"
            ] = make_json_safe(
                top_contributions
            )


        compact[
            "local_explanation"
        ] = compact_local


    elif explanation.get(
        "local_explanation_status"
    ) is not None:

        compact[
            "local_explanation_status"
        ] = explanation.get(
            "local_explanation_status"
        )


    # ==========================================
    # UNSUPPORTED REASON
    # ==========================================

    if explanation.get(
        "reason"
    ) is not None:

        compact[
            "reason"
        ] = explanation.get(
            "reason"
        )


    return compact


# ==========================================
# COMPACT ML RESULTS FOR AI
# ==========================================

def compact_ml_results_for_ai(
    ml_results,
    problem_type
):
    """
    Create a compact LLM-specific copy of
    Machine Learning results.

    The original ml_results object is NOT
    modified.
    """

    if not isinstance(
        ml_results,
        dict
    ):

        return make_json_safe(
            ml_results
        )


    compact = {}


    # ==========================================
    # COMMON / IMPORTANT ML SECTIONS
    # ==========================================

    allowed_keys = {

        "problem_type",

        "evaluation",

        "class_performance",

        "model_comparison",

        "cross_validation",

        "imbalance_results",

        "inspection_model"
    }


    for key in allowed_keys:

        if (
            key in ml_results
            and ml_results[key] is not None
        ):

            compact[
                key
            ] = make_json_safe(
                ml_results[
                    key
                ]
            )


    # ==========================================
    # EXPLAINABILITY
    # ==========================================

    explanation = (
        ml_results.get(
            "explainability"
        )
    )

    if explanation is not None:

        compact[
            "explainability"
        ] = (
            compact_explainability_for_ai(
                explanation
            )
        )


    # ==========================================
    # DIAGNOSTICS
    # ==========================================

    diagnostics = (
        ml_results.get(
            "diagnostics"
        )
    )


    if diagnostics is not None:

        if problem_type == "Classification":

            compact[
                "diagnostics"
            ] = (
                compact_classification_diagnostics(
                    diagnostics
                )
            )


        elif problem_type == "Regression":

            compact[
                "diagnostics"
            ] = (
                compact_regression_diagnostics(
                    diagnostics
                )
            )


        else:

            compact[
                "diagnostics"
            ] = make_json_safe(
                diagnostics
            )


    return compact


# ==========================================
# COMPACT BUSINESS RESULTS
# ==========================================

def compact_business_results_for_ai(
    business_results
):
    """
    Convert business analytics into a safe,
    bounded LLM context.

    Business analytics are preserved, but
    large arrays/lists/DataFrames are limited
    by make_json_safe().
    """

    return make_json_safe(
        business_results
    )


# ==========================================
# COMPACT DECISION RESULTS
# ==========================================

def compact_decision_results_for_ai(
    decision_results
):
    """
    Create a compact LLM-specific representation
    of Decision / Insight Engine output.

    IMPORTANT:

    Decision Engine V1 contains overlapping
    structures:

        data_quality
        model_observations
        business_insights
        explainability_insights
        priorities
        all_insights

    Sending every structure would repeat the
    same insight multiple times.

    Therefore the AI receives:

        - engine version
        - target/problem information
        - summary
        - bounded all_insights
        - safety metadata

    Full decision_results remain available to
    Python/API/reporting.
    """

    if decision_results is None:
        return None


    if not isinstance(
        decision_results,
        dict
    ):

        return make_json_safe(
            decision_results
        )


    all_insights = (
        decision_results.get(
            "all_insights"
        )
        or []
    )


    compact_insights = []


    if isinstance(
        all_insights,
        list
    ):

        # --------------------------------------
        # PRIORITY ORDER
        # --------------------------------------

        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2,
            "info": 3
        }


        # --------------------------------------
        # SORT COPY ONLY
        # --------------------------------------
        #
        # Do not modify original Decision Engine
        # results.
        # --------------------------------------

        sorted_insights = sorted(

            all_insights,

            key=lambda item:
                priority_order.get(
                    item.get(
                        "priority",
                        "info"
                    )
                    if isinstance(
                        item,
                        dict
                    )
                    else "info",
                    99
                )
        )


        compact_insights = (
            sorted_insights[
                :MAX_DECISION_INSIGHTS
            ]
        )


    return {

        "decision_engine_version":
            decision_results.get(
                "decision_engine_version"
            ),

        "target_column":
            decision_results.get(
                "target_column"
            ),

        "problem_type":
            decision_results.get(
                "problem_type"
            ),

        "summary":
            make_json_safe(
                decision_results.get(
                    "summary"
                )
            ),

        "insights":
            make_json_safe(
                compact_insights
            ),

        "safety":
            make_json_safe(
                decision_results.get(
                    "safety"
                )
            )
    }


# ==========================================
# BUILD AI CONTEXT
# ==========================================

def build_ai_context(
    df,
    target_column,
    problem_type,
    ml_results,
    business_results,
    decision_results=None
):
    """
    Build grounded, compact and JSON-safe
    context for the DataLens AI Analyst.

    IMPORTANT ARCHITECTURE:

    Full analytics remain available to:

        - Python
        - API
        - Dashboard
        - Reporting

    The LLM receives only the information
    needed to explain the calculated results.

    Decision Engine results are also compressed
    before entering the LLM context.
    """

    print("\n================================")
    print("BUILDING AI ANALYST CONTEXT V4")
    print("================================")


    # ==========================================
    # DATASET SUMMARY
    # ==========================================

    dataset_summary = {

        "total_records":
            int(
                len(df)
            ),

        "total_columns":
            int(
                len(df.columns)
            ),

        "columns":
            df.columns.tolist(),

        "target_column":
            target_column,

        "problem_type":
            problem_type,

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            )
    }


    # ==========================================
    # COMPACT ML RESULTS
    # ==========================================

    safe_ml_results = (
        compact_ml_results_for_ai(
            ml_results,
            problem_type
        )
    )


    # ==========================================
    # COMPACT BUSINESS RESULTS
    # ==========================================

    safe_business_results = (
        compact_business_results_for_ai(
            business_results
        )
    )


    # ==========================================
    # COMPACT DECISION RESULTS
    # ==========================================

    safe_decision_results = (
        compact_decision_results_for_ai(
            decision_results
        )
    )


    # ==========================================
    # SEMANTIC GROUNDING METADATA
    # ==========================================

    semantic_metadata = {


        # --------------------------------------
        # DATASET CONTEXT
        # --------------------------------------

        "dataset_context": {

            "purpose":
                "development_and_testing",

            "real_world_generalization_confirmed":
                False
        },


        # --------------------------------------
        # PREPROCESSING INFORMATION
        # --------------------------------------

        "preprocessing": {

            "numerical_features_scaled":
                True,

            "scaling_method":
                "StandardScaler",

            "categorical_features_encoded":
                True,

            "encoding_method":
                "OneHotEncoder"
        },


        # --------------------------------------
        # COEFFICIENT INTERPRETATION
        # --------------------------------------

        "coefficient_interpretation": {

            "numerical_coefficients_are_on_scaled_features":
                True,

            "per_unit_real_world_interpretation_allowed":
                False,

            "coefficients_are_causal":
                False,

            "categorical_coefficients_are_encoded_model_terms":
                True
        },


        # --------------------------------------
        # MODEL SELECTION / DEPLOYMENT
        # --------------------------------------

        "model_selection": {

            "production_model_selected":
                False,

            "production_validation_completed":
                False,

            "deployment_recommendation_allowed":
                False
        },


        # --------------------------------------
        # GENERAL INTERPRETATION RULES
        # --------------------------------------

        "interpretation_rules": {

            "correlation_implies_causation":
                False,

            "missing_values_are_real_categories":
                False,

            "test_cv_difference_proves_overfitting":
                False,

            "feature_importance_implies_causation":
                False,

            "local_contribution_implies_causation":
                False
        },


        # --------------------------------------
        # DECISION ENGINE INTERPRETATION
        # --------------------------------------

        "decision_engine": {

            "llm_generated":
                False,

            "deterministic_rules":
                True,

            "priorities_are_analytical":
                True,

            "priorities_prove_business_impact":
                False,

            "automatic_business_action_allowed":
                False,

            "recommendations_are_possible_next_steps":
                True
        }
    }


    # ==========================================
    # FINAL GROUNDED CONTEXT
    # ==========================================

    context = {

        "dataset":
            dataset_summary,

        "semantic_metadata":
            semantic_metadata,

        "machine_learning":
            safe_ml_results,

        "business_analytics":
            safe_business_results,

        "decision_insights":
            safe_decision_results
    }


    # ==========================================
    # CONVERT CONTEXT TO JSON
    # ==========================================

    context_json = json.dumps(

        context,

        ensure_ascii=False,

        default=str,

        separators=(
            ",",
            ":"
        )
    )


    # ==========================================
    # CONTEXT SIZE INFORMATION
    # ==========================================

    context_characters = len(
        context_json
    )


    approximate_tokens = int(
        context_characters / 4
    )


    # ==========================================
    # STATUS
    # ==========================================

    print(
        "✓ Dataset context prepared."
    )

    print(
        "✓ Semantic grounding metadata prepared."
    )

    print(
        "✓ ML results compressed for AI."
    )

    print(
        "✓ Regression/classification diagnostics "
        "compressed."
    )

    print(
        "✓ Explainability results compressed."
    )

    print(
        "✓ Raw diagnostic plot arrays excluded "
        "from AI context."
    )

    print(
        "✓ Business analytics prepared."
    )

    if safe_decision_results is not None:

        print(
            "✓ Decision insights compressed "
            "and prepared."
        )

    else:

        print(
            "✓ No Decision Engine results "
            "supplied."
        )

    print(
        "✓ Trained model objects excluded."
    )

    print(
        "✓ AI context is JSON-safe."
    )

    print(
        f"AI Context Characters: "
        f"{context_characters}"
    )

    print(
        f"Approximate Context Tokens: "
        f"{approximate_tokens}"
    )


    # ==========================================
    # RETURN GROUNDED CONTEXT
    # ==========================================

    return context_json