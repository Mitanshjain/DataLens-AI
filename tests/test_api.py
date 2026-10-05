# ==========================================
# DATALENS AI - API TESTS
# ==========================================

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from fastapi.testclient import TestClient

from src.api.app import app
import src.api.routes as routes


# ==========================================
# CLIENT
# ==========================================

client = TestClient(app)


# ==========================================
# ROOT ENDPOINT
# ==========================================

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "DataLens AI"
    assert data["status"] == "running"
    assert data["version"] == "1.1.0"
    assert data["documentation"] == "/docs"
    assert data["health"] == "/api/health"


# ==========================================
# HEALTH ENDPOINT
# ==========================================

def test_health_endpoint():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "application": "DataLens AI",
    }


# ==========================================
# ANALYSIS REQUEST VALIDATION
# ==========================================

def test_analyze_rejects_blank_dataset_id():

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id": "   ",
            "target_column": "target",
        },
    )

    assert response.status_code == 422


def test_analyze_rejects_blank_target_column():

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id": "dataset-123",
            "target_column": "   ",
        },
    )

    assert response.status_code == 422


def test_analyze_rejects_missing_dataset_id():

    response = client.post(
        "/api/analyze",
        json={
            "target_column": "target",
        },
    )

    assert response.status_code == 422


def test_analyze_rejects_missing_target_column():

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id": "dataset-123",
        },
    )

    assert response.status_code == 422


# ==========================================
# DATASET INFORMATION
# ==========================================

