"use client";

// ==========================================
// DATALENS AI - DATASET UPLOAD V4
// ==========================================

import { useRef, useState } from "react";

import { uploadDataset } from "@/lib/api";

import type { DatasetUploadResponse } from "@/types";

interface UploadDatasetProps {
  onUploadSuccess: (dataset: DatasetUploadResponse) => void;
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function UploadDataset({
  onUploadSuccess,
}: UploadDatasetProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // ========================================
  // FILE SELECTION
  // ========================================

  function acceptFile(file: File | undefined) {
    setError(null);

    if (!file) {
      setSelectedFile(null);
      return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
      setSelectedFile(null);
      setError("Please select a CSV file.");
      // allow the same file to be chosen again after a rejection
      if (fileInputRef.current) fileInputRef.current.value = "";
      return;
    }

    setSelectedFile(file);
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    acceptFile(event.target.files?.[0]);
  }

  function handleDrop(event: React.DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
    if (isUploading) return;
    acceptFile(event.dataTransfer.files?.[0]);
  }

  function openPicker() {
    if (!isUploading) fileInputRef.current?.click();
  }

  // ========================================
  // UPLOAD
  // ========================================

  async function handleUpload() {
    if (!selectedFile) {
      setError("Please select a CSV file first.");
      return;
    }

    try {
      setIsUploading(true);
      setError(null);

      const result = await uploadDataset(selectedFile);

      onUploadSuccess(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Dataset upload failed.");
      }
    } finally {
      setIsUploading(false);
    }
  }

  // ========================================
  // UI
  // ========================================

  return (
    <section className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,text/csv"
        onChange={handleFileChange}
        className="hidden"
        tabIndex={-1}
        aria-label="Choose a CSV file"
      />

      {/* DROP ZONE */}

      <div
        role="button"
        tabIndex={isUploading ? -1 : 0}
        aria-disabled={isUploading}
        aria-label="Drop a CSV file here or press Enter to browse"
        onClick={(e) => {
          // the Browse button handles its own click
          if ((e.target as HTMLElement).closest("button")) return;
          openPicker();
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            openPicker();
          }
        }}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={(e) => {
          // ignore leave events fired when moving over child elements
          if (!e.currentTarget.contains(e.relatedTarget as Node | null)) {
            setIsDragging(false);
          }
        }}
        onDrop={handleDrop}
        className={`group relative cursor-pointer overflow-hidden rounded-[28px] px-6 py-14 text-center transition-all duration-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2 ${
          isDragging
            ? "bg-[#eef0f8] shadow-[0_0_0_6px_rgba(77,91,158,.12)]"
            : "bg-gradient-to-b from-[#faf9f5] to-white hover:from-white hover:to-white"
        } ${isUploading ? "cursor-not-allowed opacity-80" : ""}`}
      >
        {/* dashed border drawn as an SVG so corners stay crisp */}
        <svg aria-hidden className="pointer-events-none absolute inset-0 h-full w-full">
          <rect
            x="1"
            y="1"
            width="calc(100% - 2px)"
            height="calc(100% - 2px)"
            rx="27"
            fill="none"
            strokeWidth="1.5"
            strokeDasharray="7 7"
            strokeLinecap="round"
            className={`transition-colors duration-300 ${
              isDragging ? "stroke-[#4d5b9e]" : "stroke-[#d4cfc0] group-hover:stroke-[#4d5b9e]/60"
            }`}
          />
        </svg>

        <div
          aria-hidden
          className="pointer-events-none absolute -top-24 left-1/2 h-48 w-80 -translate-x-1/2 rounded-full bg-[#4d5b9e]/15 blur-3xl transition-opacity duration-500 group-hover:opacity-100"
          style={{ opacity: isDragging ? 1 : 0.45 }}
        />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-x-16 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent"
        />

        <div className="relative">
          <div className="relative mx-auto h-[72px] w-[72px]">
            {/* soft pulse ring while dragging */}
            <span
              aria-hidden
              className={`absolute inset-0 rounded-[22px] bg-[#4d5b9e]/30 transition-all duration-500 ${
                isDragging ? "scale-125 animate-ping opacity-100" : "scale-100 opacity-0"
              }`}
            />
            <div
              className={`relative flex h-full w-full items-center justify-center rounded-[22px] bg-gradient-to-br from-[#0c1424] to-[#1a2744] text-white shadow-[0_20px_40px_-14px_rgba(12,20,36,.65)] ring-1 ring-white/10 transition-transform duration-300 ${
                isDragging ? "-translate-y-1 scale-105" : "group-hover:-translate-y-0.5"
              }`}
            >
              <span aria-hidden className="absolute inset-x-4 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/80 to-transparent" />
              <svg viewBox="0 0 24 24" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                <path d="M12 16V4" />
                <path d="m7 9 5-5 5 5" />
                <path d="M4 15v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" />
              </svg>
            </div>
          </div>

          <h3 className="mt-7 text-lg font-semibold tracking-[-0.01em] text-[#0c1424]">
            {isDragging ? "Drop your file to select it" : "Drag and drop your CSV here"}
          </h3>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-[#5b6173]">
            Or choose a file from your computer. DataLens checks the structure
            before any analysis begins.
          </p>

          <button
            type="button"
            onClick={openPicker}
            disabled={isUploading}
            className="mt-7 inline-flex h-11 items-center justify-center rounded-full border border-[#d4cfc0] bg-white px-6 text-sm font-semibold text-[#0c1424] shadow-[0_1px_2px_rgba(12,20,36,.05)] transition duration-300 hover:-translate-y-px hover:border-[#4d5b9e]/60 hover:shadow-[0_12px_30px_-12px_rgba(77,91,158,.55)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
          >
            Browse files
          </button>

          <p className="mt-5 text-xs text-[#9a9eaf]">Supports .csv files</p>
        </div>
      </div>

      {/* SELECTED FILE */}

      {selectedFile && (
        <div className="relative mt-5 flex flex-col gap-3 overflow-hidden rounded-2xl border border-[#e3e0d6] bg-white p-4 shadow-[0_1px_2px_rgba(12,20,36,.04),0_20px_40px_-28px_rgba(12,20,36,.25)] sm:flex-row sm:items-center sm:justify-between">
          <span aria-hidden className="absolute inset-y-0 left-0 w-[3px] bg-gradient-to-b from-[#4d5b9e] to-[#a9bbd8]" />

          <div className="flex min-w-0 items-center gap-4 pl-1.5">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-[#eef0f8] to-[#e1e9f6] text-[11px] font-bold tracking-wide text-[#3d4a86] ring-1 ring-[#4d5b9e]/10">
              CSV
            </div>

            <div className="min-w-0">
              <p
                className="truncate text-sm font-semibold text-[#0c1424]"
                title={selectedFile.name}
              >
                {selectedFile.name}
              </p>
              <p className="mt-0.5 text-xs text-[#9a9eaf]">
                {formatSize(selectedFile.size)} · Ready for upload
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              File selected
            </span>

            <button
              type="button"
              onClick={() => {
                setSelectedFile(null);
                setError(null);
                if (fileInputRef.current) fileInputRef.current.value = "";
              }}
              disabled={isUploading}
              className="text-xs font-medium text-[#5b6173] underline-offset-4 transition hover:text-[#0c1424] hover:underline disabled:opacity-50"
            >
              Remove
            </button>
          </div>
        </div>
      )}

      {/* ERROR */}

      {error && (
        <div
          role="alert"
          className="mt-5 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3.5"
        >
          <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-red-100 text-[11px] font-bold text-red-700">
            !
          </span>
          <p className="text-sm font-medium text-red-700">{error}</p>
        </div>
      )}

      {/* ACTION */}

      <div className="mt-7 flex justify-end">
        <button
          type="button"
          onClick={handleUpload}
          disabled={!selectedFile || isUploading}
          className="group relative inline-flex h-12 min-w-[200px] items-center justify-center gap-2.5 overflow-hidden rounded-full bg-[#0c1424] px-7 text-sm font-semibold text-white shadow-[0_18px_40px_-16px_rgba(12,20,36,.7)] ring-1 ring-white/10 transition duration-300 hover:-translate-y-0.5 hover:bg-[#16223a] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4d5b9e] focus-visible:ring-offset-2 disabled:translate-y-0 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none disabled:ring-0"
        >
          <span aria-hidden className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent group-disabled:hidden" />
          {isUploading ? (
            <>
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
              Uploading...
            </>
          ) : (
            <>
              Upload Dataset
              <span className="transition-transform group-hover:translate-x-1">→</span>
            </>
          )}
        </button>
      </div>
    </section>
  );
}