"use client";

// ==========================================
// DATALENS AI - RESULTS DASHBOARD V7
// Premium Executive Analytics Workspace
// ==========================================

import { useEffect, useState } from "react";

import { getReportUrl } from "@/lib/api";

import type { AnalysisResponse, ModelComparisonRow } from "@/types";

interface ResultsDashboardProps {
  result: AnalysisResponse;
}

// ==========================================
// FORMATTERS
// ==========================================

function formatPercent(value?: number) {
  if (value === undefined || Number.isNaN(value)) {
    return "—";
  }

  return `${(value * 100).toFixed(1)}%`;
}

function formatNumber(value?: number) {
  if (value === undefined || Number.isNaN(value)) {
    return "—";
  }

  return value.toLocaleString(undefined, { maximumFractionDigits: 3 });
}

function getModelMetric(row: ModelComparisonRow, key: string) {
  const value = row[key];

  return typeof value === "number" ? value : undefined;
}

function getCvMetric<T>(row: T, key: string) {
  const value = (row as unknown as Record<string, unknown>)[key];

  return typeof value === "number" ? value : undefined;
}

function getDataQualityScore(
  missing: number,
  duplicates: number,
  rows: number,
  columns: number
) {
  const totalCells = Math.max(rows * columns, 1);
  const missingPenalty = (missing / totalCells) * 100;
  const duplicatePenalty = rows > 0 ? (duplicates / rows) * 100 : 0;

  return Math.max(0, Math.min(100, 100 - missingPenalty - duplicatePenalty));
}

const clamp = (n: number) => Math.max(0, Math.min(n, 100));

// ==========================================
// MAIN
// ==========================================