def test_dataset_information_success(
    monkeypatch,
):

    def fake_get_dataset_info(
        dataset_id,
    ):
        return {
            "dataset_id": dataset_id,
            "filename": "customers.csv",
            "rows": 100,
            "columns": 4,
            "column_names": [
                "age",
                "city",
                "income",
                "purchased",
            ],
        }

    monkeypatch.setattr(
        routes,
        "get_dataset_info",
        fake_get_dataset_info,
    )

    response = client.get(
        "/api/dataset/dataset-123"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["dataset_id"] == "dataset-123"
    assert data["filename"] == "customers.csv"
    assert data["rows"] == 100
    assert data["columns"] == 4

    assert data["column_names"] == [
        "age",
        "city",
        "income",
        "purchased",
    ]


def test_dataset_information_not_found(
    monkeypatch,
):

    def fake_get_dataset_info(
        dataset_id,
    ):
        raise FileNotFoundError(
            "Dataset was not found."
        )

    monkeypatch.setattr(
        routes,
        "get_dataset_info",
        fake_get_dataset_info,
    )

    response = client.get(
        "/api/dataset/missing-dataset"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Dataset was not found."
    )


def test_dataset_information_value_error(
    monkeypatch,
):

    def fake_get_dataset_info(
        dataset_id,
    ):
        raise ValueError(
            "Invalid dataset ID."
        )

    monkeypatch.setattr(
        routes,
        "get_dataset_info",
        fake_get_dataset_info,
    )

    response = client.get(
        "/api/dataset/bad-dataset"
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Invalid dataset ID."
    )


# ==========================================
# JSON SAFE CONVERTER
# ==========================================

def test_make_json_safe_numpy_values():

    value = {
        "integer": np.int64(10),
        "float": np.float64(2.5),
        "array": np.array(
            [1, 2, 3]
        ),
    }

    result = routes.make_json_safe(
        value
    )

    assert result == {
        "integer": 10,
        "float": 2.5,
        "array": [1, 2, 3],
    }


def test_make_json_safe_dataframe():

    df = pd.DataFrame({
        "model": [
            "A",
            "B",
        ],
        "score": [
            0.8,
            0.9,
        ],
    })

    result = routes.make_json_safe(
        df
    )

    assert result == [
        {
            "model": "A",
            "score": 0.8,
        },
        {
            "model": "B",
            "score": 0.9,
        },
    ]


# ==========================================
# DASHBOARD DATA
# ==========================================

def test_build_dashboard_data():

    results = {
        "ml_results": {
            "evaluation": {
                "accuracy":
                    np.float64(0.90)
            },
            "class_performance": None,
            "model_comparison":
                pd.DataFrame({
                    "Model": ["A"],
                    "Score": [0.90],
                }),
            "cross_validation": None,
            "explainability": {
                "importance":
                    np.array(
                        [0.7, 0.3]
                    )
            },
        },
        "business_results": {
            "kpis": {
                "customers":
                    np.int64(100)
            },
            "findings": [
                "Finding 1"
            ],
        },
        "ai_results": {
            "analysis":
                "AI summary"
        },
    }

    result = (
        routes.build_dashboard_data(
            results
        )
    )

    assert result[
        "evaluation"
    ]["accuracy"] == 0.90

    assert result[
        "model_comparison"
    ] == [
        {
            "Model": "A",
            "Score": 0.90,
        }
    ]

    assert result[
        "explainability"
    ]["importance"] == [
        0.7,
        0.3,
    ]

    assert result[
        "business_kpis"
    ]["customers"] == 100

    assert result[
        "business_findings"
    ] == [
        "Finding 1"
    ]

    assert (
        result["ai_analysis"]
        == "AI summary"
    )


# ==========================================
# ANALYZE DATASET - SUCCESS
# ==========================================

def test_analyze_dataset_success(
    monkeypatch,
):

    monkeypatch.setattr(
        routes,
        "get_dataset_path",
        lambda dataset_id:
            Path("fake_dataset.csv"),
    )

    monkeypatch.setattr(
        routes,
        "get_dataset_metadata",
        lambda dataset_id: {
            "filename":
                "customers.csv"
        },
    )

    fake_results = {
        "target_column":
            "purchased",

        "problem_type":
            "Classification",

        "positive_class":
            "Yes",

        "dataset": {
            "rows": 100,
            "columns": 4,
            "missing_values": 2,
            "duplicate_rows": 1,
        },

        "ml_results": {
            "evaluation": {
                "accuracy": 0.90
            },
            "class_performance": None,
            "model_comparison": None,
            "cross_validation": None,
            "explainability": None,
        },

        "business_results": {
            "kpis": None,
            "findings": None,
        },

        "ai_results": {
            "analysis":
                "Test AI analysis"
        },
    }

    def fake_run_complete_analysis(
        file_path,
        target_column,
        positive_class,
        report_output_path,
    ):
        return fake_results

    monkeypatch.setattr(
        routes,
        "run_complete_analysis",
        fake_run_complete_analysis,
    )

    saved_analysis = {}

    def fake_save_analysis(
        **kwargs,
    ):
        saved_analysis.update(
            kwargs
        )

    monkeypatch.setattr(
        routes,
        "save_analysis",
        fake_save_analysis,
    )

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id":
                "dataset-123",
            "target_column":
                "purchased",
            "positive_class":
                "Yes",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert (
        data["dataset_id"]
        == "dataset-123"
    )

    assert (
        data["target_column"]
        == "purchased"
    )

    assert (
        data["problem_type"]
        == "Classification"
    )

    assert (
        data["positive_class"]
        == "Yes"
    )

    assert data[
        "dataset_summary"
    ] == {
        "rows": 100,
        "columns": 4,
        "missing_values": 2,
        "duplicate_rows": 1,
    }

    assert (
        data["dashboard"]
        ["evaluation"]
        ["accuracy"]
        == 0.90
    )

    assert data[
        "report_url"
    ].startswith(
        "/api/report/"
    )

    assert saved_analysis[
        "dataset_id"
    ] == "dataset-123"

    assert saved_analysis[
        "original_filename"
    ] == "customers.csv"

    assert saved_analysis[
        "target_column"
    ] == "purchased"


# ==========================================
# ANALYZE DATASET - NOT FOUND
# ==========================================

def test_analyze_dataset_not_found(
    monkeypatch,
):

    def fake_get_dataset_path(
        dataset_id,
    ):
        raise FileNotFoundError(
            "Dataset was not found."
        )

    monkeypatch.setattr(
        routes,
        "get_dataset_path",
        fake_get_dataset_path,
    )

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id":
                "missing-dataset",
            "target_column":
                "target",
        },
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Dataset was not found."
    )


