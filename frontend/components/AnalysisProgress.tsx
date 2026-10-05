"use client";

// ==========================================
// DATALENS AI - ANALYSIS PROGRESS V4
// ==========================================

import { useEffect, useState } from "react";

interface AnalysisProgressProps {
  isAnalyzing: boolean;
}

const pipelineSteps = [
  "Profiling",
  "EDA",
  "Machine Learning",
  "Diagnostics",
  "Explainability",
  "Business Analytics",
  "Decision Engine",
  "AI Analyst",
  "Reporting",
];

function formatElapsed(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function AnalysisProgress({
  isAnalyzing,
}: AnalysisProgressProps) {
  // Elapsed time, restarts each time an analysis begins
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!isAnalyzing) return;

    setElapsed(0);
    const started = Date.now();
    const timer = window.setInterval(() => {
      setElapsed(Math.floor((Date.now() - started) / 1000));
    }, 1000);

    return () => window.clearInterval(timer);
  }, [isAnalyzing]);

  if (!isAnalyzing) {
    return null;
  }

  const cycle = pipelineSteps.length;

  return (
    <section className="w-full" role="status" aria-live="polite">
      <style>{`
        @keyframes dl-slide{0%{transform:translateX(-110%)}100%{transform:translateX(280%)}}
        @keyframes dl-step{0%,16%,100%{opacity:0;transform:scale(.96)}4%,12%{opacity:1;transform:scale(1)}}
        @keyframes dl-dot{0%,16%,100%{background:#d4cfc0;transform:scale(1)}4%,12%{background:#4d5b9e;transform:scale(1.5)}}
        @keyframes dl-label{0%,16%,100%{color:#2b3147}4%,12%{color:#3d4a86}}
        @keyframes dl-orbit{to{transform:rotate(360deg)}}
        @keyframes dl-breathe{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.15)}}
      `}</style>

      <div className="relative overflow-hidden rounded-3xl border border-[#4d5b9e]/20 bg-white shadow-[0_30px_70px_-40px_rgba(77,91,158,.6)]">
        {/* brass hairline + soft glows */}
        <span
          aria-hidden
          className="absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute -right-20 -top-24 h-64 w-64 rounded-full bg-[#4d5b9e]/10 blur-3xl"
          style={{ animation: "dl-breathe 5s ease-in-out infinite" }}
        />
        <div
          aria-hidden
          className="pointer-events-none absolute -bottom-24 -left-16 h-56 w-56 rounded-full bg-[#a9bbd8]/15 blur-3xl"
        />

        <div className="relative px-6 py-7 sm:px-8">
          {/* HEADER */}

          <div className="flex items-start gap-5">
            <div className="relative flex h-14 w-14 shrink-0 items-center justify-center">
              <div className="absolute inset-0 rounded-full bg-[#4d5b9e]/10" />
              <div
                className="absolute inset-0 rounded-full border-2 border-transparent border-r-[#a9bbd8] border-t-[#4d5b9e]"
                style={{ animation: "dl-orbit 1.1s linear infinite" }}
              />
              <div
                className="absolute inset-2 rounded-full border border-transparent border-b-[#c9b98a]/70"
                style={{ animation: "dl-orbit 2.4s linear infinite reverse" }}
              />
              <span className="h-2.5 w-2.5 rounded-full bg-gradient-to-br from-[#4d5b9e] to-[#a9bbd8]" />
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2">
                <h3 className="font-serif text-xl tracking-[-0.02em] text-[#0c1424]">
                  DataLens is analyzing your dataset
                </h3>

                <span
                  aria-hidden
                  className="datalens-number inline-flex items-center gap-2 rounded-full border border-[#e3e0d6] bg-[#faf9f5] px-3 py-1 font-mono text-xs font-medium text-[#5b6173]"
                >
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#4d5b9e]" />
                  {formatElapsed(elapsed)}
                </span>
              </div>

              <p className="mt-1.5 max-w-3xl text-sm leading-6 text-[#5b6173]">
                Statistical analysis, machine learning, explainability,
                business intelligence, decision insights and report generation
                are running automatically.
              </p>
            </div>
          </div>

          {/* INDETERMINATE BAR */}

          <div className="mt-7 h-1.5 overflow-hidden rounded-full bg-[#ece9e0]">
            <div
              className="h-full w-2/5 rounded-full bg-gradient-to-r from-[#4d5b9e] via-[#a9bbd8] to-[#4d5b9e]"
              style={{ animation: "dl-slide 1.8s cubic-bezier(.4,0,.2,1) infinite" }}
            />
          </div>

          {/* PIPELINE STEPS */}

          <ol className="mt-6 grid gap-2.5 sm:grid-cols-3 lg:grid-cols-5 xl:grid-cols-9">
            {pipelineSteps.map((step, index) => (
              <li
                key={step}
                className="relative overflow-hidden rounded-2xl border border-[#ece9e0] bg-[#faf9f5] px-3.5 py-3.5"
              >
                <span
                  aria-hidden
                  className="absolute inset-0 rounded-2xl border border-[#4d5b9e]/40 bg-gradient-to-br from-[#eef0f8] to-white shadow-[0_12px_28px_-16px_rgba(77,91,158,.6)]"
                  style={{
                    opacity: 0,
                    animation: `dl-step ${cycle}s ease-in-out ${index}s infinite`,
                  }}
                />

                <div className="relative">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] font-semibold text-[#9a9eaf]">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <span
                      aria-hidden
                      className="h-1.5 w-1.5 rounded-full bg-[#d4cfc0]"
                      style={{
                        animation: `dl-dot ${cycle}s ease-in-out ${index}s infinite`,
                      }}
                    />
                  </div>

                  <p
                    className="mt-2 text-xs font-semibold leading-4 text-[#2b3147]"
                    style={{
                      animation: `dl-label ${cycle}s ease-in-out ${index}s infinite`,
                    }}
                  >
                    {step}
                  </p>
                </div>
              </li>
            ))}
          </ol>

          <p className="mt-5 text-xs text-[#9a9eaf]">
            Processing time depends on dataset size and model complexity.
          </p>
        </div>
      </div>
    </section>
  );
}