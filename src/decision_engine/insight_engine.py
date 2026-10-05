# ==========================================
# DATALENS AI
# DECISION / INSIGHT ENGINE V1
# ==========================================

import numpy as np
import pandas as pd


# ==========================================
# SAFE PYTHON VALUE
# ==========================================

def _python_value(value):
    """
    Convert NumPy scalar values into normal
    Python values for JSON-safe output.
    """

    if isinstance(value, np.generic):
        return value.item()

    return value


# ==========================================
# ADD INSIGHT
# ==========================================

def _add_insight(
    collection,
    insight_id,
    category,
    title,
    message,
    priority,
    evidence,
    recommendation=None
):
    """
    Add one structured, evidence-backed insight.

    Priority values:

        high
        medium
        low
        info
    """

    insight = {
        "id":
            insight_id,

        "category":
            category,

        "title":
            title,

        "message":
            message,

        "priority":
            priority,

        "evidence":
            evidence
    }

    if recommendation is not None:

        insight[
            "recommendation"
        ] = recommendation

    collection.append(
        insight
    )


# ==========================================
# DATA QUALITY INSIGHTS
# ==========================================

def _generate_data_quality_insights(
    df
):
    """
    Generate factual dataset-quality insights.

    These rules do not modify the dataset.
    """

    insights = []

    total_rows = int(
        len(df)
    )

    total_columns = int(
        len(df.columns)
    )

    total_cells = (
        total_rows
        *
        total_columns
    )

    missing_values = int(
        df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = int(
        df.duplicated()
        .sum()
    )


    # ==========================================
    # MISSING VALUES
    # ==========================================

    missing_percentage = 0.0

    if total_cells > 0:

        missing_percentage = (
            missing_values
            /
            total_cells
            *
            100
        )


    if missing_values == 0:

        _add_insight(
            collection=insights,

            insight_id=
                "data_missing_none",

            category=
                "data_quality",

            title=
                "No Missing Values Detected",

            message=
                (
                    "The dataset does not contain "
                    "missing values."
                ),

            priority=
                "info",

            evidence={
                "missing_values":
                    0,

                "missing_percentage":
                    0.0
            }
        )


    elif missing_percentage >= 20:

        _add_insight(
            collection=insights,

            insight_id=
                "data_missing_high",

            category=
                "data_quality",

            title=
                "High Missing-Value Presence",

            message=
                (
                    f"The dataset contains "
                    f"{missing_values} missing "
                    f"values, representing "
                    f"{missing_percentage:.2f}% "
                    f"of all cells."
                ),

            priority=
                "high",

            evidence={
                "missing_values":
                    missing_values,

                "missing_percentage":
                    round(
                        missing_percentage,
                        2
                    )
            },

            recommendation=
                (
                    "Review columns with missing "
                    "values and verify whether "
                    "imputation, exclusion, or "
                    "source-data correction is "
                    "appropriate."
                )
        )


    elif missing_percentage >= 5:

        _add_insight(
            collection=insights,

            insight_id=
                "data_missing_moderate",

            category=
                "data_quality",

            title=
                "Moderate Missing-Value Presence",

            message=
                (
                    f"The dataset contains "
                    f"{missing_values} missing "
                    f"values ({missing_percentage:.2f}% "
                    f"of all cells)."
                ),

            priority=
                "medium",

            evidence={
                "missing_values":
                    missing_values,

                "missing_percentage":
                    round(
                        missing_percentage,
                        2
                    )
            },

            recommendation=
                (
                    "Review missingness patterns "
                    "before interpreting affected "
                    "variables."
                )
        )


    else:

        _add_insight(
            collection=insights,

            insight_id=
                "data_missing_low",

            category=
                "data_quality",

            title=
                "Limited Missing Values",

            message=
                (
                    f"The dataset contains "
                    f"{missing_values} missing "
                    f"values ({missing_percentage:.2f}% "
                    f"of all cells)."
                ),

            priority=
                "low",

            evidence={
                "missing_values":
                    missing_values,

                "missing_percentage":
                    round(
                        missing_percentage,
                        2
                    )
            }
        )


    # ==========================================
    # DUPLICATES
    # ==========================================

    duplicate_percentage = 0.0

    if total_rows > 0:

        duplicate_percentage = (
            duplicate_rows
            /
            total_rows
            *
            100
        )


    if duplicate_rows == 0:

        _add_insight(
            collection=insights,

            insight_id=
                "data_duplicates_none",

            category=
                "data_quality",

            title=
                "No Duplicate Records Detected",

            message=
                (
                    "No exact duplicate rows were "
                    "detected in the dataset."
                ),

            priority=
                "info",

            evidence={
                "duplicate_rows":
                    0,

                "duplicate_percentage":
                    0.0
            }
        )


    elif duplicate_percentage >= 10:

        _add_insight(
            collection=insights,

            insight_id=
                "data_duplicates_high",

            category=
                "data_quality",

            title=
                "High Duplicate-Record Presence",

            message=
                (
                    f"{duplicate_rows} duplicate "
                    f"records were detected "
                    f"({duplicate_percentage:.2f}% "
                    f"of rows)."
                ),

            priority=
                "high",

            evidence={
                "duplicate_rows":
                    duplicate_rows,

                "duplicate_percentage":
                    round(
                        duplicate_percentage,
                        2
                    )
            },

            recommendation=
                (
                    "Investigate whether duplicates "
                    "represent repeated valid events "
                    "or unintended duplicate records."
                )
        )


    else:

        _add_insight(
            collection=insights,

            insight_id=
                "data_duplicates_present",

            category=
                "data_quality",

            title=
                "Duplicate Records Detected",

            message=
                (
                    f"{duplicate_rows} duplicate "
                    f"records were detected "
                    f"({duplicate_percentage:.2f}% "
                    f"of rows)."
                ),

            priority=
                "medium",

            evidence={
                "duplicate_rows":
                    duplicate_rows,

                "duplicate_percentage":
                    round(
                        duplicate_percentage,
                        2
                    )
            },

            recommendation=
                (
                    "Review duplicate records before "
                    "using the dataset for business "
                    "decisions."
                )
        )


    return insights


# ==========================================
# CLASSIFICATION INSIGHTS
# ==========================================

def _generate_classification_insights(
    ml_results
):
    """
    Generate model observations for a
    classification workflow.
    """

    insights = []

    evaluation = (
        ml_results.get(
            "evaluation"
        )
        or {}
    )


    # ==========================================
    # ACCURACY
    # ==========================================

    accuracy = (
        evaluation.get(
            "accuracy"
        )
    )


    if accuracy is not None:

        accuracy = float(
            accuracy
        )


        if accuracy < 0.60:

            priority = "high"

            recommendation = (
                "Review feature quality, class "
                "balance, model selection, and "
                "validation results before relying "
                "on predictions."
            )


        elif accuracy < 0.75:

            priority = "medium"

            recommendation = (
                "Review class-level performance "
                "and cross-validation before "
                "operational use."
            )


        else:

            priority = "info"

            recommendation = None


        _add_insight(
            collection=insights,

            insight_id=
                "classification_accuracy",

            category=
                "model_performance",

            title=
                "Classification Accuracy",

            message=
                (
                    f"The base classification "
                    f"model achieved an accuracy "
                    f"of {accuracy:.4f}."
                ),

            priority=
                priority,

            evidence={
                "accuracy":
                    round(
                        accuracy,
                        6
                    )
            },

            recommendation=
                recommendation
        )


    # ==========================================
    # CLASS PERFORMANCE
    # ==========================================

    class_performance = (
        ml_results.get(
            "class_performance"
        )
    )


    if isinstance(
        class_performance,
        dict
    ):

        recall = (
            class_performance.get(
                "recall"
            )
        )

        precision = (
            class_performance.get(
                "precision"
            )
        )

        f1_score = (
            class_performance.get(
                "f1_score"
            )
        )


        if recall is not None:

            recall = float(
                recall
            )


            if recall < 0.60:

                _add_insight(
                    collection=insights,

                    insight_id=
                        "classification_low_recall",

                    category=
                        "performance_risk",

                    title=
                        "Low Positive-Class Recall",

                    message=
                        (
                            f"Positive-class recall "
                            f"is {recall:.4f}, meaning "
                            f"a notable share of actual "
                            f"positive cases may not be "
                            f"identified by the current "
                            f"model."
                        ),

                    priority=
                        "high",

                    evidence={
                        "recall":
                            round(
                                recall,
                                6
                            )
                    },

                    recommendation=
                        (
                            "Review the confusion "
                            "matrix and threshold "
                            "analysis before selecting "
                            "an operating threshold."
                        )
                )


        if precision is not None:

            precision = float(
                precision
            )


            if precision < 0.60:

                _add_insight(
                    collection=insights,

                    insight_id=
                        "classification_low_precision",

                    category=
                        "performance_risk",

                    title=
                        "Low Positive-Class Precision",

                    message=
                        (
                            f"Positive-class precision "
                            f"is {precision:.4f}, so "
                            f"predicted positive cases "
                            f"include a notable share "
                            f"of false positives."
                        ),

                    priority=
                        "medium",

                    evidence={
                        "precision":
                            round(
                                precision,
                                6
                            )
                    },

                    recommendation=
                        (
                            "Review threshold trade-offs "
                            "and the operational cost "
                            "of false positives."
                        )
                )


        if f1_score is not None:

            f1_score = float(
                f1_score
            )


            if f1_score < 0.60:

                _add_insight(
                    collection=insights,

                    insight_id=
                        "classification_low_f1",

                    category=
                        "performance_risk",

                    title=
                        "Weak Precision-Recall Balance",

                    message=
                        (
                            f"The positive-class F1 "
                            f"score is {f1_score:.4f}."
                        ),

                    priority=
                        "medium",

                    evidence={
                        "f1_score":
                            round(
                                f1_score,
                                6
                            )
                    }
                )


    # ==========================================
    # CROSS-VALIDATION
    # ==========================================

    cv_results = (
        ml_results.get(
            "cross_validation"
        )
    )


    if isinstance(
        cv_results,
        pd.DataFrame
    ):

        if not cv_results.empty:

            _add_insight(
                collection=insights,

                insight_id=
                    "classification_cv_available",

                category=
                    "model_validation",

                title=
                    "Cross-Validation Results Available",

                message=
                    (
                        "Cross-validation results are "
                        "available and should be "
                        "considered alongside single "
                        "train/test split metrics."
                    ),

                priority=
                    "info",

                evidence={
                    "models_evaluated":
                        int(
                            len(
                                cv_results
                            )
                        )
                }
            )


    return insights


# ==========================================
# REGRESSION INSIGHTS
# ==========================================

def _generate_regression_insights(
    ml_results
):
    """
    Generate model observations for a
    regression workflow.
    """

    insights = []

    model_comparison = (
        ml_results.get(
            "model_comparison"
        )
    )


    if not isinstance(
        model_comparison,
        pd.DataFrame
    ):

        return insights


    if model_comparison.empty:

        return insights


    # ==========================================
    # INSPECTION MODEL
    # ==========================================

    inspection_model = (
        ml_results.get(
            "inspection_model"
        )
    )


    first_row = (
        model_comparison
        .iloc[0]
    )


    evidence = {}


    for possible_column in [
        "Model",
        "MAE",
        "MSE",
        "RMSE",
        "R2",
        "R²"
    ]:

        if (
            possible_column
            in model_comparison.columns
        ):

            value = first_row[
                possible_column
            ]

            evidence[
                possible_column
            ] = _python_value(
                value
            )


    _add_insight(
        collection=insights,

        insight_id=
            "regression_inspection_model",

        category=
            "model_performance",

        title=
            "Regression Inspection Model",

        message=
            (
                f"{inspection_model} is currently "
                f"used by DataLens as the regression "
                f"inspection model based on the "
                f"existing test-RMSE ordering."
            ),

        priority=
            "info",

        evidence=
            evidence,

        recommendation=
            (
                "Use cross-validation and business "
                "requirements together with test "
                "metrics before selecting a final "
                "production model."
            )
    )


    # ==========================================
    # R2 RISK
    # ==========================================

    r2_column = None

    if "R2" in model_comparison.columns:
        r2_column = "R2"

    elif "R²" in model_comparison.columns:
        r2_column = "R²"


    if r2_column is not None:

        r2 = float(
            first_row[
                r2_column
            ]
        )


        if r2 < 0:

            _add_insight(
                collection=insights,

                insight_id=
                    "regression_negative_r2",

                category=
                    "performance_risk",

                title=
                    "Negative R² Detected",

                message=
                    (
                        f"The inspection model has "
                        f"an R² of {r2:.4f}. On this "
                        f"test split, its squared-error "
                        f"performance is worse than "
                        f"predicting the test-target "
                        f"mean for every observation."
                    ),

                priority=
                    "high",

                evidence={
                    "r2":
                        round(
                            r2,
                            6
                        )
                },

                recommendation=
                    (
                        "Review features, target "
                        "quality, model suitability, "
                        "and cross-validation before "
                        "using predictions."
                    )
            )


        elif r2 < 0.50:

            _add_insight(
                collection=insights,

                insight_id=
                    "regression_low_r2",

                category=
                    "performance_risk",

                title=
                    "Limited Regression Fit",

                message=
                    (
                        f"The inspection model has "
                        f"an R² of {r2:.4f} on the "
                        f"current test split."
                    ),

                priority=
                    "medium",

                evidence={
                    "r2":
                        round(
                            r2,
                            6
                        )
                },

                recommendation=
                    (
                        "Review cross-validation, "
                        "residual diagnostics, feature "
                        "quality, and alternative "
                        "models."
                    )
            )


    return insights


# ==========================================
# SEGMENT INSIGHTS
# ==========================================

def _generate_segment_insights(
    business_results
):
    """
    Convert existing business findings into
    traceable structured evidence.

    We do not invent new segment facts here.
    """

    insights = []

    findings_result = (
        business_results.get(
            "findings"
        )
        or {}
    )


    findings = (
        findings_result.get(
            "findings"
        )
        or []
    )


    # Keep V1 compact.
    # The existing Business Findings Engine may
    # generate many statements.

    for index, finding in enumerate(
        findings[:10],
        start=1
    ):

        _add_insight(
            collection=insights,

            insight_id=
                f"business_finding_{index}",

            category=
                "business_observation",

            title=
                f"Business Finding {index}",

            message=
                str(
                    finding
                ),

            priority=
                "info",

            evidence={
                "source":
                    "business_findings_engine"
            }
        )


    return insights


# ==========================================
# EXPLAINABILITY INSIGHTS
# ==========================================

def _generate_explainability_insights(
    ml_results
):
    """
    Summarize available model explainability
    without converting association into
    causation.
    """

    insights = []

    explanation = (
        ml_results.get(
            "explainability"
        )
    )


    if not isinstance(
        explanation,
        dict
    ):

        return insights


    if not explanation.get(
        "supported",
        False
    ):

        _add_insight(
            collection=insights,

            insight_id=
                "explainability_unsupported",

            category=
                "explainability",

            title=
                "Direct Explanation Limited",

            message=
                (
                    "The current inspection model "
                    "does not expose a supported "
                    "model-native explanation in "
                    "the current DataLens engine."
                ),

            priority=
                "info",

            evidence={
                "model":
                    explanation.get(
                        "model"
                    ),

                "explanation_type":
                    explanation.get(
                        "explanation_type"
                    )
            }
        )

        return insights


    global_explanation = (
        explanation.get(
            "global_explanation"
        )
        or {}
    )


    top_features = (
        global_explanation.get(
            "top_features"
        )
    )


    if isinstance(
        top_features,
        pd.DataFrame
    ):

        if not top_features.empty:

            feature_names = (
                top_features[
                    "Feature"
                ]
                .head(5)
                .astype(str)
                .tolist()
            )


            _add_insight(
                collection=insights,

                insight_id=
                    "explainability_top_features",

                category=
                    "explainability",

                title=
                    "Top Model-Influential Features",

                message=
                    (
                        "The model's leading "
                        "transformed features include: "
                        f"{', '.join(feature_names)}."
                    ),

                priority=
                    "info",

                evidence={
                    "features":
                        feature_names,

                    "method":
                        global_explanation.get(
                            "method"
                        )
                },

                recommendation=
                    (
                        "Interpret these as features "
                        "the model relies on, not as "
                        "proof of causal effects."
                    )
            )


    local_explanation = (
        explanation.get(
            "local_explanation"
        )
    )


    if isinstance(
        local_explanation,
        dict
    ):

        local_features = (
            local_explanation.get(
                "top_contributions"
            )
        )


        if isinstance(
            local_features,
            pd.DataFrame
        ):

            if not local_features.empty:

                names = (
                    local_features[
                        "Feature"
                    ]
                    .head(5)
                    .astype(str)
                    .tolist()
                )


                _add_insight(
                    collection=insights,

                    insight_id=
                        "local_explanation_available",

                    category=
                        "explainability",

                    title=
                        "Local Prediction Explanation Available",

                    message=
                        (
                            "DataLens generated a "
                            "feature-contribution "
                            "explanation for an "
                            "individual test "
                            "observation."
                        ),

                    priority=
                        "info",

                    evidence={
                        "prediction":
                            local_explanation.get(
                                "prediction"
                            ),

                        "leading_contributors":
                            names
                    }
                )


    return insights


# ==========================================
# PRIORITY SUMMARY
# ==========================================

def _build_priority_summary(
    all_insights
):
    """
    Group insights by priority.
    """

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
        "info": 3
    }


    sorted_insights = sorted(
        all_insights,
        key=lambda item:
            priority_order.get(
                item.get(
                    "priority",
                    "info"
                ),
                99
            )
    )


    return {
        "high": [
            insight
            for insight in sorted_insights
            if insight.get(
                "priority"
            ) == "high"
        ],

        "medium": [
            insight
            for insight in sorted_insights
            if insight.get(
                "priority"
            ) == "medium"
        ],

        "low": [
            insight
            for insight in sorted_insights
            if insight.get(
                "priority"
            ) == "low"
        ],

        "info": [
            insight
            for insight in sorted_insights
            if insight.get(
                "priority"
            ) == "info"
        ]
    }


