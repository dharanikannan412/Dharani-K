from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the educational passage below in simple language.

Requirements:
- Preserve the main ideas and important facts.
- Remove repetition and filler.
- Use short paragraphs or bullets when useful.
- Do not add information that is absent from the source.
- Aim for a concise revision-friendly summary.

Passage:
{text}
"""
    return generate_text(prompt)
