# ==========================================
# DATALENS AI - API ROUTES V3
# ==========================================

import logging

from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from fastapi.responses import FileResponse


from src.api.schemas import (
    HealthResponse,
    DatasetUploadResponse,
    DatasetInfoResponse,
    AnalysisRequest,
    AnalysisResponse,
    AnalysisHistoryResponse,
)


from src.services.dataset_service import (
    save_uploaded_dataset,
    get_dataset_info,
    get_dataset_path,
    get_dataset_metadata,
)


from src.services.analysis_service import (
    run_complete_analysis,
)


from src.database.analysis_repository import (
    save_analysis,
    get_analysis,
    get_analysis_history,
)


# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger(
    __name__
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter()


# ==========================================
# REPORT DIRECTORY
# ==========================================

REPORT_DIRECTORY = Path(
    "reports/generated"
)

REPORT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================
# JSON SAFE CONVERTER
# ==========================================

def make_json_safe(value):
    """
    Convert common Pandas / NumPy objects
    into JSON-safe Python values.

    Only intentionally exposed dashboard
    values should pass through this helper.
    """

    if value is None:

        return None


    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
        )
    ):

        return value


    if isinstance(
        value,
        np.generic
    ):

        return value.item()


    if isinstance(
        value,
        np.ndarray
    ):

        return value.tolist()


    if isinstance(
        value,
        pd.DataFrame
    ):

        return make_json_safe(
            value.to_dict(
                orient="records"
            )
        )


    if isinstance(
        value,
        pd.Series
    ):

        return make_json_safe(
            value.to_dict()
        )


    if isinstance(
        value,
        dict
    ):

        return {
            str(key):
                make_json_safe(item)

            for key, item
            in value.items()
        }


    if isinstance(
        value,
        (list, tuple, set)
    ):

        return [
            make_json_safe(item)
            for item in value
        ]


    return str(value)


# ==========================================
# BUILD DASHBOARD DATA
# ==========================================

def build_dashboard_data(
    results
):
    """
    Build a safe, presentation-oriented
    dashboard response.

    Model objects, raw predictions and other
    internal ML objects are intentionally
    excluded.
    """

    ml_results = (
        results.get(
            "ml_results",
            {}
        )
        or {}
    )


    business_results = (
        results.get(
            "business_results",
            {}
        )
        or {}
    )


    ai_results = (
        results.get(
            "ai_results",
            {}
        )
        or {}
    )


    # --------------------------------------
    # ML RESULTS
    # --------------------------------------

    evaluation = (
        ml_results.get(
            "evaluation"
        )
    )

    class_performance = (
        ml_results.get(
            "class_performance"
        )
    )

    model_comparison = (
        ml_results.get(
            "model_comparison"
        )
    )

    cross_validation = (
        ml_results.get(
            "cross_validation"
        )
    )

    explainability = (
        ml_results.get(
            "explainability"
        )
    )


    # --------------------------------------
    # BUSINESS ANALYTICS
    # --------------------------------------

    business_kpis = (
        business_results.get(
            "kpis"
        )
    )

    business_findings = (
        business_results.get(
            "findings"
        )
    )


    # --------------------------------------
    # AI ANALYST
    # --------------------------------------

    ai_analysis = (
        ai_results.get(
            "analysis"
        )
    )


    # --------------------------------------
    # SAFE DASHBOARD OUTPUT
    # --------------------------------------

    return {

        "evaluation":
            make_json_safe(
                evaluation
            ),

        "class_performance":
            make_json_safe(
                class_performance
            ),

        "model_comparison":
            make_json_safe(
                model_comparison
            ),

        "cross_validation":
            make_json_safe(
                cross_validation
            ),

        "explainability":
            make_json_safe(
                explainability
            ),

        "business_kpis":
            make_json_safe(
                business_kpis
            ),

        "business_findings":
            make_json_safe(
                business_findings
            ),

        "ai_analysis":
            make_json_safe(
                ai_analysis
            ),
    }


# ==========================================
# INTERNAL ERROR HELPER
# ==========================================