# ==========================================
# MAIN DECISION ENGINE
# ==========================================

def generate_decision_insights(
    df,
    target_column,
    problem_type,
    ml_results,
    business_results
):
    """
    Main DataLens Decision / Insight Engine V1.

    This engine uses deterministic Python rules.

    It does NOT call an LLM.

    Its purpose is to convert analytical output
    into structured, evidence-backed insights
    before the AI Analyst explains the results.
    """

    print("\n================================")
    print("DECISION / INSIGHT ENGINE V1")
    print("================================")

    print(
        f"Problem Type: {problem_type}"
    )

    print(
        f"Target Column: {target_column}"
    )


    # ==========================================
    # DATA QUALITY
    # ==========================================

    data_quality = (
        _generate_data_quality_insights(
            df
        )
    )


    # ==========================================
    # MODEL OBSERVATIONS / RISKS
    # ==========================================

    if problem_type == "Classification":

        model_insights = (
            _generate_classification_insights(
                ml_results
            )
        )


    elif problem_type == "Regression":

        model_insights = (
            _generate_regression_insights(
                ml_results
            )
        )


    else:

        model_insights = []


    # ==========================================
    # BUSINESS / SEGMENT INSIGHTS
    # ==========================================

    segment_insights = (
        _generate_segment_insights(
            business_results
        )
    )


    # ==========================================
    # EXPLAINABILITY
    # ==========================================

    explainability_insights = (
        _generate_explainability_insights(
            ml_results
        )
    )


    # ==========================================
    # COMBINE
    # ==========================================

    all_insights = (
        data_quality
        +
        model_insights
        +
        segment_insights
        +
        explainability_insights
    )


    priorities = (
        _build_priority_summary(
            all_insights
        )
    )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    results = {
        "decision_engine_version":
            "1.0",

        "target_column":
            target_column,

        "problem_type":
            problem_type,

        "summary": {
            "total_insights":
                len(
                    all_insights
                ),

            "high_priority":
                len(
                    priorities[
                        "high"
                    ]
                ),

            "medium_priority":
                len(
                    priorities[
                        "medium"
                    ]
                ),

            "low_priority":
                len(
                    priorities[
                        "low"
                    ]
                ),

            "informational":
                len(
                    priorities[
                        "info"
                    ]
                )
        },

        "data_quality":
            data_quality,

        "model_observations":
            model_insights,

        "business_insights":
            segment_insights,

        "explainability_insights":
            explainability_insights,

        "priorities":
            priorities,

        "all_insights":
            all_insights,

        "safety": {
            "llm_generated":
                False,

            "causal_claims_allowed":
                False,

            "automatic_business_action":
                False,

            "description":
                (
                    "Insights are generated from "
                    "deterministic analytical rules. "
                    "They support interpretation but "
                    "do not automatically establish "
                    "causation or prescribe business "
                    "actions."
                )
        }
    }


    # ==========================================
    # PRINT SUMMARY
    # ==========================================

    print(
        f"Total Insights: "
        f"{results['summary']['total_insights']}"
    )

    print(
        f"High Priority: "
        f"{results['summary']['high_priority']}"
    )

    print(
        f"Medium Priority: "
        f"{results['summary']['medium_priority']}"
    )

    print(
        f"Low Priority: "
        f"{results['summary']['low_priority']}"
    )

    print(
        f"Informational: "
        f"{results['summary']['informational']}"
    )


    print("\n================================")
    print("DECISION / INSIGHT ENGINE COMPLETE")
    print("================================")


    return results