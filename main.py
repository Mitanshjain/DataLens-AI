# ==========================================
# DATALENS AI
# DEVELOPMENT RUNNER
# ==========================================

from src.services.analysis_service import (
    run_complete_analysis
)


# ==========================================
# DEVELOPMENT CONFIGURATION
# ==========================================
#
# This file is only used for running
# DataLens manually during development.
#
# Production/API requests use FastAPI.
#
# ==========================================

file_path = (
    "data/uploads/customer_churn.csv"
)

target_column = (
    "churned"
)

positive_class = (
    "Yes"
)


# ==========================================
# RUN DATALENS
# ==========================================

if __name__ == "__main__":

    results = (
        run_complete_analysis(

            file_path=
                file_path,

            target_column=
                target_column,

            positive_class=
                positive_class
        )
    )


    # ======================================
    # FINAL SUMMARY
    # ======================================

    print(
        "\n================================"
    )

    print(
        "DATALENS AI RUN COMPLETE"
    )

    print(
        "================================"
    )

    print(
        f"Status: "
        f"{results['status']}"
    )

    print(
        f"Problem Type: "
        f"{results['problem_type']}"
    )

    print(
        f"Target Column: "
        f"{results['target_column']}"
    )

    print(
        f"Report Path: "
        f"{results['report_path']}"
    )