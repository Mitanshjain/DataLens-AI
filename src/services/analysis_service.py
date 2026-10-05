# ==========================================
# DATALENS AI
# COMPLETE ANALYSIS SERVICE V1
# ==========================================


# ==========================================
# DATA PROFILER IMPORTS
# ==========================================

from src.data_profiler.loader import (
    load_dataset
)

from src.data_profiler.validator import (
    validate_dataset
)

from src.data_profiler.profiler import (
    profile_dataset
)

from src.data_profiler.missing_values import (
    analyze_missing_values
)

from src.data_profiler.duplicates import (
    analyze_duplicates
)

from src.data_profiler.data_types import (
    analyze_data_types
)

from src.data_profiler.feature_types import (
    detect_feature_types
)

from src.data_profiler.cardinality import (
    analyze_cardinality
)

from src.data_profiler.outliers import (
    detect_outliers
)

from src.data_profiler.imbalance import (
    analyze_class_imbalance
)

from src.data_profiler.suspicious_columns import (
    detect_suspicious_columns
)

from src.data_profiler.quality_score import (
    calculate_quality_score
)


# ==========================================
# EDA IMPORTS
# ==========================================

from src.eda.descriptive_stats import (
    analyze_descriptive_statistics
)

from src.eda.distributions import (
    analyze_distributions
)

from src.eda.correlations import (
    analyze_correlations
)

from src.eda.visualizations import (
    generate_numerical_histograms,
    generate_correlation_heatmap
)

from src.eda.categorical_analysis import (
    analyze_categorical_features
)

from src.eda.relationships import (
    analyze_relationships
)

from src.eda.insights import (
    generate_eda_insights
)


# ==========================================
# ML IMPORTS
# ==========================================

from src.ml.problem_detector import (
    detect_problem_type
)

from src.ml.feature_target import (
    separate_features_target
)

from src.ml.preprocessing_analyzer import (
    analyze_preprocessing_requirements
)

from src.ml.data_split import (
    split_dataset
)

from src.ml.pipeline_builder import (
    build_preprocessor
)

from src.ml.ml_router import (
    run_ml_engine
)

from src.ml.dataset_config import (
    get_available_targets,
    validate_target_column,
    get_class_configuration
)

from src.ml.feature_engineering_analyzer import (
    analyze_feature_engineering
)


# ==========================================
# BUSINESS ANALYTICS IMPORT
# ==========================================

from src.business_analytics.business_engine import (
    run_business_analytics
)


# ==========================================
# DECISION ENGINE IMPORT
# ==========================================

from src.decision_engine.insight_engine import (
    generate_decision_insights
)


# ==========================================
# AI ANALYST IMPORT
# ==========================================

from src.ai_analyst.analyst import (
    run_ai_analyst
)


# ==========================================
# REPORTING IMPORTS
# ==========================================

from src.reporting.report_builder import (
    build_report_data
)

from src.reporting.html_report import (
    generate_html_report
)


# ==========================================
# COMPLETE ANALYSIS SERVICE
# ==========================================

