# DataLens AI

### Intelligent Data Science & Business Analytics Platform

DataLens AI is an end-to-end data science and business analytics platform that transforms raw CSV datasets into structured data profiles, exploratory analysis, machine learning results, model diagnostics, explainability insights, business findings, decision-oriented insights, AI-generated analysis, and professional HTML reports.

The platform is designed to bridge the gap between **technical machine learning outputs and business decision-making**.

Instead of only training a model, DataLens AI builds a complete analytical workflow:

**Dataset → Data Profiling → EDA → Feature Engineering → Machine Learning → Diagnostics → Explainability → Business Analytics → Decision Insights → AI Analyst → Dashboard & Report**

---

## Why DataLens AI?

Traditional machine learning projects often stop after model training and evaluation.

DataLens AI goes further by combining:

- Automated data profiling
- Exploratory data analysis
- Dynamic ML problem detection
- Classification and regression workflows
- Feature engineering
- Model comparison
- Cross-validation
- Model diagnostics
- Explainability
- Business KPI analysis
- Segment analysis
- Deterministic decision insights
- LLM-powered analytical explanations
- Interactive frontend dashboard
- Professional standalone HTML reports
- Analysis history
- Automated backend testing

The goal is to create a system that behaves more like a lightweight **data analyst + data scientist + business analyst platform** rather than a single ML notebook.

---

# Core Capabilities

## 1. Dataset Upload & Validation

Users can upload CSV datasets through the web interface.

The backend validates the dataset before analysis and provides:

- Row and column information
- Available columns
- Missing-value information
- Duplicate detection
- Feature-type analysis
- Cardinality analysis
- Suspicious-column detection
- Outlier analysis
- Dataset quality information

Uploaded datasets are assigned unique dataset IDs for subsequent analysis.

---

## 2. Automated Data Profiling

The profiling engine examines the structure and quality of the dataset before machine learning begins.

The profiler includes modules for:

- Data types
- Missing values
- Duplicate rows
- Cardinality
- Feature types
- Outliers
- Class imbalance
- Suspicious columns
- Dataset validation
- Data quality scoring

This allows DataLens AI to understand the dataset before building predictive models.

---

## 3. Exploratory Data Analysis

DataLens AI performs automated exploratory analysis using dedicated EDA modules.

Analysis includes:

- Descriptive statistics
- Numerical distributions
- Categorical analysis
- Correlation analysis
- Feature relationships
- Automated statistical insights
- Data visualizations

Generated visualizations can include numerical histograms and correlation heatmaps.

---

## 4. Dynamic ML Problem Detection

The platform automatically determines whether the selected target represents a:

- **Classification problem**
- **Regression problem**

The detection logic considers the target's:

- Data type
- Number of unique values
- Integer-like behavior
- Numeric range
- Missing values

This enables the same platform to work with different datasets without manually configuring the ML problem type.

---

## 5. Feature & Target Preparation

Before model training, DataLens AI:

- Separates features and target
- Removes rows with missing target values
- Preserves missing feature values for preprocessing
- Detects obvious identifier columns
- Removes identifier fields from ML features
- Verifies feature/target alignment
- Validates target variability

Identifier detection intentionally uses conservative name-based rules so useful high-cardinality features are not automatically discarded.

---

## 6. Dynamic Preprocessing

The preprocessing layer analyzes the dataset and prepares numerical and categorical features for machine learning.

Depending on the dataset, preprocessing can include:

- Numerical missing-value handling
- Categorical missing-value handling
- Categorical encoding
- Feature transformation
- Leakage-safe preprocessing pipelines

Preprocessing is integrated into machine learning pipelines so transformations are learned from training data rather than leaking information from test data.

---

## 7. Feature Engineering

DataLens AI contains a dedicated feature engineering layer.

The feature engineering system can analyze:

- Skewed numerical variables
- Constant features
- Near-constant features
- High-cardinality features
- Datetime-like features

The feature engineering pipeline can perform transformations such as:

- Datetime decomposition
- Signed `log1p` transformations for skewed variables
- Removal of constant features

Preprocessing requirements are recalculated after feature engineering.

---

# Machine Learning Engine

DataLens AI dynamically routes analysis to classification or regression workflows.

## Classification

The classification engine supports model training and comparison using algorithms such as:

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors

Classification analysis includes:

- Model training
- Predictions
- Evaluation metrics
- Class-level performance
- Model comparison
- Cross-validation
- Class imbalance handling
- Classification diagnostics

### Classification Metrics

Depending on the analysis, metrics can include:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Precision-Recall metrics
- Average Precision

---

## Regression

For continuous targets, DataLens AI routes the dataset through its regression engine.

Regression analysis includes:

- Model training
- Prediction
- Evaluation
- Model comparison
- Regression diagnostics
- Residual analysis

