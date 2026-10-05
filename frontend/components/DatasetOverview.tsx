// ==========================================
// DATALENS AI - DATASET OVERVIEW V4
// ==========================================

import type { DatasetUploadResponse } from "@/types";

interface DatasetOverviewProps {
  dataset: DatasetUploadResponse;
}

export default function DatasetOverview({ dataset }: DatasetOverviewProps) {
  return (
    <section className="w-full space-y-6">
      {/* SUMMARY */}

      <div className="grid gap-4 sm:grid-cols-[minmax(0,1.4fr)_1fr_1fr]">
        <SummaryItem
          label="Source file"
          value={dataset.filename}
          icon="CSV"
          compact
        />

        <SummaryItem label="Rows" value={dataset.rows.toLocaleString()} />

        <SummaryItem label="Columns" value={dataset.columns.toLocaleString()} />
      </div>

      {/* COLUMNS */}

      <div className="relative overflow-hidden rounded-3xl border border-[#ece9e0] bg-gradient-to-b from-[#faf9f5] to-white p-6 sm:p-7">
        <span
          aria-hidden
          className="absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/60 to-transparent"
        />

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="font-serif text-xl tracking-[-0.02em] text-[#0c1424]">
              Dataset schema
            </h3>

            <p className="mt-1 text-sm text-[#5b6173]">
              Columns detected from the uploaded CSV.
            </p>
          </div>

          <div className="flex w-fit items-center gap-2 rounded-full bg-emerald-50 px-3.5 py-1.5 text-xs font-medium text-emerald-700 ring-1 ring-emerald-600/10">
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute h-full w-full animate-ping rounded-full bg-emerald-400/60" />
              <span className="relative h-1.5 w-1.5 rounded-full bg-emerald-500" />
            </span>
            Validation passed
          </div>
        </div>

        <div className="mt-6 flex max-h-[18rem] flex-wrap gap-2.5 overflow-y-auto pr-1">
          {dataset.column_names.map((column, index) => (
            <div
              key={column}
              className="group inline-flex items-center gap-2.5 rounded-full border border-[#e3e0d6] bg-white py-1.5 pl-1.5 pr-4 text-sm text-[#2b3147] shadow-[0_1px_2px_rgba(12,20,36,.03)] transition duration-300 hover:-translate-y-0.5 hover:border-[#4d5b9e]/40 hover:shadow-[0_14px_30px_-16px_rgba(77,91,158,.55)]"
            >
              <span className="flex h-6 min-w-6 items-center justify-center rounded-full bg-gradient-to-br from-[#eef0f8] to-[#e1e9f6] px-1.5 font-mono text-[10px] font-semibold text-[#3d4a86] ring-1 ring-[#4d5b9e]/10 transition-colors duration-300 group-hover:from-[#4d5b9e] group-hover:to-[#5d6bb0] group-hover:text-white">
                {String(index + 1).padStart(2, "0")}
              </span>

              <span className="font-medium">{column}</span>
            </div>
          ))}
        </div>

        <div className="mt-6 flex flex-col gap-2 border-t border-[#ece9e0] pt-5 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-[#9a9eaf]">
            {dataset.column_names.length} fields
          </p>

          <p className="flex flex-col gap-1 sm:flex-row sm:items-center sm:gap-3">
            <span className="text-xs font-medium text-[#9a9eaf]">
              Dataset ID
            </span>

            <span className="break-all rounded-md bg-[#0c1424]/[0.04] px-2 py-1 font-mono text-[11px] text-[#5b6173]">
              {dataset.dataset_id}
            </span>
          </p>
        </div>
      </div>
    </section>
  );
}

// ==========================================
// SUMMARY ITEM
// ==========================================

function SummaryItem({
  label,
  value,
  icon,
  compact = false,
}: {
  label: string;
  value: string;
  icon?: string;
  compact?: boolean;
}) {
  return (
    <div className="group relative flex items-center gap-4 overflow-hidden rounded-3xl border border-[#ece9e0] bg-white p-6 shadow-[0_1px_2px_rgba(12,20,36,.04)] transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_26px_60px_-36px_rgba(77,91,158,.5)]">
      <span
        aria-hidden
        className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/0 to-transparent transition-all duration-500 group-hover:via-[#c9b98a]/80"
      />

      {icon && (
        <div className="relative flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[#0c1424] to-[#1a2744] text-[11px] font-bold tracking-wide text-white shadow-[0_14px_30px_-14px_rgba(12,20,36,.6)] ring-1 ring-white/10">
          <span
            aria-hidden
            className="absolute inset-x-3 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/80 to-transparent"
          />
          {icon}
        </div>
      )}

      <div className="min-w-0">
        <p className="text-sm font-medium text-[#5b6173]">{label}</p>

        <p
          className={`mt-1.5 text-[#0c1424] ${
            compact
              ? "truncate text-base font-semibold"
              : "datalens-number font-serif text-[2.4rem] font-light leading-none tracking-[-0.04em]"
          }`}
          title={compact ? value : undefined}
        >
          {value}
        </p>
      </div>
    </div>
  );
}