def run_complete_analysis(
    file_path,
    target_column,
    positive_class=None,
    report_output_path=None
):
    """
    Run the complete DataLens AI analysis
    pipeline for a supplied dataset.

    Parameters
    ----------
    file_path:
        Path to the uploaded CSV dataset.

    target_column:
        Column selected as the prediction
        target.

    positive_class:
        Optional positive class for binary
        classification.

        Example:
            "Yes"

        Regression:
            None

    report_output_path:
        Optional custom path for the generated
        HTML report.

    Returns
    -------
    dict
        Structured results containing:

        - dataset information
        - problem type
        - class configuration
        - feature engineering analysis
        - ML results
        - business analytics
        - decision insights
        - AI analysis
        - report data
        - report path
    """

    print("\n================================")
    print("DATALENS AI ANALYSIS SERVICE")
    print("================================")


    # ======================================
    # 1. LOAD DATASET
    # ======================================

    df = load_dataset(
        file_path
    )

    if df is None:

        raise ValueError(
            "Dataset could not be loaded."
        )


    # ======================================
    # 2. VALIDATE DATASET
    # ======================================

    is_valid = validate_dataset(
        df
    )

    if not is_valid:

        raise ValueError(
            "Dataset validation failed."
        )


    # ======================================
    # 3. VALIDATE TARGET
    # ======================================

    available_targets = (
        get_available_targets(
            df
        )
    )

    validate_target_column(
        df,
        target_column
    )


    # ======================================
    # 4. DATA PROFILING
    # ======================================

    print("\n================================")
    print("DATA PROFILING")
    print("================================")

    profile_dataset(
        df
    )

    analyze_missing_values(
        df
    )

    analyze_duplicates(
        df
    )

    analyze_data_types(
        df
    )

    detect_feature_types(
        df
    )

    analyze_cardinality(
        df
    )

    detect_outliers(
        df
    )

    analyze_class_imbalance(
        df
    )

    detect_suspicious_columns(
        df
    )

    calculate_quality_score(
        df
    )


    # ======================================
    # 5. EXPLORATORY DATA ANALYSIS
    # ======================================

    print("\n================================")
    print("EXPLORATORY DATA ANALYSIS")
    print("================================")

    analyze_descriptive_statistics(
        df
    )

    analyze_distributions(
        df
    )

    analyze_correlations(
        df
    )

    generate_numerical_histograms(
        df
    )

    analyze_categorical_features(
        df
    )

    analyze_relationships(
        df
    )

    generate_correlation_heatmap(
        df
    )

    generate_eda_insights(
        df
    )


    # ======================================
    # 6. PROBLEM TYPE DETECTION
    # ======================================

    problem_type = (
        detect_problem_type(
            df,
            target_column
        )
    )


    # ======================================
    # 7. FEATURE / TARGET SEPARATION
    # ======================================

    X, y = (
        separate_features_target(
            df,
            target_column
        )
    )


    # ======================================
    # 8. CLASS CONFIGURATION
    # ======================================

    class_config = (
        get_class_configuration(
            y,
            problem_type,
            positive_class=positive_class
        )
    )

    resolved_positive_class = (
        class_config.get(
            "positive_class"
        )
    )


    # ======================================
    # 9. PREPROCESSING ANALYSIS
    # ======================================

    (
        numerical_features,
        categorical_features

    ) = analyze_preprocessing_requirements(
        X
    )


    # ======================================
    # 10. FEATURE ENGINEERING ANALYSIS
    # ======================================
    #
    # This stage only analyzes the dataset.
    #
    # Actual learned transformations are
    # performed inside the sklearn Pipeline
    # and therefore fitted using training
    # data only.
    # ======================================

    feature_engineering_results = (
        analyze_feature_engineering(
            X
        )
    )


    # ======================================
    # IMPORTANT
    # ======================================
    #
    # We intentionally do NOT call the
    # standalone preprocessing preview
    # functions here.
    #
    # Actual ML preprocessing remains inside
    # the sklearn Pipeline and is fitted only
    # using training data.
    #
    # ======================================


    # ======================================
    # 11. TRAIN / TEST SPLIT
    # ======================================

    (
        X_train,
        X_test,
        y_train,
        y_test

    ) = split_dataset(
        X,
        y
    )


    # ======================================
    # 12. BUILD PREPROCESSOR
    # ======================================

    preprocessor = (
        build_preprocessor(
            numerical_features,
            categorical_features
        )
    )


    # ======================================
    # 13. DYNAMIC ML ENGINE
    # ======================================

    ml_results = (
        run_ml_engine(

            problem_type=
                problem_type,

            preprocessor=
                preprocessor,

            X=
                X,

            y=
                y,

            X_train=
                X_train,

            X_test=
                X_test,

            y_train=
                y_train,

            y_test=
                y_test,

            positive_class=
                resolved_positive_class
        )
    )


    # ======================================
    # 14. BUSINESS ANALYTICS
    # ======================================

    business_results = (
        run_business_analytics(
            df,
            target_column
        )
    )


    # ======================================
    # 15. DECISION / INSIGHT ENGINE
    # ======================================

    decision_results = (
        generate_decision_insights(

            df=df,

            target_column=
                target_column,

            problem_type=
                problem_type,

            ml_results=
                ml_results,

            business_results=
                business_results
        )
    )


    # ======================================
    # 16. AI ANALYST
    # ======================================
    #
    # IMPORTANT:
    #
    # Decision results are intentionally NOT
    # passed to the AI Analyst yet.
    #
    # First we verify that Decision Engine V1
    # works correctly inside the full pipeline.
    # ======================================

    ai_results = (
        run_ai_analyst(

            df=df,

            target_column=
                target_column,

            problem_type=
                problem_type,

            ml_results=
                ml_results,

            business_results=
                business_results
        )
    )


    # ======================================
    # 17. REPORT BUILDER
    # ======================================
    #
    # Decision results are also intentionally
    # not passed into reporting yet.
    #
    # That integration comes after this phase
    # is verified.
    # ======================================

    report_data = build_report_data(
    df=df,
    target_column=target_column,
    problem_type=problem_type,
    ml_results=ml_results,
    business_results=business_results,
    decision_results=decision_results,
    ai_results=ai_results
)


    # ======================================
    # 18. HTML REPORT
    # ======================================

    if report_output_path:

        report_path = (
            generate_html_report(
                report_data,

                output_path=
                    report_output_path
            )
        )

    else:

        report_path = (
            generate_html_report(
                report_data
            )
        )


    # ======================================
    # 19. SERVICE RESPONSE
    # ======================================

    results = {

        "status":
            "success",

        "file_path":
            str(file_path),

        "target_column":
            target_column,

        "available_targets":
            available_targets,

        "problem_type":
            problem_type,

        "positive_class":
            resolved_positive_class,

        "class_configuration":
            class_config,


        # ==================================
        # DATASET SUMMARY
        # ==================================

        "dataset": {

            "rows":
                int(
                    len(df)
                ),

            "columns":
                int(
                    len(
                        df.columns
                    )
                ),

            "column_names":
                df.columns.tolist(),

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
        },


        # ==================================
        # FEATURE CONFIGURATION
        # ==================================

        "feature_configuration": {

            "numerical_features":
                numerical_features,

            "categorical_features":
                categorical_features
        },


        # ==================================
        # FEATURE ENGINEERING
        # ==================================

        "feature_engineering":
            feature_engineering_results,


        # ==================================
        # MACHINE LEARNING
        # ==================================

        "ml_results":
            ml_results,


        # ==================================
        # BUSINESS ANALYTICS
        # ==================================

        "business_results":
            business_results,


        # ==================================
        # DECISION / INSIGHT ENGINE
        # ==================================

        "decision_results":
            decision_results,


        # ==================================
        # AI ANALYST
        # ==================================

        "ai_results":
            ai_results,


        # ==================================
        # REPORT
        # ==================================

        "report_data":
            report_data,

        "report_path":
            report_path
    }


    # ======================================
    # COMPLETE
    # ======================================

    print("\n================================")
    print("ANALYSIS SERVICE COMPLETE")
    print("================================")

    print(
        f"Problem Type: "
        f"{problem_type}"
    )

    print(
        f"Target Column: "
        f"{target_column}"
    )

    print(
        f"Decision Insights: "
        f"{decision_results['summary']['total_insights']}"
    )

    print(
        f"High Priority Insights: "
        f"{decision_results['summary']['high_priority']}"
    )

    print(
        f"Report: "
        f"{report_path}"
    )


    return results