# ==========================================
# DATALENS AI - AI ANALYST ENGINE V2
# ==========================================

from src.ai_analyst.context_builder import (
    build_ai_context
)

from src.ai_analyst.llm_client import (
    ask_llm
)

from src.ai_analyst.prompt import (
    AI_ANALYST_SYSTEM_PROMPT
)


def run_ai_analyst(
    df,
    target_column,
    problem_type,
    ml_results,
    business_results,
    decision_results=None
):
    """
    Run the grounded DataLens AI Analyst.

    Python analytics engines calculate facts.

    The Decision / Insight Engine converts
    analytical results into structured,
    evidence-backed observations.

    The LLM explains the supplied evidence.
    """

    print("\n================================")
    print("AI ANALYST V2")
    print("================================")


    # ==========================================
    # BUILD GROUNDED CONTEXT
    # ==========================================

    context = build_ai_context(

        df=df,

        target_column=
            target_column,

        problem_type=
            problem_type,

        ml_results=
            ml_results,

        business_results=
            business_results,

        decision_results=
            decision_results
    )


    # ==========================================
    # BUILD USER PROMPT
    # ==========================================

    user_prompt = f"""
Analyze the following DataLens AI results.

Use only the supplied analytics evidence.

The context may contain structured findings
from the deterministic Decision / Insight
Engine.

Treat those findings as evidence-backed
analytical observations, not as causal proof
or automatic business decisions.

Do not invent or estimate missing information.

ANALYTICS CONTEXT:

{context}

Create a concise executive-level analysis
while preserving important technical findings.

Prioritize meaningful decision insights when
they are supported by the supplied evidence.
"""


    # ==========================================
    # CALL LLM
    # ==========================================

    analysis = ask_llm(

        system_prompt=
            AI_ANALYST_SYSTEM_PROMPT,

        user_prompt=
            user_prompt
    )


    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    print(
        "\n================================"
    )

    print(
        "AI ANALYST REPORT"
    )

    print(
        "================================\n"
    )

    print(
        analysis
    )


    # ==========================================
    # STRUCTURED OUTPUT
    # ==========================================

    return {

        "target_column":
            target_column,

        "problem_type":
            problem_type,

        "decision_engine_used":
            decision_results is not None,

        "analysis":
            analysis
    }