def raise_internal_server_error(
    operation: str,
    error: Exception
):
    """
    Log the real internal exception while
    returning a safe generic message to
    the API client.
    """

    logger.exception(
        "DataLens API failure during %s",
        operation,
        exc_info=error,
    )


    raise HTTPException(
        status_code=500,
        detail=(
            "An internal server error occurred. "
            "Please try again."
        ),
    ) from error


# ==========================================
# HEALTH CHECK
# ==========================================

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check():
    """
    Verify that the API process is running.
    """

    return {
        "status": "ok",
        "application": "DataLens AI",
    }


# ==========================================
# UPLOAD DATASET
# ==========================================

@router.post(
    "/upload",
    response_model=DatasetUploadResponse,
)
async def upload_dataset(
    file: UploadFile = File(...)
):
    """
    Upload and validate a CSV dataset.
    """

    try:

        dataset_info = (
            await save_uploaded_dataset(
                file
            )
        )


        return {

            "status":
                "success",

            "dataset_id":
                dataset_info[
                    "dataset_id"
                ],

            "filename":
                dataset_info[
                    "filename"
                ],

            "rows":
                dataset_info[
                    "rows"
                ],

            "columns":
                dataset_info[
                    "columns"
                ],

            "column_names":
                dataset_info[
                    "column_names"
                ],
        }


    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


    except Exception as error:

        raise_internal_server_error(
            "dataset upload",
            error,
        )


# ==========================================
# GET DATASET INFORMATION
# ==========================================

@router.get(
    "/dataset/{dataset_id}",
    response_model=DatasetInfoResponse,
)
def dataset_information(
    dataset_id: str
):
    """
    Return information about a previously
    uploaded dataset.
    """

    try:

        dataset_info = (
            get_dataset_info(
                dataset_id
            )
        )


        return {

            "status":
                "success",

            "dataset_id":
                dataset_info[
                    "dataset_id"
                ],

            "filename":
                dataset_info[
                    "filename"
                ],

            "rows":
                dataset_info[
                    "rows"
                ],

            "columns":
                dataset_info[
                    "columns"
                ],

            "column_names":
                dataset_info[
                    "column_names"
                ],
        }


    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error


    except Exception as error:

        raise_internal_server_error(
            "dataset information retrieval",
            error,
        )


# ==========================================
# RUN COMPLETE ANALYSIS
# ==========================================

@router.post(
    "/analyze",
    response_model=AnalysisResponse,
)
def analyze_dataset(
    request: AnalysisRequest
):
    """
    Run the complete DataLens analysis
    pipeline for an uploaded dataset.
    """

    try:

        # ----------------------------------
        # RESOLVE UPLOADED DATASET
        # ----------------------------------

        file_path = (
            get_dataset_path(
                request.dataset_id
            )
        )


        # ----------------------------------
        # GENERATE ANALYSIS ID
        # ----------------------------------

        analysis_id = str(
            uuid4()
        )


        # ----------------------------------
        # UNIQUE REPORT PATH
        # ----------------------------------

        report_output_path = (
            REPORT_DIRECTORY
            / f"{analysis_id}.html"
        )


        # ----------------------------------
        # RUN COMPLETE PIPELINE
        # ----------------------------------

        results = (
            run_complete_analysis(

                file_path=
                    str(file_path),

                target_column=
                    request.target_column,

                positive_class=
                    request.positive_class,

                report_output_path=
                    str(
                        report_output_path
                    ),
            )
        )


        # ----------------------------------
        # DASHBOARD-SAFE RESULTS
        # ----------------------------------

        dashboard_data = (
            build_dashboard_data(
                results
            )
        )


        # ----------------------------------
        # DATASET SUMMARY
        # ----------------------------------

        dataset_results = (
            results[
                "dataset"
            ]
        )


        dataset_summary = {

            "rows":
                int(
                    dataset_results[
                        "rows"
                    ]
                ),

            "columns":
                int(
                    dataset_results[
                        "columns"
                    ]
                ),

            "missing_values":
                int(
                    dataset_results[
                        "missing_values"
                    ]
                ),

            "duplicate_rows":
                int(
                    dataset_results[
                        "duplicate_rows"
                    ]
                ),
        }


        # ----------------------------------
        # DATASET METADATA
        # ----------------------------------

        dataset_metadata = (
            get_dataset_metadata(
                request.dataset_id
            )
        )


        # ----------------------------------
        # PERSIST COMPLETED ANALYSIS
        # ----------------------------------

        save_analysis(

            analysis_id=
                analysis_id,

            dataset_id=
                request.dataset_id,

            original_filename=
                dataset_metadata.get(
                    "filename"
                ),

            target_column=
                results[
                    "target_column"
                ],

            problem_type=
                results[
                    "problem_type"
                ],

            positive_class=
                results[
                    "positive_class"
                ],

            rows=
                dataset_summary[
                    "rows"
                ],

            columns=
                dataset_summary[
                    "columns"
                ],

            missing_values=
                dataset_summary[
                    "missing_values"
                ],

            duplicate_rows=
                dataset_summary[
                    "duplicate_rows"
                ],

            report_path=
                str(
                    report_output_path
                ),
        )


        # ----------------------------------
        # API RESPONSE
        # ----------------------------------

        return {

            "status":
                "success",

            "analysis_id":
                analysis_id,

            "dataset_id":
                request.dataset_id,

            "target_column":
                results[
                    "target_column"
                ],

            "problem_type":
                results[
                    "problem_type"
                ],

            "positive_class":
                results[
                    "positive_class"
                ],

            "dataset_summary":
                dataset_summary,

            "dashboard":
                dashboard_data,

            "report_url":
                (
                    f"/api/report/"
                    f"{analysis_id}"
                ),
        }


    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error


    except Exception as error:

        raise_internal_server_error(
            "dataset analysis",
            error,
        )


