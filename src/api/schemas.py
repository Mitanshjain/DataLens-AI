# ==========================================
# DATALENS AI - API SCHEMAS V3
# ==========================================

from typing import Any

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


# ==========================================
# HEALTH RESPONSE
# ==========================================

class HealthResponse(BaseModel):

    status: str

    application: str


# ==========================================
# DATASET UPLOAD RESPONSE
# ==========================================

class DatasetUploadResponse(BaseModel):

    status: str

    dataset_id: str

    filename: str

    rows: int

    columns: int

    column_names: list[str]


# ==========================================
# DATASET INFORMATION RESPONSE
# ==========================================

class DatasetInfoResponse(BaseModel):

    status: str

    dataset_id: str

    filename: str

    rows: int

    columns: int

    column_names: list[str]


# ==========================================
# ANALYSIS REQUEST
# ==========================================

class AnalysisRequest(BaseModel):
    """
    Request used to start a DataLens
    analysis.
    """

    dataset_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    target_column: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    positive_class: Any | None = None


    # --------------------------------------
    # CLEAN DATASET ID
    # --------------------------------------

    @field_validator(
        "dataset_id"
    )
    @classmethod
    def validate_dataset_id_text(
        cls,
        value: str
    ) -> str:

        cleaned_value = (
            value.strip()
        )

        if not cleaned_value:

            raise ValueError(
                "dataset_id cannot be empty."
            )

        return cleaned_value


    # --------------------------------------
    # CLEAN TARGET COLUMN
    # --------------------------------------

    @field_validator(
        "target_column"
    )
    @classmethod
    def validate_target_column_text(
        cls,
        value: str
    ) -> str:

        cleaned_value = (
            value.strip()
        )

        if not cleaned_value:

            raise ValueError(
                "target_column cannot be empty."
            )

        return cleaned_value


# ==========================================
# DATASET SUMMARY
# ==========================================

class DatasetSummary(BaseModel):

    rows: int

    columns: int

    missing_values: int

    duplicate_rows: int


# ==========================================
# DASHBOARD SUMMARY
# ==========================================

class DashboardSummary(BaseModel):
    """
    Safe presentation-oriented results
    for the frontend dashboard.

    Detailed technical results remain
    inside the analysis engine and
    generated report.
    """

    evaluation: Any | None = None

    class_performance: Any | None = None

    model_comparison: Any | None = None

    cross_validation: Any | None = None

    explainability: Any | None = None

    business_kpis: Any | None = None

    business_findings: Any | None = None

    ai_analysis: str | None = None


# ==========================================
# ANALYSIS RESPONSE
# ==========================================

class AnalysisResponse(BaseModel):

    status: str

    analysis_id: str

    dataset_id: str

    target_column: str

    problem_type: str

    positive_class: Any | None = None

    dataset_summary: DatasetSummary

    dashboard: DashboardSummary

    report_url: str


# ==========================================
# ANALYSIS HISTORY ITEM
# ==========================================

class AnalysisHistoryItem(BaseModel):
    """
    One previously completed DataLens
    analysis stored in the database.
    """

    analysis_id: str

    dataset_id: str

    original_filename: str | None = None

    target_column: str

    problem_type: str

    positive_class: str | None = None

    rows: int

    columns: int

    missing_values: int

    duplicate_rows: int

    created_at: str

    report_url: str


# ==========================================
# ANALYSIS HISTORY RESPONSE
# ==========================================

class AnalysisHistoryResponse(BaseModel):
    """
    Response returned when requesting
    previous DataLens analyses.
    """

    status: str

    total: int

    analyses: list[
        AnalysisHistoryItem
    ]