Regression diagnostics help evaluate not only predictive accuracy but also the model's error behavior.

---

# Cross-Validation

Classification models are compared using stratified K-fold cross-validation.

The cross-validation engine evaluates:

- Accuracy
- Weighted Precision
- Weighted Recall
- Weighted F1 Score
- Accuracy variation
- F1 variation

For small datasets, DataLens AI automatically reduces the number of folds based on the size of the smallest target class.

This prevents invalid cross-validation configurations.

---

# Model Diagnostics

DataLens AI goes beyond basic model metrics.

## Classification Diagnostics

Classification diagnostics can include:

- ROC curve analysis
- ROC-AUC
- Precision-Recall analysis
- Average Precision
- Threshold-based evaluation

Threshold analysis evaluates multiple decision thresholds without automatically claiming that one threshold is universally optimal.

---

## Regression Diagnostics

Regression diagnostics analyze:

- Prediction errors
- Residual behavior
- Error distributions
- Model reliability indicators

These diagnostics provide additional context beyond a single evaluation score.

---

# Explainability

DataLens AI includes an explainability layer for understanding model behavior.

Depending on the model, the platform can provide:

- Global feature importance
- Coefficient-based importance
- Local feature contributions
- Tree-based feature importance

For compatible linear models, local contribution analysis is based on the transformed feature value multiplied by its model coefficient.

Explainability outputs are explicitly treated as **model behavior explanations, not causal conclusions**.

Feature importance does not imply that changing a feature will cause a specific business outcome.

---

# Business Analytics Engine

Machine learning results are complemented by a dedicated business analytics layer.

The business analytics system includes:

### KPI Engine

Extracts useful dataset-level and analytical KPIs.

### Segment Analysis

Analyzes meaningful groups or categories in the dataset.

### Business Findings

Produces factual findings based on calculated data.

### Correlation Insights

Strong relationships can be surfaced as analytical observations while avoiding unsupported causal claims.

The business analytics layer is deterministic and based on computed results rather than LLM-generated numbers.

---

# Decision / Insight Engine

DataLens AI contains a deterministic decision engine that converts analytical outputs into structured decision-oriented insights.

The engine can produce:

- Executive summary
- Data quality observations
- Model observations
- Business insights
- Explainability insights
- Prioritized findings
- Safety metadata

The Decision Engine runs **before the AI Analyst**.

This architecture ensures that important metrics and conclusions originate from Python-based analytics rather than being invented by a language model.

---

# AI Analyst

DataLens AI integrates an LLM-powered AI Analyst using a provider-independent architecture.

The current implementation supports Groq-based language models.

The AI Analyst receives structured analytical context containing information from:

- Data profiling
- EDA
- Machine learning
- Model diagnostics
- Explainability
- Business analytics
- Decision insights

The LLM's role is to **explain and communicate calculated evidence**, not generate analytical metrics.

## AI Safety Principle

> Python calculates. The LLM explains.

The system is intentionally designed so the AI Analyst does not act as the source of truth for numerical metrics.

This reduces the risk of hallucinated analytical results.

---

# AI Context Compression

Large analytical outputs can contain significantly more information than an LLM needs.

DataLens AI therefore contains a context-building layer that prepares and compresses analytical information before it is passed to the AI Analyst.

This helps:

- Reduce unnecessary context
- Preserve important evidence
- Improve prompt quality
- Keep analytical explanations focused
- Reduce token usage

---

# Professional HTML Reporting

Each completed analysis can generate a standalone professional HTML report.

The report contains major sections such as:

1. Dataset Overview
2. Machine Learning Analysis
3. Business Analytics
4. Decision Insights
5. AI Analyst Report

The report interface uses a clean navy, blue, and white visual identity and is designed to be:

- Responsive
- Readable
- Presentation-friendly
- Print-friendly
- Suitable for PDF export from the browser

Reports are stored under:

```text
reports/generated/
```

---

# Web Dashboard

DataLens AI includes a modern frontend built using Next.js and TypeScript.

The primary user workflow is:

```text
Upload Dataset
      ↓
Dataset Overview
      ↓
Select Target
      ↓
Configure Analysis
      ↓
Run Analysis
      ↓
Analysis Progress
      ↓
Results Dashboard
      ↓
Open Full Report
```

Users can also view previous analyses through the Analysis History interface.

---

# Frontend Components

The frontend is separated into reusable components:

```text
frontend/components/
├── AnalysisConfig.tsx
├── AnalysisHistory.tsx
├── AnalysisProgress.tsx
├── DatasetOverview.tsx
├── Navbar.tsx
├── ResultsDashboard.tsx
└── UploadDataset.tsx
```

The main application files are:

