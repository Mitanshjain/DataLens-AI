# ==========================================
# DATALENS AI - LLM CLIENT V2
# ==========================================

import os

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# GET GROQ CLIENT
# ==========================================

def get_groq_client():
    """
    Create and return a Groq client.

    API key is loaded securely from
    the .env file.
    """

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Add it to the .env file."
        )

    return Groq(
        api_key=api_key
    )


# ==========================================
# ASK LLM
# ==========================================

def ask_llm(
    system_prompt,
    user_prompt,
    model="openai/gpt-oss-20b"
):
    """
    Send grounded analytics information
    to the LLM and return the final
    text response.
    """

    client = get_groq_client()

    try:

        response = (
            client.chat.completions.create(

                model=model,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],

                # ----------------------------------
                # GPT-OSS reasoning configuration
                # ----------------------------------

                reasoning_effort="low",

                include_reasoning=False,

                # ----------------------------------
                # Response configuration
                # ----------------------------------

                temperature=0.2,

                max_completion_tokens=4096,

                stream=False
            )
        )


        # ======================================
        # VALIDATE RESPONSE
        # ======================================

        if not response.choices:

            raise ValueError(
                "LLM returned no response choices."
            )


        message = (
            response
            .choices[0]
            .message
        )


        content = (
            message.content
        )


        # ======================================
        # VALIDATE CONTENT
        # ======================================

        if (
            content is None
            or not content.strip()
        ):

            raise ValueError(
                "LLM returned an empty final response."
            )


        return content.strip()


    except Exception as error:

        raise RuntimeError(
            f"LLM request failed: {error}"
        ) from error