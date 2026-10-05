# ==========================================
# DATALENS AI - BUSINESS ANALYTICS ENGINE V1
# ==========================================

from src.business_analytics.kpi_engine import (
    generate_kpi_summary
)

from src.business_analytics.segment_analysis import (
    analyze_segments
)

from src.business_analytics.business_findings import (
    generate_business_findings
)


def run_business_analytics(
    df,
    target_column=None
):
    """
    Main orchestrator for the
    DataLens AI Business Analytics Engine.

    Runs:
        1. KPI Analysis
        2. Segment Analysis
        3. Business Findings

    Returns all results in one
    structured dictionary.
    """

    print("\n================================")
    print("BUSINESS ANALYTICS ENGINE")
    print("================================")

    print(
        f"Target Column: {target_column}"
    )


    # ==========================================
    # 1. KPI ENGINE
    # ==========================================

    kpi_results = (
        generate_kpi_summary(
            df,
            target_column=target_column
        )
    )


    # ==========================================
    # 2. SEGMENT ANALYSIS
    # ==========================================

    segment_results = (
        analyze_segments(
            df,
            target_column=target_column
        )
    )


    # ==========================================
    # 3. BUSINESS FINDINGS
    # ==========================================

    findings_results = (
        generate_business_findings(
            df,
            target_column=target_column
        )
    )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    business_results = {

        "target_column":
            target_column,

        "kpis":
            kpi_results,

        "segments":
            segment_results,

        "findings":
            findings_results
    }


    # ==========================================
    # COMPLETE
    # ==========================================

    print("\n================================")
    print("BUSINESS ANALYTICS COMPLETE")
    print("================================")

    print(
        f"Total Findings: "
        f"{findings_results['total_findings']}"
    )


    return business_results