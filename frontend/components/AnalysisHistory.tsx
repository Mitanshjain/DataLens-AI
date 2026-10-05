"use client";

// ==========================================
// DATALENS AI - ANALYSIS HISTORY V3
// ==========================================

import { useEffect, useState } from "react";

import { getAnalysisHistory, getReportUrl } from "@/lib/api";

import type { AnalysisHistoryItem } from "@/types";

// ==========================================
// COMPONENT
// ==========================================

export default function AnalysisHistory() {
  const [analyses, setAnalyses] = useState<AnalysisHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ========================================
  // LOAD ANALYSIS HISTORY
  // ========================================

  async function loadHistory() {
    try {
      setIsLoading(true);
      setError(null);

      const response = await getAnalysisHistory();

      setAnalyses(response.analyses);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Unable to load analysis history.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  // ========================================
  // LOAD ON COMPONENT MOUNT
  // ========================================

  useEffect(() => {
    void loadHistory();
  }, []);

  // ========================================
  // FORMAT DATE
  // ========================================

  function formatDate(dateString: string) {
    const date = new Date(dateString);

    return date.toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  }

  // ========================================
  // OPEN REPORT
  // ========================================

  function handleOpenReport(reportUrl: string) {
    window.open(getReportUrl(reportUrl), "_blank", "noopener,noreferrer");
  }

  // ========================================
  // UI
  // ========================================

  return (
    <section className="space-y-5">
      {/* COUNT */}

      {!isLoading && !error && analyses.length > 0 && (
        <div className="flex items-center justify-between gap-4">
          <p className="text-sm text-[#5b6173]">
            Your previously completed DataLens analyses.
          </p>

          <span className="datalens-number shrink-0 rounded-full border border-[#e3e0d6] bg-white px-3.5 py-1.5 text-xs font-medium text-[#5b6173] shadow-[0_1px_2px_rgba(12,20,36,.04)]">
            {analyses.length} {analyses.length === 1 ? "analysis" : "analyses"}
          </span>
        </div>
      )}

      {/* LOADING */}

      {isLoading && (
        <div role="status" aria-live="polite" className="space-y-4">
          <span className="sr-only">Loading analysis history...</span>

          {[0, 1].map((i) => (
            <div
              key={i}
              aria-hidden
              className="relative overflow-hidden rounded-3xl border border-[#e3e0d6] bg-white p-6 shadow-[0_1px_2px_rgba(12,20,36,.04)] sm:p-7"
            >
              <div className="animate-pulse space-y-5" style={{ animationDelay: `${i * 150}ms` }}>
                <div className="flex items-center gap-3">
                  <div className="h-5 w-48 rounded-full bg-[#ece9e0]" />
                  <div className="h-6 w-24 rounded-full bg-[#4d5b9e]/10" />
                </div>
                <div className="h-3.5 w-36 rounded-full bg-[#ece9e0]" />
                <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                  {[0, 1, 2, 3].map((j) => (
                    <div key={j} className="h-16 rounded-2xl bg-[#faf9f5]" />
                  ))}
                </div>
              </div>
            </div>
          ))}

          <p className="flex items-center justify-center gap-2.5 pt-1 text-sm text-[#5b6173]" aria-hidden>
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#ece9e0] border-t-[#4d5b9e]" />
            Loading analysis history...
          </p>
        </div>
      )}

      {/* ERROR */}

      {!isLoading && error && (
        <div
          role="alert"
          className="flex flex-col gap-4 rounded-3xl border border-red-200 bg-red-50 p-6 sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex items-start gap-4">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-100 font-bold text-red-700">
              !
            </div>

            <div>
              <p className="text-sm font-semibold text-red-800">Unable to load history</p>
              <p className="mt-1 text-sm text-red-700">{error}</p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => {
              void loadHistory();
            }}
            className="inline-flex h-10 shrink-0 items-center justify-center rounded-full border border-red-200 bg-white px-5 text-sm font-medium text-red-700 transition hover:bg-red-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-400 focus-visible:ring-offset-2"
          >
            Try again
          </button>
        </div>
      )}

      {/* EMPTY STATE */}

      {!isLoading && !error && analyses.length === 0 && (
        <div className="relative overflow-hidden rounded-3xl border border-dashed border-[#d4cfc0] bg-gradient-to-b from-[#faf9f5] to-white px-6 py-16 text-center">
          <span
            aria-hidden
            className="absolute inset-x-16 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/60 to-transparent"
          />
          <div
            aria-hidden
            className="pointer-events-none absolute left-1/2 top-0 h-40 w-72 -translate-x-1/2 rounded-full bg-[#4d5b9e]/10 blur-3xl"
          />

          <div className="relative">
            <div className="relative mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-[#0c1424] to-[#1a2744] text-xl text-white shadow-[0_16px_36px_-14px_rgba(12,20,36,.6)] ring-1 ring-white/10">
              <span
                aria-hidden
                className="absolute inset-x-3 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/80 to-transparent"
              />
              ↗
            </div>

            <h3 className="mt-6 font-serif text-2xl tracking-[-0.02em] text-[#0c1424]">
              No analyses yet
            </h3>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-[#5b6173]">
              Upload a dataset and complete your first analysis. It will appear
              here automatically.
            </p>

            <a
              href="#workspace"
              className="mt-7 inline-flex h-11 items-center rounded-full bg-[#0c1424] px-6 text-sm font-semibold text-white shadow-[0_18px_40px_-16px_rgba(12,20,36,.7)] transition duration-300 hover:-translate-y-0.5 hover:bg-[#16223a] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2"
            >
              Start an analysis
            </a>
          </div>
        </div>
      )}

      {/* HISTORY LIST */}

      {!isLoading && !error && analyses.length > 0 && (
        <div className="space-y-4">
          {analyses.map((analysis) => (
            <article
              key={analysis.analysis_id}
              className="group relative overflow-hidden rounded-3xl border border-[#e3e0d6] bg-white p-6 shadow-[0_1px_2px_rgba(12,20,36,.04)] transition duration-300 hover:-translate-y-0.5 hover:border-[#4d5b9e]/30 hover:shadow-[0_30px_70px_-40px_rgba(77,91,158,.55)] sm:p-7"
            >
              <span
                aria-hidden
                className="absolute inset-y-0 left-0 w-[3px] origin-top scale-y-0 bg-gradient-to-b from-[#4d5b9e] to-[#a9bbd8] transition-transform duration-500 group-hover:scale-y-100"
              />
              <span
                aria-hidden
                className="absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/0 to-transparent transition-all duration-500 group-hover:via-[#c9b98a]/70"
              />

              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                {/* LEFT */}

                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-3">
                    <h3 className="truncate font-serif text-xl tracking-[-0.02em] text-[#0c1424]">
                      {analysis.original_filename || "Dataset"}
                    </h3>

                    <span className="rounded-full bg-[#4d5b9e]/10 px-3 py-1 text-xs font-medium text-[#3d4a86] ring-1 ring-[#4d5b9e]/10">
                      {analysis.problem_type}
                    </span>
                  </div>

                  <p className="mt-2 text-sm text-[#5b6173]">
                    Target:{" "}
                    <span className="font-semibold text-[#0c1424]">
                      {analysis.target_column}
                    </span>
                  </p>

                  {/* METRICS */}

                  <dl className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
                    <Stat label="Rows" value={analysis.rows.toLocaleString()} />
                    <Stat label="Columns" value={String(analysis.columns)} />
                    <Stat label="Missing" value={analysis.missing_values.toLocaleString()} />
                    <Stat label="Duplicates" value={analysis.duplicate_rows.toLocaleString()} />
                  </dl>

                  <p className="mt-5 flex items-center gap-2 text-xs text-[#9a9eaf]">
                    <span aria-hidden className="h-1 w-1 rounded-full bg-[#c9b98a]" />
                    {formatDate(analysis.created_at)}
                  </p>
                </div>

                {/* RIGHT */}

                <div className="flex shrink-0 items-center">
                  <button
                    type="button"
                    onClick={() => handleOpenReport(analysis.report_url)}
                    className="group/btn relative inline-flex h-12 items-center justify-center gap-2 overflow-hidden rounded-full bg-[#0c1424] px-6 text-sm font-semibold text-white shadow-[0_18px_40px_-16px_rgba(12,20,36,.7)] ring-1 ring-white/10 transition duration-300 hover:-translate-y-0.5 hover:bg-[#16223a] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2"
                  >
                    <span
                      aria-hidden
                      className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent"
                    />
                    Open Report
                    <span className="transition-transform group-hover/btn:-translate-y-0.5 group-hover/btn:translate-x-0.5">
                      ↗
                    </span>
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

// ==========================================
// STAT
// ==========================================

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-[#ece9e0] bg-[#faf9f5] px-4 py-3 transition-colors duration-300 group-hover:bg-[#f3f4fa]">
      <dt className="text-xs text-[#9a9eaf]">{label}</dt>
      <dd className="datalens-number mt-1 text-base font-semibold text-[#0c1424]">
        {value}
      </dd>
    </div>
  );
}