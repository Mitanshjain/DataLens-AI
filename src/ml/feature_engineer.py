# ==========================================
# DATALENS AI - FEATURE ENGINEER V1
# ==========================================

import numpy as np
import pandas as pd

from sklearn.base import (
    BaseEstimator,
    TransformerMixin
)


class DataLensFeatureEngineer(
    BaseEstimator,
    TransformerMixin
):
    """
    Leakage-safe automatic feature engineering
    transformer for DataLens AI.

    Current V1 responsibilities:

    1. Remove constant features.
    2. Detect datetime-like features.
    3. Decompose datetime features.
    4. Apply safe signed-log transformation
       to strongly skewed numerical features.

    All decisions are learned during fit().
    Therefore, when this transformer is inside
    an sklearn Pipeline, test data does not
    influence learned feature-engineering
    decisions.
    """

    def __init__(
        self,
        skew_threshold=1.0,
        datetime_parse_threshold=0.90
    ):

        self.skew_threshold = (
            skew_threshold
        )

        self.datetime_parse_threshold = (
            datetime_parse_threshold
        )

    # ==========================================
    # FIT
    # ==========================================

    def fit(
        self,
        X,
        y=None
    ):

        X = self._ensure_dataframe(X)

        self.input_features_ = (
            X.columns.tolist()
        )

        self.constant_features_ = []

        self.datetime_features_ = []

        self.skewed_features_ = []

        # --------------------------------------
        # CONSTANT FEATURES
        # --------------------------------------

        for column in X.columns:

            unique_count = (
                X[column]
                .dropna()
                .nunique()
            )

            if unique_count <= 1:

                self.constant_features_.append(
                    column
                )

        # --------------------------------------
        # DATETIME FEATURES
        # --------------------------------------

        for column in X.columns:

            if (
                column
                in self.constant_features_
            ):
                continue

            series = X[column]

            if (
                pd.api.types
                .is_datetime64_any_dtype(
                    series
                )
            ):

                self.datetime_features_.append(
                    column
                )

                continue

            if not (
                pd.api.types
                .is_object_dtype(series)
                or pd.api.types
                .is_string_dtype(series)
            ):
                continue

            sample = (
                series
                .dropna()
                .astype(str)
                .head(100)
            )

            if sample.empty:
                continue

            parsed = pd.to_datetime(
                sample,
                errors="coerce"
            )

            parse_ratio = float(
                parsed.notna().mean()
            )

            if (
                parse_ratio
                >= self.datetime_parse_threshold
            ):

                self.datetime_features_.append(
                    column
                )

        # --------------------------------------
        # SKEWED NUMERICAL FEATURES
        # --------------------------------------

        numerical_features = (
            X.select_dtypes(
                include="number"
            )
            .columns
            .tolist()
        )

        for column in numerical_features:

            if (
                column
                in self.constant_features_
            ):
                continue

            values = (
                X[column]
                .dropna()
            )

            if len(values) < 3:
                continue

            skewness = values.skew()

            if pd.isna(skewness):
                continue

            if (
                abs(float(skewness))
                >= self.skew_threshold
            ):

                self.skewed_features_.append(
                    column
                )

        return self

    # ==========================================
    # TRANSFORM
    # ==========================================

    def transform(
        self,
        X
    ):

        X = self._ensure_dataframe(
            X
        ).copy()

        # --------------------------------------
        # REMOVE CONSTANT FEATURES
        # --------------------------------------

        columns_to_drop = [
            column
            for column
            in self.constant_features_
            if column in X.columns
        ]

        if columns_to_drop:

            X = X.drop(
                columns=columns_to_drop
            )

        # --------------------------------------
        # DATETIME DECOMPOSITION
        # --------------------------------------

        for column in self.datetime_features_:

            if column not in X.columns:
                continue

            parsed = pd.to_datetime(
                X[column],
                errors="coerce"
            )

            X[
                f"{column}__year"
            ] = parsed.dt.year

            X[
                f"{column}__month"
            ] = parsed.dt.month

            X[
                f"{column}__day"
            ] = parsed.dt.day

            X[
                f"{column}__dayofweek"
            ] = parsed.dt.dayofweek

            X = X.drop(
                columns=[column]
            )

        # --------------------------------------
        # SAFE SKEW TRANSFORMATION
        # --------------------------------------
        #
        # signed log1p:
        #
        # positive values remain positive
        # negative values remain negative
        #
        # This means we do not require every
        # value to be > 0.
        # --------------------------------------

        for column in self.skewed_features_:

            if column not in X.columns:
                continue

            numeric_values = pd.to_numeric(
                X[column],
                errors="coerce"
            )

            X[column] = (
                np.sign(numeric_values)
                * np.log1p(
                    np.abs(
                        numeric_values
                    )
                )
            )

        return X

    # ==========================================
    # FEATURE NAMES
    # ==========================================

    def get_feature_names_out(
        self,
        input_features=None
    ):

        if not hasattr(
            self,
            "input_features_"
        ):

            raise RuntimeError(
                "Feature engineer must be "
                "fitted before requesting "
                "feature names."
            )

        features = []

        for column in self.input_features_:

            if (
                column
                in self.constant_features_
            ):
                continue

            if (
                column
                in self.datetime_features_
            ):

                features.extend(
                    [
                        f"{column}__year",
                        f"{column}__month",
                        f"{column}__day",
                        f"{column}__dayofweek"
                    ]
                )

            else:

                features.append(
                    column
                )

        return np.asarray(
            features,
            dtype=object
        )

    # ==========================================
    # DATAFRAME HELPER
    # ==========================================

    def _ensure_dataframe(
        self,
        X
    ):

        if isinstance(
            X,
            pd.DataFrame
        ):

            return X

        if hasattr(
            self,
            "input_features_"
        ):

            return pd.DataFrame(
                X,
                columns=
                    self.input_features_
            )

        return pd.DataFrame(X)