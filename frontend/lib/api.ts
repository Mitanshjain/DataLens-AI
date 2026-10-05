// ==========================================
// DATALENS AI - API CLIENT V1
// ==========================================

import type {
  AnalysisHistoryResponse,
  AnalysisRequest,
  AnalysisResponse,
  ApiErrorResponse,
  DatasetInfoResponse,
  DatasetUploadResponse,
} from "@/types";


// ==========================================
// API BASE URL
// ==========================================

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000/api";


// ==========================================
// HANDLE API RESPONSE
// ==========================================

async function handleResponse<T>(
  response: Response
): Promise<T> {

  if (!response.ok) {

    let message =
      "Something went wrong while communicating with DataLens AI.";

    try {

      const errorData =
        (await response.json()) as ApiErrorResponse;

      if (errorData.detail) {
        message = errorData.detail;
      }

    } catch {
      // Keep default error message.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}


// ==========================================
// UPLOAD DATASET
// ==========================================

export async function uploadDataset(
  file: File
): Promise<DatasetUploadResponse> {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  const response = await fetch(
    `${API_BASE_URL}/upload`,
    {
      method: "POST",
      body: formData,
    }
  );


  return handleResponse<DatasetUploadResponse>(
    response
  );
}


// ==========================================
// GET DATASET INFORMATION
// ==========================================

export async function getDatasetInfo(
  datasetId: string
): Promise<DatasetInfoResponse> {

  const response = await fetch(
    `${API_BASE_URL}/dataset/${datasetId}`,
    {
      method: "GET",
    }
  );


  return handleResponse<DatasetInfoResponse>(
    response
  );
}


// ==========================================
// RUN ANALYSIS
// ==========================================

export async function runAnalysis(
  request: AnalysisRequest
): Promise<AnalysisResponse> {

  const response = await fetch(
    `${API_BASE_URL}/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(
        request
      ),
    }
  );


  return handleResponse<AnalysisResponse>(
    response
  );
}


// ==========================================
// GET ANALYSIS HISTORY
// ==========================================

export async function getAnalysisHistory():
  Promise<AnalysisHistoryResponse> {

  const response = await fetch(
    `${API_BASE_URL}/analyses`,
    {
      method: "GET",

      cache: "no-store",
    }
  );


  return handleResponse<AnalysisHistoryResponse>(
    response
  );
}


// ==========================================
// GET REPORT URL
// ==========================================

export function getReportUrl(
  reportUrl: string
): string {

  const backendBaseUrl =
    API_BASE_URL.replace(
      /\/api\/?$/,
      ""
    );


  if (reportUrl.startsWith("http")) {
    return reportUrl;
  }


  return `${backendBaseUrl}${reportUrl}`;
}