export default function ResultsDashboard({ result }: ResultsDashboardProps) {
  const reportUrl = getReportUrl(result.report_url);

  const { dataset_summary, dashboard } = result;

  const evaluation = dashboard.evaluation;
  const modelComparison = dashboard.model_comparison ?? [];
  const crossValidation = dashboard.cross_validation ?? [];
  const explainability = dashboard.explainability;
  const explanationFeatures = explainability?.features ?? [];
  const businessFindings = dashboard.business_findings?.findings ?? [];
  const businessKPIs = dashboard.business_kpis;
  const targetDistribution = businessKPIs?.target_kpi?.distribution;

  const dataQuality = getDataQualityScore(
    dataset_summary.missing_values,
    dataset_summary.duplicate_rows,
    dataset_summary.rows,
    dataset_summary.columns
  );

  const isClassification = result.problem_type === "Classification";

  const positiveClass =
    result.positive_class !== null && result.positive_class !== undefined
      ? String(result.positive_class)
      : "Automatic";

  const navLinks = [
    ["#analysis-overview", "Overview"],
    ["#model-performance", "Performance"],
    ["#model-benchmark", "Models"],
    ["#explainability", "Explainability"],
    ["#business-intelligence", "Business"],
    ["#ai-analyst", "AI Analyst"],
    ["#full-report", "Report"],
  ];

  // Highlight the link for the section currently on screen
  const [activeSection, setActiveSection] = useState("#analysis-overview");

  useEffect(() => {
    const targets = navLinks
      .map(([href]) => document.querySelector(href))
      .filter((el): el is Element => el !== null);
    if (targets.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) setActiveSection(`#${entry.target.id}`);
        });
      },
      { rootMargin: "-30% 0px -60% 0px" }
    );

    targets.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result.analysis_id]);

  // Best candidate model (F1 for classification, R² for regression)
  const modelScores = modelComparison.map((model) =>
    isClassification
      ? getModelMetric(model, "F1 Score")
      : (getModelMetric(model, "R2 Score") ?? getModelMetric(model, "R2"))
  );
  let bestModelIndex = -1;
  modelScores.forEach((score, i) => {
    if (score === undefined || Number.isNaN(score)) return;
    if (bestModelIndex === -1 || score > (modelScores[bestModelIndex] as number)) {
      bestModelIndex = i;
    }
  });
  if (modelComparison.length < 2) bestModelIndex = -1;

  return (
    <section className="w-full space-y-6">
      {/* ==================================
          EXECUTIVE HERO
      ================================== */}

      <section
        id="analysis-overview"
        className="relative isolate scroll-mt-28 overflow-hidden rounded-[32px] border border-white/10 bg-[#060a13] text-white shadow-[0_50px_120px_-40px_rgba(6,10,19,.8)]"
      >
        <div aria-hidden className="pointer-events-none absolute -left-24 -top-32 -z-10 h-96 w-96 rounded-full bg-[#4d5b9e]/40 blur-[120px]" />
        <div aria-hidden className="pointer-events-none absolute -bottom-32 right-10 -z-10 h-80 w-80 rounded-full bg-[#a9bbd8]/15 blur-[120px]" />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 -z-10 opacity-[0.05]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,.9) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.9) 1px,transparent 1px)",
            backgroundSize: "64px 64px",
            WebkitMaskImage: "radial-gradient(ellipse at 30% 20%,#000,transparent 70%)",
            maskImage: "radial-gradient(ellipse at 30% 20%,#000,transparent 70%)",
          }}
        />
        <span aria-hidden className="absolute inset-x-12 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent" />

        <div className="flex flex-col gap-3 border-b border-white/10 px-7 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-9">
          <div className="flex items-center gap-3">
            <span className="relative flex h-2 w-2">
              <span className="absolute h-full w-full animate-ping rounded-full bg-emerald-400/60" />
              <span className="relative h-2 w-2 rounded-full bg-emerald-400" />
            </span>
            <p className="text-sm font-medium text-slate-300">Analysis complete</p>
          </div>

          <p className="break-all font-mono text-[11px] text-slate-500">{result.analysis_id}</p>
        </div>

        <div className="grid xl:grid-cols-[minmax(0,1fr)_360px]">
          <div className="px-7 py-10 sm:px-9 sm:py-14">
            <p className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 text-xs font-medium text-[#a9bbd8]">
              <span className="h-1 w-1 rounded-full bg-[#c9b98a]" />
              {result.problem_type} intelligence
            </p>

            <h2 className="mt-6 max-w-3xl font-serif text-4xl font-light leading-[1.05] tracking-[-0.035em] sm:text-5xl">
              Analysis of{" "}
              <span className="bg-gradient-to-r from-[#dbe4f4] via-[#a9bbd8] to-[#dbe4f4] bg-clip-text italic text-transparent">
                {result.target_column}
              </span>
            </h2>

            <p className="mt-5 max-w-2xl text-[15px] leading-7 text-slate-400">
              DataLens has completed the end-to-end analytical workflow, combining dataset profiling, machine learning, explainability, business analytics and grounded AI interpretation.
            </p>

            <div className="mt-10 flex flex-wrap gap-x-12 gap-y-5 border-t border-white/10 pt-7">
              <HeroMeta label="Problem" value={result.problem_type} />
              <HeroMeta label="Target" value={result.target_column} />
              <HeroMeta label="Positive class" value={positiveClass} />
            </div>
          </div>

          <aside className="border-t border-white/10 bg-white/[0.03] p-7 backdrop-blur xl:border-l xl:border-t-0 sm:p-9">
            <p className="text-sm font-medium text-slate-400">Dataset health</p>

            <div className="mt-5 flex items-end justify-between">
              <div>
                <p className="datalens-number font-serif text-5xl font-light tracking-[-0.04em]">{dataQuality.toFixed(1)}</p>
                <p className="mt-1 text-xs text-slate-500">quality score / 100</p>
              </div>
              <span className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-300">Validated</span>
            </div>

            <div className="mt-5 h-1.5 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full origin-left rounded-full bg-gradient-to-r from-[#5563a8] to-[#c7d4ea]"
                style={{ width: `${dataQuality}%`, animation: "dl-grow 1.2s .2s cubic-bezier(.2,.7,.2,1) both" }}
              />
            </div>

            <div className="mt-8 grid grid-cols-2 gap-3">
              <DarkStat label="Rows" value={dataset_summary.rows.toLocaleString()} />
              <DarkStat label="Columns" value={dataset_summary.columns.toLocaleString()} />
              <DarkStat label="Missing" value={dataset_summary.missing_values.toLocaleString()} />
              <DarkStat label="Duplicates" value={dataset_summary.duplicate_rows.toLocaleString()} />
            </div>
          </aside>
        </div>
      </section>

      {/* ==================================
          RESULT NAVIGATION
      ================================== */}

      <nav aria-label="Results sections" className="sticky top-3 z-20 overflow-x-auto rounded-full border border-[#e3e0d6] bg-white/85 p-1.5 shadow-[0_16px_40px_-20px_rgba(12,20,36,.3)] backdrop-blur-xl backdrop-saturate-150">
        <div className="flex min-w-max items-center gap-1">
          {navLinks.map(([href, label]) => {
            const isActive = activeSection === href;
            return (
              <a
                key={href}
                href={href}
                aria-current={isActive ? "location" : undefined}
                className={`rounded-full px-4 py-2 text-[13px] font-medium transition duration-300 ${
                  isActive
                    ? "bg-[#0c1424] text-white shadow-[0_8px_20px_-10px_rgba(12,20,36,.6)]"
                    : "text-[#5b6173] hover:bg-[#0c1424]/[0.06] hover:text-[#0c1424]"
                }`}
              >
                {label}
              </a>
            );
          })}
        </div>
      </nav>

      {/* ==================================
          EXECUTIVE KPI STRIP
      ================================== */}

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {isClassification && evaluation ? (
          <>
            <ExecutiveMetric label="Accuracy" value={formatPercent(evaluation.accuracy)} supporting="Overall prediction accuracy" progress={evaluation.accuracy * 100} />
            <ExecutiveMetric label="F1 Score" value={formatPercent(evaluation.f1_score)} supporting="Precision-recall balance" progress={evaluation.f1_score * 100} />
          </>
        ) : (
          <>
            <ExecutiveMetric label="Records" value={dataset_summary.rows.toLocaleString()} supporting="Analyzed observations" />
            <ExecutiveMetric label="Features" value={dataset_summary.columns.toLocaleString()} supporting="Dataset columns" />
          </>
        )}

        <ExecutiveMetric label="Data Quality" value={`${dataQuality.toFixed(1)}%`} supporting="Structural dataset health" progress={dataQuality} />
        <ExecutiveMetric label="Models Tested" value={modelComparison.length.toLocaleString()} supporting="Candidate model benchmark" />
      </section>

      {/* ==================================
          PERFORMANCE
      ================================== */}

      {isClassification && evaluation && (
        <DashboardSection
          id="model-performance"
          title="Classification performance"
          description="Held-out evaluation metrics from the classification workflow."
        >
          <div className="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(300px,0.75fr)]">
            <div className="overflow-hidden rounded-2xl border border-[#ece9e0]">
              <p className="border-b border-[#ece9e0] bg-[#faf9f5] px-5 py-3.5 text-sm font-semibold">Evaluation metrics</p>
              <div className="divide-y divide-[#ece9e0]">
                <PerformanceMetric label="Accuracy" value={evaluation.accuracy} description="Correct predictions across all evaluated observations." />
                <PerformanceMetric label="Precision" value={evaluation.precision} description="Reliability of positive predictions." />
                <PerformanceMetric label="Recall" value={evaluation.recall} description="Coverage of actual positive observations." />
                <PerformanceMetric label="F1 Score" value={evaluation.f1_score} description="Harmonic balance of precision and recall." />
              </div>
            </div>

            <div className="overflow-hidden rounded-2xl border border-[#ece9e0] bg-[#faf9f5]">
              <p className="border-b border-[#ece9e0] px-5 py-3.5 text-sm font-semibold">Analysis context</p>
              <div className="divide-y divide-[#ece9e0]">
                <ContextRow label="Problem type" value={result.problem_type} />
                <ContextRow label="Target" value={result.target_column} />
                <ContextRow label="Positive class" value={positiveClass} />
                <ContextRow label="Evaluated models" value={String(modelComparison.length)} />
              </div>
            </div>
          </div>

          {evaluation.confusion_matrix?.length === 2 && (
            <div className="mt-8 grid gap-6 border-t border-[#ece9e0] pt-8 lg:grid-cols-[280px_minmax(0,560px)]">
              <div>
                <h4 className="font-serif text-xl tracking-[-0.02em]">Confusion matrix</h4>
                <p className="mt-2 text-sm leading-6 text-[#5b6173]">
                  Raw prediction counts from the held-out test set. Classes remain in the ordering returned by the model. Darker cells hold a larger share of the predictions.
                </p>
              </div>

              <div className="rounded-2xl border border-[#ece9e0] bg-[#faf9f5] p-5">
                <p className="mb-3 text-center text-xs font-medium text-[#9a9eaf]">Predicted class</p>

                <div className="flex gap-3">
                  <div className="flex w-6 shrink-0 items-center justify-center">
                    <span className="-rotate-90 whitespace-nowrap text-xs font-medium text-[#9a9eaf]">Actual class</span>
                  </div>

                  <div className="grid flex-1 grid-cols-2 gap-3">
                    {(() => {
                      const cells = evaluation.confusion_matrix.flat();
                      const total = Math.max(
                        cells.reduce((sum, v) => sum + Number(v || 0), 0),
                        1
                      );

                      return cells.map((value, index) => {
                        const row = Math.floor(index / 2) + 1;
                        const column = (index % 2) + 1;
                        const correct = row === column;
                        const share = Number(value || 0) / total;

                        return (
                          <div
                            key={index}
                            className={`relative overflow-hidden rounded-2xl border px-4 py-7 text-center transition duration-300 hover:-translate-y-0.5 ${
                              correct ? "border-[#4d5b9e]/30" : "border-[#ece9e0] bg-white"
                            }`}
                            style={
                              correct
                                ? { background: `linear-gradient(135deg, rgba(77,91,158,${0.06 + share * 0.3}), #fff)` }
                                : undefined
                            }
                          >
                            <p className={`datalens-number font-serif text-4xl font-light tracking-[-0.03em] ${correct ? "text-[#3d4a86]" : "text-[#0c1424]"}`}>
                              {value}
                            </p>
                            <p className="mt-2 text-[11px] text-[#9a9eaf]">
                              Actual {row} / Predicted {column}
                            </p>
                          </div>
                        );
                      });
                    })()}
                  </div>
                </div>
              </div>
            </div>
          )}
        </DashboardSection>
      )}

      {/* ==================================
          MODEL BENCHMARK
      ================================== */}

      {modelComparison.length > 0 && (
        <DashboardSection
          id="model-benchmark"
          title="Candidate model comparison"
          description="Side-by-side performance of the models evaluated by the DataLens ML engine."
        >
          <DataTable heads={isClassification ? ["Model", "Accuracy", "Precision", "Recall", "F1 Score"] : ["Model", "MAE", "RMSE", "R²"]}>
            {modelComparison.map((model, index) => (
              <tr key={`${model.Model}-${index}`} className={`transition-colors hover:bg-[#faf9f5] ${index === bestModelIndex ? "bg-[#eef0f8]/50" : ""}`}>
                <TableCell strong>
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-[11px] text-[#9a9eaf]">{String(index + 1).padStart(2, "0")}</span>
                    {model.Model}
                    {index === bestModelIndex && (
                      <span className="rounded-full bg-[#4d5b9e]/10 px-2.5 py-0.5 text-[11px] font-medium text-[#3d4a86]">
                        Top performer
                      </span>
                    )}
                  </div>
                </TableCell>

                {isClassification ? (
                  <>
                    <TableCell>{formatPercent(getModelMetric(model, "Accuracy"))}</TableCell>
                    <TableCell>{formatPercent(getModelMetric(model, "Precision"))}</TableCell>
                    <TableCell>{formatPercent(getModelMetric(model, "Recall"))}</TableCell>
                    <TableCell>{formatPercent(getModelMetric(model, "F1 Score"))}</TableCell>
                  </>
                ) : (
                  <>
                    <TableCell>{formatNumber(getModelMetric(model, "MAE"))}</TableCell>
                    <TableCell>{formatNumber(getModelMetric(model, "RMSE"))}</TableCell>
                    <TableCell>
                      {formatNumber(getModelMetric(model, "R2 Score") ?? getModelMetric(model, "R2"))}
                    </TableCell>
                  </>
                )}
              </tr>
            ))}
          </DataTable>

          {crossValidation.length > 0 && (
            <div className="mt-8 border-t border-[#ece9e0] pt-8">
              <div className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
                <h4 className="font-serif text-xl tracking-[-0.02em]">Cross-validation summary</h4>
                <p className="text-xs text-[#9a9eaf]">Generalization evidence across validation folds</p>
              </div>

              <DataTable heads={isClassification ? ["Model", "CV Accuracy", "CV Precision", "CV Recall", "CV F1"] : ["Model", "CV MAE", "CV RMSE", "CV R²"]}>
                {crossValidation.map((row, index) => (
                  <tr key={`${row.Model}-${index}`} className="transition-colors hover:bg-[#faf9f5]">
                    <TableCell strong>{row.Model}</TableCell>

                    {isClassification ? (
                      <>
                        <TableCell>{formatPercent(getCvMetric(row, "CV Accuracy"))}</TableCell>
                        <TableCell>{formatPercent(getCvMetric(row, "CV Precision"))}</TableCell>
                        <TableCell>{formatPercent(getCvMetric(row, "CV Recall"))}</TableCell>
                        <TableCell>{formatPercent(getCvMetric(row, "CV F1 Score"))}</TableCell>
                      </>
                    ) : (
                      <>
                        <TableCell>{formatNumber(getCvMetric(row, "CV MAE"))}</TableCell>
                        <TableCell>{formatNumber(getCvMetric(row, "CV RMSE"))}</TableCell>
                        <TableCell>{formatNumber(getCvMetric(row, "CV R2"))}</TableCell>
                      </>
                    )}
                  </tr>
                ))}
              </DataTable>
            </div>
          )}
        </DashboardSection>
      )}

      {/* ==================================
          TARGET DISTRIBUTION
      ================================== */}

      {targetDistribution && (
        <DashboardSection
          id="target-distribution"
          title="Target distribution"
          description="Observed distribution of the selected outcome variable."
        >
          <div className="divide-y divide-[#ece9e0] overflow-hidden rounded-2xl border border-[#ece9e0]">
            {Object.entries(targetDistribution).map(([label, percentage]) => (
              <div key={label} className="grid gap-3 bg-white px-5 py-4 transition-colors hover:bg-[#faf9f5] sm:grid-cols-[180px_minmax(0,1fr)_80px] sm:items-center">
                <p className="truncate text-sm font-semibold">{label}</p>
                <Bar value={percentage} />
                <p className="datalens-number text-right text-sm font-semibold">{percentage.toFixed(1)}%</p>
              </div>
            ))}
          </div>
        </DashboardSection>
      )}

      {/* ==================================
          EXPLAINABILITY
      ================================== */}

      {explanationFeatures.length > 0 && (
        <DashboardSection
          id="explainability"
          title="Model explainability"
          description={
            explainability?.explanation_type
              ? `Explanation method: ${explainability.explanation_type}. Feature influence is model-specific and does not establish causation.`
              : "Ranked model feature influence. Importance does not establish causation."
          }
        >
          <div className="grid gap-8 lg:grid-cols-[260px_minmax(0,1fr)]">
            <aside>
              <p className="text-sm leading-6 text-[#5b6173]">
                This view identifies the features with the strongest influence inside the fitted model. Interpret the ranking as model evidence, not as causal business impact.
              </p>

              {explainability?.model && (
                <div className="mt-6 border-t border-[#ece9e0] pt-5">
                  <p className="text-xs font-medium text-[#9a9eaf]">Explained model</p>
                  <p className="mt-2 text-sm font-semibold">{explainability.model}</p>
                </div>
              )}
            </aside>

            <div className="divide-y divide-[#ece9e0] overflow-hidden rounded-2xl border border-[#ece9e0]">
              {explanationFeatures.slice(0, 8).map((feature, index) => {
                const magnitude = feature["Absolute Coefficient"] ?? feature.Importance ?? 0;

                const maxMagnitude = Math.max(
                  ...explanationFeatures.map(
                    (item) => item["Absolute Coefficient"] ?? item.Importance ?? 0
                  ),
                  1
                );

                const width = (magnitude / maxMagnitude) * 100;

                return (
                  <div key={`${feature.Feature}-${index}`} className="grid gap-3 bg-white px-5 py-4 transition-colors hover:bg-[#faf9f5] sm:grid-cols-[36px_minmax(0,1fr)_100px] sm:items-center">
                    <span className="font-mono text-[11px] font-semibold text-[#9a9eaf]">{String(index + 1).padStart(2, "0")}</span>

                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold" title={feature.Feature}>{feature.Feature}</p>
                      <div className="mt-2.5"><Bar value={width} thin /></div>
                    </div>

                    <p className="text-right font-mono text-xs font-semibold text-[#5b6173]">
                      {feature.Coefficient !== undefined
                        ? feature.Coefficient.toFixed(4)
                        : feature.Importance !== undefined
                          ? feature.Importance.toFixed(4)
                          : "—"}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </DashboardSection>
      )}

      {/* ==================================
          BUSINESS INTELLIGENCE
      ================================== */}

      {businessFindings.length > 0 && (
        <DashboardSection
          id="business-intelligence"
          title="Evidence-backed findings"
          description={`${dashboard.business_findings?.total_findings ?? businessFindings.length} findings generated from deterministic dataset analysis.`}
        >
          <div className="grid gap-4 lg:grid-cols-2">
            {businessFindings.slice(0, 8).map((finding, index) => (
              <article key={index} className="group relative flex gap-4 overflow-hidden rounded-2xl border border-[#ece9e0] bg-white p-5 transition duration-300 hover:-translate-y-0.5 hover:border-[#4d5b9e]/30 hover:shadow-[0_24px_50px_-28px_rgba(77,91,158,.5)]">
                <span aria-hidden className="absolute inset-y-0 left-0 w-[3px] origin-top scale-y-0 bg-gradient-to-b from-[#4d5b9e] to-[#a9bbd8] transition-transform duration-500 group-hover:scale-y-100" />
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#4d5b9e]/10 font-mono text-[11px] font-bold text-[#3d4a86]">
                  {String(index + 1).padStart(2, "0")}
                </div>

                <div>
                  <p className="text-xs font-medium text-[#9a9eaf]">Analytical finding</p>
                  <p className="mt-1.5 text-sm leading-6 text-[#2b3147]">{finding}</p>
                </div>
              </article>
            ))}
          </div>
        </DashboardSection>
      )}

      {/* ==================================
          AI ANALYST
      ================================== */}

      {dashboard.ai_analysis && (
        <DashboardSection
          id="ai-analyst"
          title="AI Analyst briefing"
          description="Grounded interpretation of the evidence calculated by the DataLens analytics pipeline."
        >
          <div className="overflow-hidden rounded-2xl border border-[#ece9e0] lg:grid lg:grid-cols-[250px_minmax(0,1fr)]">
            <aside className="relative overflow-hidden border-b border-[#ece9e0] bg-gradient-to-br from-[#0c1424] to-[#1a2744] p-7 text-white lg:border-b-0 lg:border-r">
              <span aria-hidden className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent" />
              <div aria-hidden className="absolute -left-10 -top-10 h-36 w-36 rounded-full bg-[#4d5b9e]/50 blur-3xl" />
              <div className="relative">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-[#e4e9f5] to-[#a9bbd8] font-mono text-xs font-bold text-[#060a13] ring-1 ring-white/30">AI</div>
                <p className="mt-6 text-xs font-medium text-slate-400">Analyst principle</p>
                <p className="mt-2 font-serif text-xl font-light italic leading-snug">Evidence first. Interpretation second.</p>
                <p className="mt-6 border-t border-white/10 pt-5 text-xs leading-5 text-slate-400">
                  Model metrics are calculated by the analytics pipeline. The AI layer explains those results rather than inventing them.
                </p>
              </div>
            </aside>

            <div className="bg-white p-6 sm:p-9">
              <div className="max-h-[42rem] overflow-y-auto pr-2">
                <MarkdownContent content={dashboard.ai_analysis} />
              </div>
            </div>
          </div>
        </DashboardSection>
      )}

      {/* ==================================
          REPORT CTA
      ================================== */}

      <section id="full-report" className="relative isolate scroll-mt-28 overflow-hidden rounded-[28px] bg-gradient-to-br from-[#0c1424] via-[#111c36] to-[#1a2744] text-white shadow-[0_40px_90px_-40px_rgba(12,20,36,.7)]">
        <span aria-hidden className="absolute inset-x-12 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/70 to-transparent" />
        <div aria-hidden className="pointer-events-none absolute -right-20 -top-24 -z-10 h-72 w-72 rounded-full bg-[#4d5b9e]/40 blur-[90px]" />

        <div className="flex flex-col gap-6 px-7 py-9 sm:px-10 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-start gap-5">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[#e4e9f5] to-[#a9bbd8] text-lg text-[#060a13] shadow-[0_16px_36px_-14px_rgba(169,187,216,.6)]">↗</div>

            <div>
              <p className="text-xs font-medium text-[#c9b98a]">Analysis deliverable</p>
              <h3 className="mt-1 font-serif text-2xl tracking-[-0.02em]">Complete DataLens report</h3>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
                Open the complete analytical report containing detailed results, explainability, business analysis, AI interpretation and analytical limitations.
              </p>
            </div>
          </div>

          <a
            href={reportUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="group inline-flex h-13 min-w-[210px] shrink-0 items-center justify-center rounded-full bg-[#f5f4ef] px-7 py-3.5 text-sm font-semibold text-[#060a13] shadow-[0_18px_40px_-16px_rgba(169,187,216,.6)] transition duration-300 hover:-translate-y-0.5 hover:bg-white focus:outline-none focus-visible:ring-2 focus-visible:ring-[#a9bbd8] focus-visible:ring-offset-2 focus-visible:ring-offset-[#0c1424]"
          >
            Open Full Report
            <span className="ml-3 transition-transform group-hover:translate-x-1">→</span>
          </a>
        </div>
      </section>

      {/* ==================================
          ANALYSIS METADATA
      ================================== */}

      <footer className="flex flex-col gap-2 border-t border-[#e3e0d6] pt-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-xs font-medium text-[#9a9eaf]">DataLens analysis reference</p>
        <p className="break-all font-mono text-[11px] text-[#9a9eaf]">{result.analysis_id}</p>
      </footer>
    </section>
  );
}

// ==========================================
// DASHBOARD SECTION
// ==========================================

function DashboardSection({
  id,
  title,
  description,
  children,
}: {
  id: string;
  title: string;
  description: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-28 overflow-hidden rounded-[28px] border border-[#e3e0d6] bg-white shadow-[0_2px_4px_rgba(12,20,36,.03),0_40px_80px_-50px_rgba(12,20,36,.28)]">
      <header className="relative flex flex-col gap-2 border-b border-[#ece9e0] bg-gradient-to-b from-[#faf9f5] to-white px-7 py-6 sm:px-9 xl:flex-row xl:items-end xl:justify-between">
        <span aria-hidden className="absolute -bottom-px left-7 h-px w-16 bg-[#c9b98a] sm:left-9" />
        <h3 className="font-serif text-[1.7rem] font-normal tracking-[-0.025em]">{title}</h3>
        <p className="max-w-2xl text-sm leading-6 text-[#5b6173] xl:text-right">{description}</p>
      </header>

      <div className="p-6 sm:p-9">{children}</div>
    </section>
  );
}

// ==========================================
// SMALL HELPERS
// ==========================================

function HeroMeta({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1.5 text-sm font-semibold text-white">{value}</p>
    </div>
  );
}

function DarkStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-white/[0.08] bg-white/[0.04] p-4 transition duration-300 hover:bg-white/[0.07]">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="datalens-number mt-2 text-xl font-semibold text-white">{value}</p>
    </div>
  );
}

function Bar({ value, thin = false }: { value: number; thin?: boolean }) {
  return (
    <div className={`overflow-hidden rounded-full bg-[#ece9e0] ${thin ? "h-1.5" : "h-2"}`}>
      <div
        className="h-full origin-left rounded-full bg-gradient-to-r from-[#4d5b9e] to-[#a9bbd8]"
        style={{ width: `${clamp(value)}%`, animation: "dl-grow 1s cubic-bezier(.2,.7,.2,1) both" }}
      />
    </div>
  );
}

function ExecutiveMetric({
  label,
  value,
  supporting,
  progress,
}: {
  label: string;
  value: string;
  supporting: string;
  progress?: number;
}) {
  return (
    <div className="group relative overflow-hidden rounded-3xl border border-[#e3e0d6] bg-white p-6 shadow-[0_1px_2px_rgba(12,20,36,.04)] transition duration-300 hover:-translate-y-1 hover:shadow-[0_30px_60px_-34px_rgba(77,91,158,.5)]">
      <span aria-hidden className="absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-[#c9b98a]/0 to-transparent transition-all duration-500 group-hover:via-[#c9b98a]/80" />
      <p className="text-sm font-medium text-[#5b6173]">{label}</p>
      <p className="datalens-number mt-3 font-serif text-[2.6rem] font-light leading-none tracking-[-0.04em]">{value}</p>
      <p className="mt-2 text-xs text-[#9a9eaf]">{supporting}</p>

      {progress !== undefined && (
        <div className="mt-5"><Bar value={progress} thin /></div>
      )}
    </div>
  );
}

function PerformanceMetric({
  label,
  value,
  description,
}: {
  label: string;
  value: number;
  description: string;
}) {
  return (
    <div className="grid gap-4 bg-white px-5 py-5 transition-colors hover:bg-[#faf9f5] sm:grid-cols-[130px_minmax(0,1fr)_80px] sm:items-center">
      <p className="text-sm font-semibold">{label}</p>

      <div>
        <Bar value={value * 100} />
        <p className="mt-2 text-[11px] leading-4 text-[#9a9eaf]">{description}</p>
      </div>

      <p className="datalens-number text-right font-serif text-2xl font-light">{formatPercent(value)}</p>
    </div>
  );
}

function ContextRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="px-5 py-4">
      <p className="text-xs text-[#9a9eaf]">{label}</p>
      <p className="mt-1.5 break-words text-sm font-semibold">{value}</p>
    </div>
  );
}

// ==========================================
// TABLE HELPERS
// ==========================================

function DataTable({ heads, children }: { heads: string[]; children: React.ReactNode }) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-[#ece9e0]">
      <table className="min-w-full border-collapse text-left text-sm">
        <thead className="border-b border-[#ece9e0] bg-[#faf9f5]">
          <tr>
            {heads.map((h) => (
              <th key={h} className="whitespace-nowrap px-5 py-3.5 text-xs font-semibold text-[#5b6173]">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-[#ece9e0] bg-white">{children}</tbody>
      </table>
    </div>
  );
}

function TableCell({ children, strong = false }: { children: React.ReactNode; strong?: boolean }) {
  return (
    <td className={`whitespace-nowrap px-5 py-4 ${strong ? "font-semibold" : "datalens-number text-[#5b6173]"}`}>
      {children}
    </td>
  );
}

// ==========================================
// MARKDOWN RENDERER
// ==========================================

function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");

  return (
    <div className="text-sm leading-7 text-[#2b3147]">
      {lines.map((rawLine, index) => {
        const line = rawLine.trim();

        if (!line) {
          return <div key={index} className="h-3" />;
        }

        if (line.startsWith("# ")) {
          return (
            <h2 key={index} className="mt-8 border-b border-[#ece9e0] pb-3 font-serif text-2xl tracking-[-0.02em] first:mt-0">
              <InlineMarkdown text={line.slice(2)} />
            </h2>
          );
        }

        if (line.startsWith("## ")) {
          return (
            <h3 key={index} className="mt-7 font-serif text-xl tracking-[-0.01em]">
              <InlineMarkdown text={line.slice(3)} />
            </h3>
          );
        }

        if (line.startsWith("### ")) {
          return (
            <h4 key={index} className="mt-5 text-sm font-semibold">
              <InlineMarkdown text={line.slice(4)} />
            </h4>
          );
        }

        if (line.startsWith("- ") || line.startsWith("* ")) {
          return (
            <div key={index} className="mt-2 flex gap-3 pl-1">
              <span className="mt-2.5 h-1.5 w-1.5 shrink-0 rounded-full bg-gradient-to-br from-[#4d5b9e] to-[#a9bbd8]" />
              <p className="flex-1"><InlineMarkdown text={line.slice(2)} /></p>
            </div>
          );
        }

        const numberedMatch = line.match(/^(\d+)\.\s+(.*)$/);

        if (numberedMatch) {
          return (
            <div key={index} className="mt-2 flex gap-3">
              <span className="min-w-7 font-mono text-[11px] font-semibold text-[#3d4a86]">{numberedMatch[1]}.</span>
              <p className="flex-1"><InlineMarkdown text={numberedMatch[2]} /></p>
            </div>
          );
        }

        return (
          <p key={index} className="mt-2"><InlineMarkdown text={line} /></p>
        );
      })}
    </div>
  );
}

// ==========================================
// INLINE MARKDOWN
// ==========================================

function InlineMarkdown({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g);

  return (
    <>
      {parts.map((part, index) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={index} className="font-semibold text-[#0c1424]">{part.slice(2, -2)}</strong>;
        }

        if (part.startsWith("`") && part.endsWith("`")) {
          return <code key={index} className="rounded-md bg-[#4d5b9e]/10 px-1.5 py-0.5 font-mono text-xs text-[#3d4a86]">{part.slice(1, -1)}</code>;
        }

        if (part.startsWith("*") && part.endsWith("*")) {
          return <em key={index} className="italic">{part.slice(1, -1)}</em>;
        }

        return <span key={index}>{part}</span>;
      })}
    </>
  );
}