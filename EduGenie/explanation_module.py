import os

from gemini_client import generate_text


_local_pipeline = None


def _local_explain(concept: str) -> str:
    global _local_pipeline
    if _local_pipeline is None:
        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=os.getenv(
                "LOCAL_EXPLAINER_MODEL",
                "MBZUAI/LaMini-Flan-T5-783M",
            ),
            max_new_tokens=220,
        )

    prompt = (
        "Explain the following educational concept for a beginner. "
        "Use simple language, a short example, and avoid unnecessary jargon. "
        f"Concept: {concept}"
    )
    result = _local_pipeline(prompt)
    return result[0]["generated_text"].strip()


def explain_concept(concept: str) -> str:
    use_local = os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() == "true"

    if use_local:
        try:
            return _local_explain(concept)
        except Exception:
            # A local model may be unavailable because of RAM, package, or
            # download constraints. Gemini keeps the endpoint functional.
            pass

    prompt = f"""
Explain this concept as an excellent teacher helping a beginner.

Concept:
{concept}

Return:
1. A one-sentence definition.
2. A simple explanation.
3. A concrete everyday or academic example.
4. One common misconception or mistake, if relevant.

Keep the response clear and reasonably concise.
"""
    return generate_text(prompt)