```text
frontend/app/
├── favicon.ico
├── globals.css
├── layout.tsx
└── page.tsx
```

---

# FastAPI Backend

The backend is built with FastAPI.

Application metadata:

```text
Application: DataLens AI API
Version: 1.1.0
```

During local development:

```text
Frontend: http://localhost:3000
Backend:  http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs
```

The API handles:

- Dataset upload
- Dataset information
- Analysis requests
- Analysis history
- Generated report delivery
- Health checks

Pydantic schemas provide request and response validation.

---

# Analysis Persistence

DataLens AI uses SQLite for lightweight analysis persistence.

Stored information allows the platform to maintain analysis history and reconnect generated reports with previous analyses.

Database-related modules are located in:

```text
src/database/
├── analysis_repository.py
└── connection.py
```

---

# End-to-End Architecture

```text
CSV Dataset
     │
     ▼
Dataset Service
     │
     ▼
Data Validation & Profiling
     │
     ▼
Exploratory Data Analysis
     │
     ▼
Target Validation
     │
     ▼
Problem Detection
     │
     ├───────────────┐
     ▼               ▼
Classification    Regression
     │               │
     └───────┬───────┘
             ▼
     Feature Engineering
             │
             ▼
        Preprocessing
             │
             ▼
       Model Training
             │
             ▼
      Model Evaluation
             │
             ▼
        Diagnostics
             │
             ▼
       Explainability
             │
             ▼
     Business Analytics
             │
             ▼
    Decision / Insight Engine
             │
             ▼
         AI Analyst
             │
        ┌────┴────┐
        ▼         ▼
   Dashboard   HTML Report
```

---

# Project Structure

```text
DataLens-AI/
│
├── src/
│   │
│   ├── ai_analyst/
│   │   ├── analyst.py
│   │   ├── context_builder.py
│   │   ├── llm_client.py
│   │   └── prompt.py
│   │
│   ├── api/
│   │   ├── app.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── business_analytics/
│   │   ├── business_engine.py
│   │   ├── business_findings.py
│   │   ├── kpi_engine.py
│   │   └── segment_analysis.py
│   │
│   ├── database/
│   │   ├── analysis_repository.py
│   │   └── connection.py
│   │
│   ├── data_profiler/
│   │   ├── cardinality.py
│   │   ├── data_types.py
│   │   ├── duplicates.py
│   │   ├── feature_types.py
│   │   ├── imbalance.py
│   │   ├── loader.py
│   │   ├── missing_values.py
│   │   ├── outliers.py
│   │   ├── profiler.py
│   │   ├── quality_score.py
│   │   ├── suspicious_columns.py
│   │   └── validator.py
│   │
│   ├── decision_engine/
│   │   └── insight_engine.py
│   │
│   ├── eda/
│   │   ├── categorical_analysis.py
│   │   ├── correlations.py
│   │   ├── descriptive_stats.py
│   │   ├── distributions.py
│   │   ├── insights.py
│   │   ├── relationships.py
│   │   └── visualizations.py
│   │
│   ├── ml/
│   │   ├── classification_diagnostics.py
│   │   ├── class_performance.py
│   │   ├── cross_validator.py
│   │   ├── dataset_config.py
│   │   ├── data_split.py
│   │   ├── evaluator.py
│   │   ├── explainability.py
│   │   ├── feature_engineer.py
│   │   ├── feature_engineering_analyzer.py
│   │   ├── feature_target.py
│   │   ├── imbalance_handler.py
│   │   ├── ml_router.py
│   │   ├── model_builder.py
│   │   ├── model_comparison.py
│   │   ├── pipeline_builder.py
│   │   ├── predictor.py
│   │   ├── preprocessing_analyzer.py
│   │   ├── preprocessor.py
│   │   ├── problem_detector.py
│   │   ├── regression_diagnostics.py
│   │   ├── regression_engine.py
│   │   └── trainer.py
│   │
│   ├── reporting/
│   │   ├── html_report.py
│   │   └── report_builder.py
│   │
│   └── services/
│       ├── analysis_service.py
│       └── dataset_service.py
│
├── frontend/
│   ├── app/
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/
│   │   ├── AnalysisConfig.tsx
│   │   ├── AnalysisHistory.tsx
│   │   ├── AnalysisProgress.tsx
│   │   ├── DatasetOverview.tsx
│   │   ├── Navbar.tsx
│   │   ├── ResultsDashboard.tsx
│   │   └── UploadDataset.tsx
│   │
│   └── types/
│       └── index.ts
│
├── tests/
│   ├── test_api.py
│   ├── test_cross_validator.py
│   ├── test_dataset_config.py
│   ├── test_feature_target.py
│   └── test_problem_detector.py
│
├── reports/
│   ├── eda/
│   └── generated/
│
├── data/
│   ├── uploads/
│   └── datalens.db
│
├── pyproject.toml
└── README.md
```