# ==========================================
# ANALYZE DATASET - VALUE ERROR
# ==========================================

def test_analyze_dataset_value_error(
    monkeypatch,
):

    monkeypatch.setattr(
        routes,
        "get_dataset_path",
        lambda dataset_id:
            Path("fake.csv"),
    )

    def fake_analysis(
        **kwargs,
    ):
        raise ValueError(
            "Target is invalid."
        )

    monkeypatch.setattr(
        routes,
        "run_complete_analysis",
        fake_analysis,
    )

    response = client.post(
        "/api/analyze",
        json={
            "dataset_id":
                "dataset-123",
            "target_column":
                "bad-target",
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Target is invalid."
    )


# ==========================================
# ANALYSIS HISTORY
# ==========================================

def test_analysis_history_success(
    monkeypatch,
):

    fake_records = [
        {
            "analysis_id":
                "analysis-1",

            "dataset_id":
                "dataset-1",

            "original_filename":
                "customers.csv",

            "target_column":
                "purchased",

            "problem_type":
                "Classification",

            "positive_class":
                "Yes",

            "rows": 100,

            "columns": 4,

            "missing_values": 2,

            "duplicate_rows": 1,

            "created_at":
                "2026-10-05 10:00:00",
        }
    ]

    monkeypatch.setattr(
        routes,
        "get_analysis_history",
        lambda: fake_records,
    )

    response = client.get(
        "/api/analyses"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["total"] == 1

    analysis = data[
        "analyses"
    ][0]

    assert (
        analysis["analysis_id"]
        == "analysis-1"
    )

    assert (
        analysis["report_url"]
        == "/api/report/analysis-1"
    )


def test_analysis_history_empty(
    monkeypatch,
):

    monkeypatch.setattr(
        routes,
        "get_analysis_history",
        lambda: [],
    )

    response = client.get(
        "/api/analyses"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "success",
        "total": 0,
        "analyses": [],
    }


# ==========================================
# REPORT - ANALYSIS NOT FOUND
# ==========================================

def test_report_analysis_not_found(
    monkeypatch,
):

    monkeypatch.setattr(
        routes,
        "get_analysis",
        lambda analysis_id: None,
    )

    response = client.get(
        "/api/report/missing-analysis"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Analysis was not found."
    )


# ==========================================
# REPORT FILE MISSING
# ==========================================

def test_report_file_not_found(
    monkeypatch,
    tmp_path,
):

    missing_report = (
        tmp_path
        / "missing-report.html"
    )

    monkeypatch.setattr(
        routes,
        "get_analysis",
        lambda analysis_id: {
            "report_path":
                str(missing_report)
        },
    )

    response = client.get(
        "/api/report/analysis-123"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Analysis report was not found."
    )


# ==========================================
# REPORT SUCCESS
# ==========================================

def test_report_success(
    monkeypatch,
    tmp_path,
):

    report_file = (
        tmp_path
        / "report.html"
    )

    report_file.write_text(
        (
            "<html>"
            "<body>"
            "<h1>DataLens AI Report</h1>"
            "</body>"
            "</html>"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        routes,
        "get_analysis",
        lambda analysis_id: {
            "report_path":
                str(report_file)
        },
    )

    response = client.get(
        "/api/report/analysis-123"
    )

    assert response.status_code == 200

    assert (
        "text/html"
        in response.headers[
            "content-type"
        ]
    )

    assert (
        "DataLens AI Report"
        in response.text
    )


# ==========================================
# SAFE INTERNAL ERROR
# ==========================================

def test_dataset_information_internal_error_is_safe(
    monkeypatch,
):

    def fake_get_dataset_info(
        dataset_id,
    ):
        raise RuntimeError(
            "Sensitive internal details"
        )

    monkeypatch.setattr(
        routes,
        "get_dataset_info",
        fake_get_dataset_info,
    )

    response = client.get(
        "/api/dataset/dataset-123"
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": (
            "An internal server error occurred. "
            "Please try again."
        )
    }

    assert (
        "Sensitive internal details"
        not in response.text
    )