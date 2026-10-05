// ==========================================
// DATALENS AI - FRONTEND TYPES V2
// ==========================================


// ==========================================
// DATASET UPLOAD RESPONSE
// ==========================================

export interface DatasetUploadResponse {
  status: string;
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  column_names: string[];
}


// ==========================================
// DATASET INFORMATION
// ==========================================

export interface DatasetInfoResponse {
  status: string;
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  column_names: string[];
}


// ==========================================
// ANALYSIS REQUEST
// ==========================================

export interface AnalysisRequest {
  dataset_id: string;
  target_column: string;
  positive_class?: string | number | boolean | null;
}


// ==========================================
// DATASET SUMMARY
// ==========================================

export interface DatasetSummary {
  rows: number;
  columns: number;
  missing_values: number;
  duplicate_rows: number;
}


// ==========================================
// CLASSIFICATION EVALUATION
// ==========================================

export interface ClassificationEvaluation {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  classification_report: string;
}


// ==========================================
// MODEL COMPARISON ROW
// ==========================================
//
// Classification and regression return
// different metric columns.
//
// The additional index signature keeps
// this structure flexible for both.
//

export interface ModelComparisonRow {
  Model: string;

  Accuracy?: number;
  Precision?: number;
  Recall?: number;
  "F1 Score"?: number;

  MAE?: number;
  MSE?: number;
  RMSE?: number;
  "R2 Score"?: number;
  R2?: number;

  [key: string]:
    string | number | null | undefined;
}


// ==========================================
// CROSS VALIDATION ROW
// ==========================================

export interface CrossValidationRow {
  Model: string;

  "CV Accuracy"?: number;
  "CV Precision"?: number;
  "CV Recall"?: number;
  "CV F1 Score"?: number;

  "Accuracy Std"?: number;
  "F1 Std"?: number;

  "CV MAE"?: number;
  "CV MSE"?: number;
  "CV RMSE"?: number;
  "CV R2"?: number;

  [key: string]:
    string | number | null | undefined;
}


// ==========================================
// EXPLAINABILITY FEATURE
// ==========================================

export interface ExplainabilityFeature {
  Feature: string;

  Coefficient?: number;

  "Absolute Coefficient"?: number;

  Importance?: number;

  [key: string]:
    string | number | null | undefined;
}


// ==========================================
// EXPLAINABILITY
// ==========================================

export interface ExplainabilityResult {
  model?: string;
  explanation_type?: string;
  features?: ExplainabilityFeature[];

  [key: string]: unknown;
}


// ==========================================
// BUSINESS KPI TYPES
// ==========================================

export interface DatasetKPIs {
  total_records?: number;
  total_columns?: number;
  missing_values?: number;
  duplicate_rows?: number;
}


export interface NumericalKPI {
  mean?: number;
  median?: number;
  minimum?: number;
  maximum?: number;
  sum?: number;
}


export interface CategoricalKPI {
  unique_values?: number;
  top_value?: string | number | boolean | null;
  top_count?: number;
  top_percentage?: number;
}


export interface TargetKPI {
  type?: string;
  distribution?: Record<string, number>;
}


export interface BusinessKPIs {
  dataset_kpis?: DatasetKPIs;

  numerical_kpis?: Record<
    string,
    NumericalKPI
  >;

  categorical_kpis?: Record<
    string,
    CategoricalKPI
  >;

  target_kpi?: TargetKPI;
}


// ==========================================
// BUSINESS FINDINGS
// ==========================================

export interface BusinessFindings {
  total_findings?: number;
  findings?: string[];
}


// ==========================================
// DASHBOARD DATA
// ==========================================

export interface DashboardData {
  evaluation:
    ClassificationEvaluation | null;

  class_performance:
    Record<string, unknown> | null;

  model_comparison:
    ModelComparisonRow[] | null;

  cross_validation:
    CrossValidationRow[] | null;

  explainability:
    ExplainabilityResult | null;

  business_kpis:
    BusinessKPIs | null;

  business_findings:
    BusinessFindings | null;

  ai_analysis:
    string | null;
}


// ==========================================
// ANALYSIS RESPONSE
// ==========================================

export interface AnalysisResponse {
  status: string;

  analysis_id: string;

  dataset_id: string;

  target_column: string;

  problem_type: string;

  positive_class?:
    string | number | boolean | null;

  dataset_summary: DatasetSummary;

  dashboard: DashboardData;

  report_url: string;
}


// ==========================================
// API ERROR
// ==========================================

export interface ApiErrorResponse {
  detail?: string;
}

// ==========================================
// ANALYSIS HISTORY
// ==========================================

export interface AnalysisHistoryItem {
  analysis_id: string;

  dataset_id: string;

  original_filename: string | null;

  target_column: string;

  problem_type: string;

  positive_class: string | null;

  rows: number;

  columns: number;

  missing_values: number;

  duplicate_rows: number;

  created_at: string;

  report_url: string;
}


export interface AnalysisHistoryResponse {
  status: string;

  total: number;

  analyses: AnalysisHistoryItem[];
}