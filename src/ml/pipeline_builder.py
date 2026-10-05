# ==========================================
# DATALENS AI - PREPROCESSING PIPELINE V2
# ==========================================

from sklearn.compose import (
    ColumnTransformer,
    make_column_selector
)

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from src.ml.feature_engineer import (
    DataLensFeatureEngineer
)


def build_preprocessor(
    numerical_features=None,
    categorical_features=None
):
    """
    Build the complete DataLens AI
    preprocessing pipeline.

    Pipeline:

    Raw Features
        ↓
    Feature Engineering
        ↓
    Dynamic Column Detection
        ↓
    Missing Value Handling
        ↓
    Encoding / Scaling

    Feature engineering is fitted inside the
    sklearn Pipeline, so learned transformations
    use training data only.
    """

    print("\n================================")
    print("BUILDING ML PREPROCESSING PIPELINE")
    print("================================")

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================

    feature_engineer = (
        DataLensFeatureEngineer(
            skew_threshold=1.0,
            datetime_parse_threshold=0.90
        )
    )

    # ==========================================
    # NUMERICAL PIPELINE
    # ==========================================

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    # ==========================================
    # CATEGORICAL PIPELINE
    # ==========================================

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    # ==========================================
    # DYNAMIC COLUMN SELECTION
    # ==========================================
    #
    # We intentionally detect feature types
    # AFTER feature engineering.
    #
    # Example:
    #
    # purchase_date
    #
    # becomes:
    #
    # purchase_date__year
    # purchase_date__month
    # purchase_date__day
    # purchase_date__dayofweek
    #
    # Those generated columns are numerical and
    # therefore automatically enter the numeric
    # preprocessing pipeline.
    # ==========================================

    column_preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                make_column_selector(
                    dtype_include="number"
                )
            ),
            (
                "categorical",
                categorical_pipeline,
                make_column_selector(
                    dtype_include=[
                        "object",
                        "string",
                        "category"
                    ]
                )
            )
        ],
        remainder="drop"
    )

    # ==========================================
    # COMPLETE PREPROCESSING PIPELINE
    # ==========================================

    preprocessor = Pipeline(
        steps=[
            (
                "feature_engineering",
                feature_engineer
            ),
            (
                "column_preprocessing",
                column_preprocessor
            )
        ]
    )

    print(
        "✓ Leakage-safe feature engineering configured."
    )

    print(
        "✓ Constant feature removal configured."
    )

    print(
        "✓ Datetime decomposition configured."
    )

    print(
        "✓ Numerical skew transformation configured."
    )

    print(
        "✓ Dynamic numerical feature selection configured."
    )

    print(
        "✓ Numerical median imputation configured."
    )

    print(
        "✓ Numerical StandardScaler configured."
    )

    print(
        "✓ Dynamic categorical feature selection configured."
    )

    print(
        "✓ Categorical imputation configured."
    )

    print(
        "✓ One-Hot Encoding configured."
    )

    print(
        "✓ Complete preprocessing pipeline created."
    )

    return preprocessor