---

# Technology Stack

## Backend

- Python 3.13+
- FastAPI
- Pydantic
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- SQLite
- Groq API
- Uvicorn
- uv

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Testing

- Pytest
- FastAPI TestClient

---

# Automated Testing

DataLens AI includes automated tests for critical ML and API behavior.

Current test suite:

```text
tests/
├── test_problem_detector.py
├── test_dataset_config.py
├── test_feature_target.py
├── test_cross_validator.py
└── test_api.py
```

Coverage includes:

- ML problem detection
- Dataset target configuration
- Feature/target separation
- Identifier detection
- Missing-target handling
- Cross-validation safety
- Dynamic fold reduction
- API validation
- Dataset information endpoints
- Analysis endpoint behavior
- Analysis history
- Report serving
- JSON-safe API conversion
- Dashboard response construction
- Safe internal error handling

Current verified result:

```text
76 passed
```

Run the complete test suite with:

```bash
uv run pytest -v
```

---

# Installation

## Prerequisites

Make sure the following are installed:

- Python 3.13+
- Node.js
- npm
- uv

---

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd DataLens-AI
```

---

## 2. Install Backend Dependencies

Using `uv`:

```bash
uv sync
```

---

## 3. Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit API keys or secrets to GitHub.

---

## 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

Then return to the project root when needed:

```bash
cd ..
```

---

# Running the Application

Two terminals are recommended.

## Terminal 1 — Backend

From the project root:

```bash
uv run uvicorn src.api.app:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:3000
```

Open the frontend URL in your browser.

---

# Typical User Workflow

1. Open DataLens AI.
2. Upload a CSV dataset.
3. Review dataset information.
4. Select the target column.
5. Configure optional analysis settings.
6. Start the analysis.
7. DataLens automatically detects classification or regression.
8. The platform profiles and analyzes the dataset.
9. Feature engineering and preprocessing are applied.
10. Machine learning models are trained and evaluated.
11. Diagnostics and explainability are generated.
12. Business analytics are calculated.
13. Decision insights are generated from computed evidence.
14. The AI Analyst explains the results.
15. Review the Results Dashboard.
16. Open the complete HTML report.
17. Access previous runs through Analysis History.

---

# Engineering Principles

DataLens AI follows several important design principles.

### Evidence Before Explanation

Analytical metrics are calculated by Python-based engines before being sent to the AI layer.

### Leakage-Safe ML

Preprocessing is designed to be fitted through ML pipelines rather than using information from the complete dataset during training.

### Generic Dataset Support

The system is designed to work dynamically across different CSV datasets instead of being tied to a single hard-coded dataset.

### Explainability Is Not Causality

Model importance and local contributions describe model behavior. They do not prove real-world causal relationships.

### Conservative Automation

The system avoids automatically removing every high-cardinality feature or automatically declaring a decision threshold optimal without sufficient evidence.

### Deterministic Decision Insights

Important decision insights are generated from analytical evidence before the LLM explanation layer.

### LLM as Communication Layer

The AI Analyst explains structured results instead of acting as the source of analytical truth.

---

# Project Status

Major platform capabilities completed:

- [x] Data profiling
- [x] Exploratory data analysis
- [x] Dynamic problem detection
- [x] Classification engine
- [x] Regression engine
- [x] Dynamic preprocessing
- [x] Feature engineering
- [x] Cross-validation
- [x] Model diagnostics
- [x] Explainability
- [x] Business analytics
- [x] Decision / Insight Engine
- [x] AI Analyst
- [x] Context compression
- [x] Professional HTML reporting
- [x] FastAPI backend
- [x] SQLite analysis history
- [x] Next.js dashboard
- [x] Generic dataset robustness
- [x] Backend hardening
- [x] Automated testing — 76 tests passing

---

# Future Improvements

Potential future enhancements include:

- Containerized deployment with Docker
- Cloud deployment
- Additional ML algorithms
- Hyperparameter tuning
- More advanced model explainability
- Extended visualization library
- Exportable PDF reports
- Authentication and user workspaces
- Dataset and report lifecycle management
- Background analysis jobs for larger datasets
- Production-grade database integration

---

# Project Objective

DataLens AI was built as an end-to-end data science and business analytics engineering project demonstrating practical skills across:

**Python • Data Analysis • Machine Learning • Statistics • Feature Engineering • Model Evaluation • Explainability • Business Analytics • Generative AI • FastAPI • Next.js • REST APIs • Testing • Software Architecture**

The project demonstrates how machine learning can be integrated into a complete analytical product rather than existing only as an isolated notebook or model.

---

## DataLens AI

**From raw data to evidence-backed analytical insights.**