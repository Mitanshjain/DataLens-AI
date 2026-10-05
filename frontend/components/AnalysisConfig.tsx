"use client";

// ==========================================
// DATALENS AI - ANALYSIS CONFIGURATION V4
// ==========================================

import { useState } from "react";

import type { DatasetUploadResponse } from "@/types";

interface AnalysisConfigProps {
  dataset: DatasetUploadResponse;

  onRunAnalysis: (targetColumn: string) => void;

  isAnalyzing: boolean;
}

const pipelineItems = [
  "Problem detection",
  "Feature preprocessing",
  "Model training",
  "Model evaluation",
  "Explainability",
  "Business insights",
];

export default function AnalysisConfig({
  dataset,
  onRunAnalysis,
  isAnalyzing,
}: AnalysisConfigProps) {
  const [targetColumn, setTargetColumn] = useState("");

  function handleRunAnalysis() {
    if (!targetColumn) {
      return;
    }

    onRunAnalysis(targetColumn);
  }

  return (
    <section className="w-full">
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        {/* TARGET SELECT */}

        <div className="relative overflow-hidden rounded-3xl border border-[#ece9e0] bg-white p-6 shadow-[0_1px_2px_rgba(12,20,36,.03),0_24px_50px_-36px_rgba(12,20,36,.2)] sm:p-7">
          <span
            aria-hidden
            className="absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/60 to-transparent"
          />

          <div className="flex items-start justify-between gap-4">
            <div>
              <label
                htmlFor="target-column"
                className="font-serif text-xl tracking-[-0.02em] text-[#0c1424]"
              >
                Target column
              </label>

              <p className="mt-1.5 text-sm leading-6 text-[#5b6173]">
                Choose the variable the model should learn to predict or
                explain.
              </p>
            </div>

            <span className="datalens-number hidden shrink-0 rounded-full border border-[#e3e0d6] bg-[#faf9f5] px-3 py-1 text-xs font-medium text-[#5b6173] sm:inline-flex">
              {dataset.column_names.length} columns
            </span>
          </div>

          <div className="relative mt-5">
            <select
              id="target-column"
              value={targetColumn}
              onChange={(event) => setTargetColumn(event.target.value)}
              disabled={isAnalyzing}
              className={`h-14 w-full cursor-pointer appearance-none rounded-2xl border bg-gradient-to-b from-[#faf9f5] to-white px-5 pr-14 text-[15px] font-medium outline-none transition duration-300 hover:border-[#4d5b9e]/50 focus:border-[#4d5b9e] focus:bg-white focus:ring-4 focus:ring-[#4d5b9e]/10 disabled:cursor-not-allowed disabled:opacity-60 ${
                targetColumn
                  ? "border-[#4d5b9e]/40 text-[#0c1424]"
                  : "border-[#d4cfc0] text-[#5b6173]"
              }`}
            >
              <option value="">Select target column</option>

              {dataset.column_names.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>

            <span
              aria-hidden
              className="pointer-events-none absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full bg-[#0c1424]/[0.05] text-[10px] text-[#5b6173]"
            >
              ▾
            </span>
          </div>

          {targetColumn && (
            <div
              className="mt-5 flex items-start gap-3 rounded-2xl border border-[#4d5b9e]/20 bg-gradient-to-br from-[#eef0f8] to-white px-4 py-3.5"
              style={{ animation: "dl-rise .5s cubic-bezier(.2,.7,.2,1) both" }}
            >
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#4d5b9e] to-[#5d6bb0] text-[10px] font-bold text-white shadow-[0_6px_14px_-6px_rgba(77,91,158,.8)]">
                ✓
              </span>

              <p className="text-sm leading-6 text-[#2b3147]">
                Selected target:{" "}
                <strong className="font-semibold text-[#0c1424]">
                  {targetColumn}
                </strong>
                . DataLens will automatically classify the task as
                classification or regression.
              </p>
            </div>
          )}
        </div>

        {/* AUTOMATION INFO */}

        <aside className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-[#0c1424] to-[#1a2744] p-6 text-white shadow-[0_30px_60px_-30px_rgba(12,20,36,.7)] ring-1 ring-white/10 sm:p-7">
          <span
            aria-hidden
            className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent"
          />
          <div
            aria-hidden
            className="pointer-events-none absolute -right-12 -top-12 h-40 w-40 rounded-full bg-[#4d5b9e]/50 blur-3xl"
          />

          <div className="relative">
            <p className="font-serif text-xl tracking-[-0.02em]">
              Automated pipeline
            </p>

            <p className="mt-1.5 text-xs leading-5 text-slate-400">
              Everything below runs for you.
            </p>

            <ul className="mt-5 space-y-3.5">
              {pipelineItems.map((item) => (
                <li key={item} className="flex items-center gap-3">
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#e4e9f5] to-[#a9bbd8] text-[10px] font-bold text-[#060a13]">
                    ✓
                  </span>

                  <span className="text-sm text-slate-200">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </aside>
      </div>

      {/* ACTION */}

      <div className="mt-7 flex flex-col gap-4 border-t border-[#ece9e0] pt-6 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs leading-5 text-[#9a9eaf]">
          Analysis runs across the complete DataLens intelligence pipeline.
        </p>

        <button
          type="button"
          onClick={handleRunAnalysis}
          disabled={!targetColumn || isAnalyzing}
          className="group relative inline-flex h-12 min-w-[240px] items-center justify-center gap-2.5 overflow-hidden rounded-full bg-[#0c1424] px-7 text-sm font-semibold text-white shadow-[0_18px_40px_-16px_rgba(12,20,36,.7)] ring-1 ring-white/10 transition duration-300 hover:-translate-y-0.5 hover:bg-[#16223a] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2 disabled:translate-y-0 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none disabled:ring-0"
        >
          <span
            aria-hidden
            className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent group-disabled:hidden"
          />
          {isAnalyzing ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-[#4d5b9e]" />
              Analysis in progress...
            </>
          ) : (
            <>
              Run Complete Analysis
              <span className="transition-transform group-hover:translate-x-1">
                →
              </span>
            </>
          )}
        </button>
      </div>
    </section>
  );
}