# ==========================================
# GET ANALYSIS HISTORY
# ==========================================

@router.get(
    "/analyses",
    response_model=AnalysisHistoryResponse,
)
def analysis_history():
    """
    Return previously completed analyses.
    """

    try:

        records = (
            get_analysis_history()
        )


        analyses = []


        for record in records:

            analyses.append(
                {

                    "analysis_id":
                        record[
                            "analysis_id"
                        ],

                    "dataset_id":
                        record[
                            "dataset_id"
                        ],

                    "original_filename":
                        record[
                            "original_filename"
                        ],

                    "target_column":
                        record[
                            "target_column"
                        ],

                    "problem_type":
                        record[
                            "problem_type"
                        ],

                    "positive_class":
                        record[
                            "positive_class"
                        ],

                    "rows":
                        record[
                            "rows"
                        ],

                    "columns":
                        record[
                            "columns"
                        ],

                    "missing_values":
                        record[
                            "missing_values"
                        ],

                    "duplicate_rows":
                        record[
                            "duplicate_rows"
                        ],

                    "created_at":
                        record[
                            "created_at"
                        ],

                    "report_url":
                        (
                            f"/api/report/"
                            f"{record['analysis_id']}"
                        ),
                }
            )


        return {
            "status":
                "success",

            "total":
                len(analyses),

            "analyses":
                analyses,
        }


    except Exception as error:

        raise_internal_server_error(
            "analysis history retrieval",
            error,
        )


# ==========================================
# GET GENERATED REPORT
# ==========================================

@router.get(
    "/report/{analysis_id}"
)
def get_analysis_report(
    analysis_id: str
):
    """
    Return the generated HTML report for a
    completed analysis.
    """

    try:

        cleaned_analysis_id = (
            analysis_id.strip()
        )


        if not cleaned_analysis_id:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Analysis ID cannot be empty."
                ),
            )


        analysis = (
            get_analysis(
                cleaned_analysis_id
            )
        )


        if analysis is None:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Analysis was not found."
                ),
            )


        report_path = Path(
            analysis[
                "report_path"
            ]
        )


        if not report_path.exists():

            raise HTTPException(
                status_code=404,
                detail=(
                    "Analysis report "
                    "was not found."
                ),
            )


        if not report_path.is_file():

            raise HTTPException(
                status_code=404,
                detail=(
                    "Analysis report "
                    "is not a valid file."
                ),
            )


        return FileResponse(
    path=report_path,
    media_type="text/html",
    content_disposition_type="inline",
)


    except HTTPException:

        raise


    except Exception as error:

        raise_internal_server_error(
            "report retrieval",
            error,
        )