"use client";

import { useState } from "react";

import Navbar from "@/components/Navbar";
import UploadDataset from "@/components/UploadDataset";
import DatasetOverview from "@/components/DatasetOverview";
import AnalysisConfig from "@/components/AnalysisConfig";
import AnalysisProgress from "@/components/AnalysisProgress";
import ResultsDashboard from "@/components/ResultsDashboard";
import AnalysisHistory from "@/components/AnalysisHistory";

import { runAnalysis } from "@/lib/api";

import type { AnalysisResponse, DatasetUploadResponse } from "@/types";


// DATALENS AI — premium palette
// night #060a13 · navy #0c1424 · paper #f5f4ef · line #e3e0d6
// indigo #4d5b9e · mist #a9bbd8 · brass #c9b98a (hairlines + one highlight)

export default function Home() {
  const [dataset, setDataset] = useState<DatasetUploadResponse | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  function handleUploadSuccess(uploadedDataset: DatasetUploadResponse) {
    setDataset(uploadedDataset);
    setAnalysisResult(null);
    setAnalysisError(null);
  }

  async function handleRunAnalysis(targetColumn: string) {
    if (!dataset) return;

    try {
      setIsAnalyzing(true);
      setAnalysisError(null);
      setAnalysisResult(null);

      const result = await runAnalysis({
        dataset_id: dataset.dataset_id,
        target_column: targetColumn,
        positive_class: null,
      });

      setAnalysisResult(result);
      setHistoryRefreshKey((current) => current + 1);
    } catch (error) {
      if (error instanceof Error) {
        setAnalysisError(error.message);
      } else {
        setAnalysisError("Analysis failed. Please try again.");
      }
    } finally {
      setIsAnalyzing(false);
    }
  }

  const workspaceStatus = isAnalyzing
    ? "Processing analysis"
    : analysisResult
      ? "Analysis complete"
      : dataset
        ? "Dataset ready"
        : "Ready for data";

  const st = (done: boolean, active: boolean): State =>
    done ? "complete" : active ? "active" : "pending";

  // how many of the 4 steps are finished (drives the progress line)
  const stepsDone = analysisResult ? 4 : dataset ? 2 : 0;

  // Fonts now load once in layout.tsx; font-serif maps to Fraunces via globals.css
  const serif = "font-serif";

  function spotlight(e: React.MouseEvent<HTMLElement>) {
    const r = e.currentTarget.getBoundingClientRect();
    e.currentTarget.style.setProperty("--x", `${e.clientX - r.left}px`);
    e.currentTarget.style.setProperty("--y", `${e.clientY - r.top}px`);
  }

  return (
    <div className={`font-sans min-h-screen bg-[#f5f4ef] text-[#0c1424] antialiased selection:bg-[#4d5b9e]/20`}>
      <style>{`
        html{scroll-behavior:smooth}
        @keyframes dl-rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
        @keyframes dl-draw{from{stroke-dashoffset:900}to{stroke-dashoffset:0}}
        @keyframes dl-grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
        @keyframes dl-ring{from{stroke-dashoffset:339}to{stroke-dashoffset:19}}
        @keyframes dl-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
        @keyframes dl-sheen{from{background-position:200% 0}to{background-position:-200% 0}}
        .dl-grain{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.5'/%3E%3C/svg%3E")}
        .dl-sheen{background:linear-gradient(110deg,#a9bbd8 20%,#fff 40%,#c9b98a 50%,#fff 60%,#a9bbd8 80%);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:dl-sheen 9s linear infinite}
        @media (prefers-reduced-motion:reduce){*{animation:none!important;scroll-behavior:auto!important}}
      `}</style>

      <Navbar />

      {/* ================= HERO ================= */}
      <section
        onMouseMove={spotlight}
        className="relative isolate overflow-hidden bg-[#060a13] pb-24 pt-28 lg:pb-32 lg:pt-36"
        style={{ ["--x" as string]: "70%", ["--y" as string]: "30%" }}
      >
        <div aria-hidden className="pointer-events-none absolute inset-0 -z-10" style={{ background: "radial-gradient(620px circle at var(--x) var(--y),rgba(105,122,196,.22),transparent 60%), radial-gradient(1000px 520px at 85% -10%,rgba(77,91,158,.35),transparent 70%), radial-gradient(700px 420px at 0% 100%,rgba(201,185,138,.08),transparent 70%)" }} />
        <div aria-hidden className="pointer-events-none absolute inset-0 -z-10 opacity-[0.06]" style={{ backgroundImage: "linear-gradient(rgba(255,255,255,.9) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.9) 1px,transparent 1px)", backgroundSize: "64px 64px", WebkitMaskImage: "radial-gradient(ellipse at 70% 30%,#000,transparent 65%)", maskImage: "radial-gradient(ellipse at 70% 30%,#000,transparent 65%)" }} />
        <div aria-hidden className="dl-grain pointer-events-none absolute inset-0 -z-10 opacity-[0.07] mix-blend-overlay" />

        <div className="mx-auto grid max-w-[1280px] items-center gap-16 px-6 lg:grid-cols-[1.05fr_1fr] lg:gap-10 lg:px-10">
          {/* copy */}
          <div style={{ animation: "dl-rise .9s cubic-bezier(.2,.7,.2,1) both" }}>
            <div className="inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-white/[0.04] py-1.5 pl-2 pr-4 backdrop-blur-xl">
              <span className="relative flex h-5 w-5 items-center justify-center">
                <span className="absolute h-5 w-5 animate-ping rounded-full bg-emerald-400/30" />
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
              </span>
              <span className="text-[13px] text-slate-300">Analysis engine online</span>
            </div>

            <h1 className={`${serif} mt-8 text-[3rem] font-light leading-[1.02] tracking-[-0.04em] text-[#f5f4ef] sm:text-[4.2rem] xl:text-[5.2rem]`}>
              <span className="dl-sheen">Turn any dataset into clear decisions.</span>
            </h1>

            <div aria-hidden className="mt-8 h-px w-20 bg-gradient-to-r from-[#c9b98a] to-transparent" />

            <p className="mt-8 max-w-[34rem] text-[17px] leading-8 text-slate-400">
              Upload one CSV and get profiling, a trained model, explainability and a written business briefing, all grounded in what your data actually shows.
            </p>

            <div className="mt-10 flex flex-wrap items-center gap-4">
              <a href="#workspace" className="group inline-flex h-14 items-center rounded-full bg-[#f5f4ef] px-8 text-[15px] font-semibold text-[#060a13] shadow-[0_24px_60px_-20px_rgba(169,187,216,.6)] transition duration-300 hover:-translate-y-0.5 hover:bg-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#060a13]">
                Start an analysis
                <span className="ml-3 flex h-7 w-7 items-center justify-center rounded-full bg-[#060a13] text-[#f5f4ef] transition-transform duration-300 group-hover:translate-x-1">→</span>
              </a>
              <a href="#archive" className="inline-flex h-14 items-center rounded-full border border-white/15 px-8 text-[15px] font-medium text-slate-200 transition hover:border-white/30 hover:bg-white/[0.06] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8]">
                View past reports
              </a>
            </div>

            <dl className="mt-14 flex max-w-lg gap-10 border-t border-white/10 pt-7">
              {[["CSV", "Any structured file"], ["Auto", "Model selection"], ["Plain", "Language briefing"]].map(([k, v]) => (
                <div key={k}>
                  <dt className={`${serif} text-2xl font-light text-white`}>{k}</dt>
                  <dd className="mt-1 text-xs text-slate-500">{v}</dd>
                </div>
              ))}
            </dl>
          </div>

          {/* product frame */}
          <div className="relative" style={{ animation: "dl-rise 1.2s .2s cubic-bezier(.2,.7,.2,1) both" }}>
            <div aria-hidden className="absolute -inset-10 -z-10 rounded-full bg-[#4d5b9e]/25 blur-[90px]" />

            <div className="relative rounded-[30px] border border-white/10 bg-gradient-to-b from-white/[0.08] to-white/[0.02] p-2 shadow-[0_60px_120px_-40px_rgba(77,91,158,.6)] backdrop-blur-2xl">
              <div aria-hidden className="absolute inset-x-12 -top-px h-px bg-gradient-to-r from-transparent via-[#c9b98a]/80 to-transparent" />
              <div className="rounded-[24px] border border-white/[0.06] bg-[#0b1322] p-5 sm:p-6">
                <div className="flex items-center justify-between">
                  <div className="flex gap-1.5">
                    {[0, 1, 2].map((i) => <span key={i} className="h-2.5 w-2.5 rounded-full bg-white/15" />)}
                  </div>
                  <span className="rounded-full border border-white/10 px-3 py-1 text-[11px] text-slate-400">Sample output</span>
                </div>

                <div className="mt-6 grid gap-4 sm:grid-cols-[auto_1fr] sm:items-center">
                  <div className="relative mx-auto h-36 w-36">
                    <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90" aria-hidden>
                      <defs>
                        <linearGradient id="dl-ring" x1="0" x2="1"><stop offset="0" stopColor="#6b7bbd" /><stop offset="1" stopColor="#dbe4f4" /></linearGradient>
                      </defs>
                      <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,.07)" strokeWidth="8" />
                      <circle cx="60" cy="60" r="54" fill="none" stroke="url(#dl-ring)" strokeWidth="8" strokeLinecap="round" strokeDasharray="339" strokeDashoffset="19" style={{ animation: "dl-ring 2s .6s cubic-bezier(.2,.7,.2,1) both" }} />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className={`${serif} text-4xl font-light text-white`}>94.2<span className="text-xl text-slate-400">%</span></span>
                      <span className="mt-0.5 text-[11px] text-slate-500">Accuracy</span>
                    </div>
                  </div>

                  <div className="space-y-3.5">
                    <p className="text-xs text-slate-500">What drives the result</p>
                    {[["Feature A", 88], ["Feature B", 66], ["Feature C", 47], ["Feature D", 29]].map(([n, w], i) => (
                      <div key={n}>
                        <div className="mb-1.5 flex justify-between text-xs text-slate-400"><span>{n}</span><span>{w}%</span></div>
                        <div className="h-1.5 rounded-full bg-white/[0.06]">
                          <div className="h-full origin-left rounded-full bg-gradient-to-r from-[#5563a8] to-[#c7d4ea]" style={{ width: `${w}%`, animation: `dl-grow 1.2s ${0.9 + i * 0.15}s cubic-bezier(.2,.7,.2,1) both` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-5 rounded-2xl border border-white/[0.07] bg-white/[0.025] p-5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-500">Prediction confidence over validation folds</span>
                    <span className="rounded-full bg-emerald-400/10 px-2.5 py-1 text-emerald-300">Strong fit</span>
                  </div>
                  <svg viewBox="0 0 500 110" className="mt-4 h-24 w-full" fill="none" aria-hidden>
                    <defs>
                      <linearGradient id="dl-a" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#a9bbd8" stopOpacity=".28" /><stop offset="1" stopColor="#a9bbd8" stopOpacity="0" /></linearGradient>
                      <linearGradient id="dl-l" x1="0" x2="1"><stop offset="0" stopColor="#6b7bbd" /><stop offset="1" stopColor="#e1e9f6" /></linearGradient>
                    </defs>
                    <path d="M0 92 C50 86 80 70 130 68 S200 74 250 52 S340 44 390 28 S460 14 500 8 V110 H0Z" fill="url(#dl-a)" />
                    <path d="M0 92 C50 86 80 70 130 68 S200 74 250 52 S340 44 390 28 S460 14 500 8" stroke="url(#dl-l)" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="900" style={{ animation: "dl-draw 2.2s .7s ease-out both" }} />
                  </svg>
                </div>
              </div>
            </div>

            {/* floating insight chip */}
            <div className="absolute -bottom-6 -left-4 hidden max-w-[240px] rounded-2xl border border-white/10 bg-[#0f192d]/90 p-4 shadow-2xl backdrop-blur-xl sm:block" style={{ animation: "dl-float 7s ease-in-out infinite" }}>
              <p className="text-[11px] text-[#c9b98a]">AI briefing</p>
              <p className="mt-1.5 text-[13px] leading-5 text-slate-300">Feature A explains most of the outcome. Prioritise it in next quarter&apos;s plan.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ================= CAPABILITIES ================= */}
      <section className="mx-auto max-w-[1280px] px-6 pb-4 pt-24 lg:px-10 lg:pt-32">
        <div className="max-w-2xl">
          <h2 className={`${serif} text-[2.3rem] font-light leading-[1.08] tracking-[-0.035em] sm:text-[3.2rem]`}>One workflow, from first look to final briefing.</h2>
          <p className="mt-5 max-w-lg text-base leading-7 text-[#5b6173]">Each layer builds on the last, so every number in the report can be traced back to your data.</p>
        </div>

        <div className="mt-14 grid gap-5 lg:grid-cols-6">
          <Bento cls="lg:col-span-4" serif={serif} title="Profile and explore" text="Schema, missing values, distributions and correlations are checked before any model is trained.">
            <div className="mt-10 grid h-24 grid-cols-12 items-end gap-1.5">
              {[34, 52, 70, 88, 100, 82, 64, 46, 58, 40, 26, 18].map((h, i) => (
                <span key={i} className="rounded-t-md bg-gradient-to-t from-[#4d5b9e]/20 to-[#4d5b9e] transition-all duration-500 group-hover:to-[#a9bbd8]" style={{ height: `${h}%`, opacity: 0.45 + h / 190 }} />
              ))}
            </div>
          </Bento>

          <Bento cls="lg:col-span-2" dark serif={serif} title="Predict" text="Classification or regression, detected and trained for you.">
            <p className={`${serif} mt-10 text-7xl font-light tracking-tight text-[#e1e9f6]`}>Auto</p>
          </Bento>

          <Bento cls="lg:col-span-2" serif={serif} title="Explain" text="Feature impact and diagnostics, so every result can be trusted.">
            <div className="mt-10 space-y-2.5">
              {[88, 62, 41].map((w, i) => (
                <div key={w} className="h-2 rounded-full bg-[#0c1424]/[0.07]">
                  <div className="h-full rounded-full bg-gradient-to-r from-[#4d5b9e] to-[#a9bbd8]" style={{ width: `${w}%`, opacity: 1 - i * 0.2 }} />
                </div>
              ))}
            </div>
          </Bento>

          <Bento cls="lg:col-span-4" serif={serif} title="Brief the business" text="KPIs, key findings and an AI-written summary, grounded in the analysis rather than guesswork.">
            <div className="mt-10 grid gap-5 sm:grid-cols-[auto_1fr] sm:items-center">
              <div className="flex gap-3">
                {["12%", "3.4×", "8"].map((v) => (
                  <div key={v} className="flex h-16 w-20 flex-col justify-center rounded-2xl border border-[#e3e0d6] bg-[#faf9f5] px-3">
                    <span className="h-1.5 w-8 rounded-full bg-[#4d5b9e]/40" />
                    <span className={`${serif} mt-2 text-lg text-[#0c1424]`}>{v}</span>
                  </div>
                ))}
              </div>
              <div className="space-y-2.5">
                {[100, 86, 64].map((w) => <span key={w} className="block h-2 rounded-full bg-[#0c1424]/10" style={{ width: `${w}%` }} />)}
              </div>
            </div>
          </Bento>
        </div>
      </section>

      {/* ================= WORKSPACE ================= */}
      <main id="workspace" className="mx-auto max-w-[1360px] scroll-mt-20 px-6 py-24 lg:px-10 lg:py-32">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className={`${serif} text-[2.4rem] font-light leading-tight tracking-[-0.035em] sm:text-[3.4rem]`}>Analysis workspace</h2>
            <p className="mt-3 max-w-xl text-base leading-7 text-[#5b6173]">Add a dataset, choose a target, and DataLens takes it from there.</p>
          </div>
          <div role="status" aria-live="polite" className="flex w-fit items-center gap-3 rounded-full border border-[#e3e0d6] bg-white py-2.5 pl-4 pr-6 shadow-[0_8px_24px_-14px_rgba(12,20,36,.25)]">
            <span className={`h-2.5 w-2.5 rounded-full ${isAnalyzing ? "animate-pulse bg-[#4d5b9e]" : dataset ? "bg-emerald-500" : "bg-slate-300"}`} />
            <span className="text-sm font-medium">{workspaceStatus}</span>
          </div>
        </div>

        <div className="relative mt-12 overflow-hidden rounded-[32px] border border-[#e3e0d6] bg-white shadow-[0_2px_4px_rgba(12,20,36,.04),0_70px_120px_-50px_rgba(12,20,36,.35)]">
          {/* stepper with connected progress line */}
          <div className="relative border-b border-[#ece9e0] bg-[#faf9f5]">
            <div aria-hidden className="absolute inset-x-0 bottom-0 h-[2px] bg-[#ece9e0]">
              <div className="h-full bg-gradient-to-r from-[#4d5b9e] to-[#a9bbd8] transition-all duration-700 ease-out" style={{ width: `${(stepsDone / 4) * 100}%` }} />
            </div>
            <div className="grid md:grid-cols-4">
              <Step n="1" title="Dataset" detail="Upload your CSV" state={st(Boolean(dataset), !dataset)} />
              <Step n="2" title="Profile" detail="Check the structure" state={st(Boolean(dataset), false)} />
              <Step n="3" title="Configure" detail="Choose a target" state={st(Boolean(analysisResult), Boolean(dataset))} />
              <Step n="4" title="Analyze" detail="Generate results" state={st(Boolean(analysisResult), isAnalyzing)} last />
            </div>
          </div>

          <div className="grid min-h-[480px] lg:grid-cols-[290px_minmax(0,1fr)]">
            <aside className="hidden border-r border-[#ece9e0] bg-[#faf9f5] p-8 lg:block">
              <div className="sticky top-24">
                <p className="text-sm font-semibold">Included automatically</p>
                <ul className="mt-5 space-y-4">
                  {["Data profiling", "Exploratory analysis", "Feature engineering", "Model evaluation", "Explainability", "Business intelligence"].map((m) => (
                    <li key={m} className="flex items-center gap-3 text-sm text-[#5b6173]">
                      <span className="flex h-5 w-5 items-center justify-center rounded-full bg-[#0c1424] text-[10px] text-white">✓</span>
                      {m}
                    </li>
                  ))}
                </ul>
                <div className="relative mt-10 overflow-hidden rounded-2xl bg-gradient-to-br from-[#0c1424] to-[#1a2744] p-6 shadow-[0_24px_50px_-24px_rgba(12,20,36,.6)]">
                  <span aria-hidden className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent" />
                  <span aria-hidden className="absolute -right-8 -top-8 h-24 w-24 rounded-full bg-[#4d5b9e]/40 blur-2xl" />
                  <p className={`${serif} relative text-xl font-light italic leading-snug text-white`}>Evidence first. Interpretation second.</p>
                </div>
              </div>
            </aside>

            <div className="min-w-0">
              <Block serif={serif} title="Connect your dataset" description="Upload a structured CSV file to begin." status={dataset ? "Connected" : "Required"} complete={Boolean(dataset)}>
                <UploadDataset onUploadSuccess={handleUploadSuccess} />
              </Block>

              {dataset && (
                <Block serif={serif} title="Dataset overview" description="Confirm the size and columns look right." status="Verified" complete>
                  <DatasetOverview dataset={dataset} />
                </Block>
              )}

              {dataset && (
                <Block serif={serif} title="Choose what to predict" description="Select the target column. Problem type and model settings are detected for you." status={isAnalyzing ? "Processing" : analysisResult ? "Complete" : "Ready"} complete={Boolean(analysisResult)} processing={isAnalyzing}>
                  <AnalysisConfig dataset={dataset} onRunAnalysis={handleRunAnalysis} isAnalyzing={isAnalyzing} />
                </Block>
              )}

              {isAnalyzing && (
                <div className="relative border-t border-[#ece9e0] bg-gradient-to-b from-[#eef0f8] to-white p-8 sm:p-10">
                  <span aria-hidden className="absolute inset-x-0 top-0 h-[2px] bg-gradient-to-r from-transparent via-[#4d5b9e] to-transparent" />
                  <div className="mb-7 flex items-center justify-between">
                    <div>
                      <h3 className={`${serif} text-2xl font-normal tracking-[-0.02em]`}>Building your analysis</h3>
                      <p className="mt-1 text-sm text-[#5b6173]">Larger datasets can take a minute.</p>
                    </div>
                    <span className="hidden items-center gap-2 rounded-full bg-[#4d5b9e]/10 px-4 py-2 text-xs font-medium text-[#3d4a86] sm:flex">
                      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-[#4d5b9e]" />
                      Processing
                    </span>
                  </div>
                  <AnalysisProgress isAnalyzing={isAnalyzing} />
                </div>
              )}
            </div>
          </div>
        </div>

        {analysisError && (
          <div role="alert" className="mt-8 flex items-start gap-4 rounded-3xl border border-red-200 bg-red-50 p-6">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-100 font-bold text-red-700">!</div>
            <div>
              <p className="font-semibold">Analysis could not be completed</p>
              <p className="mt-1 text-sm leading-6 text-slate-600">{analysisError}</p>
            </div>
          </div>
        )}

        {analysisResult && (
          <section className="mt-28">
            <Heading serif={serif} title="Analysis results" description="Performance, diagnostics, explainability, business intelligence and AI interpretation." status="Complete" />
            <div className="mt-12">
              {/* DO NOT MODIFY RESULTS DASHBOARD */}
              <ResultsDashboard result={analysisResult} />
            </div>
          </section>
        )}

        <section id="archive" className="mt-28 scroll-mt-20">
          <Heading serif={serif} title="Analysis archive" description="Reopen reports you've generated before." status="History" />
          <div className="mt-12">
            <AnalysisHistory key={historyRefreshKey} />
          </div>
        </section>
      </main>

      {/* ================= FOOTER ================= */}
      <footer className="relative overflow-hidden bg-[#060a13]">
        <span aria-hidden className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/50 to-transparent" />
        <div aria-hidden className="absolute -bottom-32 left-1/2 h-64 w-[700px] -translate-x-1/2 rounded-full bg-[#4d5b9e]/20 blur-[100px]" />
        <div className="relative mx-auto flex max-w-[1360px] flex-col gap-8 px-6 py-16 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <div className="flex items-center gap-4">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#e4e9f5] to-[#a9bbd8] text-sm font-bold text-[#060a13]">DL</div>
            <div>
              <p className="font-semibold text-white">DataLens AI</p>
              <p className="text-xs text-slate-500">From raw data to evidence-backed insight.</p>
            </div>
          </div>
          <p className={`${serif} text-xl font-light italic text-slate-400`}>Profile. Model. Explain. Decide.</p>
        </div>
      </footer>
    </div>
  );
}

// ============================================================
// SMALL COMPONENTS
// ============================================================

type State = "active" | "complete" | "pending";

function Bento({ cls, serif, title, text, children, dark = false }: { cls: string; serif: string; title: string; text: string; children: React.ReactNode; dark?: boolean }) {
  return (
    <div
      className={`group relative overflow-hidden rounded-[28px] border p-8 transition duration-500 hover:-translate-y-1 ${
        dark
          ? "border-white/10 bg-gradient-to-br from-[#0c1424] to-[#1a2744] text-white shadow-[0_30px_60px_-30px_rgba(12,20,36,.7)]"
          : "border-[#e3e0d6] bg-white shadow-[0_1px_2px_rgba(12,20,36,.04)] hover:shadow-[0_40px_70px_-40px_rgba(12,20,36,.35)]"
      } ${cls}`}
    >
      {dark && <span aria-hidden className="absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent" />}
      <h3 className={`${serif} text-[1.7rem] font-normal tracking-[-0.02em]`}>{title}</h3>
      <p className={`mt-2 max-w-md text-sm leading-6 ${dark ? "text-slate-400" : "text-[#5b6173]"}`}>{text}</p>
      {children}
    </div>
  );
}

function Step({ n, title, detail, state, last = false }: { n: string; title: string; detail: string; state: State; last?: boolean }) {
  const complete = state === "complete";
  const active = state === "active";
  return (
    <div className={`relative px-7 py-6 ${last ? "" : "border-b border-[#ece9e0] md:border-b-0 md:border-r"} ${active ? "bg-white" : ""}`}>
      {active && <span className="absolute inset-x-0 top-0 h-[3px] bg-gradient-to-r from-[#4d5b9e] to-[#a9bbd8]" />}
      <div className="flex items-center gap-4">
        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-semibold transition-all duration-500 ${complete ? "bg-[#0c1424] text-white shadow-[0_8px_18px_-8px_rgba(12,20,36,.7)]" : active ? "bg-[#4d5b9e]/10 text-[#3d4a86] ring-4 ring-[#4d5b9e]/10" : "bg-slate-100 text-slate-400"}`}>
          {complete ? "✓" : n}
        </div>
        <div>
          <p className={`text-sm font-semibold ${complete || active ? "text-[#0c1424]" : "text-slate-400"}`}>{title}</p>
          <p className="mt-0.5 text-xs text-slate-400">{detail}</p>
        </div>
      </div>
    </div>
  );
}

function Block({ serif, title, description, status, complete = false, processing = false, children }: { serif: string; title: string; description: string; status: string; complete?: boolean; processing?: boolean; children: React.ReactNode }) {
  return (
    <section className="border-b border-[#ece9e0] last:border-b-0">
      <div className="flex flex-col gap-3 px-7 pt-9 sm:flex-row sm:items-start sm:justify-between sm:px-10">
        <div>
          <h3 className={`${serif} text-2xl font-normal tracking-[-0.02em]`}>{title}</h3>
          <p className="mt-1.5 max-w-xl text-sm leading-6 text-[#5b6173]">{description}</p>
        </div>
        <span className={`inline-flex w-fit shrink-0 items-center gap-2 rounded-full px-3.5 py-1.5 text-xs font-medium ${complete ? "bg-emerald-50 text-emerald-700" : processing ? "bg-[#4d5b9e]/10 text-[#3d4a86]" : "bg-slate-100 text-slate-500"}`}>
          <span className={`h-1.5 w-1.5 rounded-full ${complete ? "bg-emerald-500" : processing ? "animate-pulse bg-[#4d5b9e]" : "bg-slate-400"}`} />
          {status}
        </span>
      </div>
      <div className="px-7 pb-10 pt-7 sm:px-10">{children}</div>
    </section>
  );
}

function Heading({ serif, title, description, status }: { serif: string; title: string; description: string; status: string }) {
  return (
    <div className="relative flex flex-col gap-4 border-b border-[#e3e0d6] pb-8 sm:flex-row sm:items-end sm:justify-between">
      <span aria-hidden className="absolute -bottom-px left-0 h-px w-24 bg-[#c9b98a]" />
      <div>
        <h2 className={`${serif} text-[2.1rem] font-light tracking-[-0.035em] sm:text-[2.9rem]`}>{title}</h2>
        <p className="mt-2 max-w-2xl text-base leading-7 text-[#5b6173]">{description}</p>
      </div>
      <span className="w-fit rounded-full border border-[#e3e0d6] bg-white px-4 py-1.5 text-xs font-medium text-[#5b6173]">{status}</span>
    </div>
  );
}