import os
from functools import lru_cache

from google import genai
from google.genai import types


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )
    return genai.Client(api_key=api_key)


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    response = get_client().models.generate_content(
        model=get_model_name(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=2048,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def generate_structured(prompt: str, schema):
    response = get_client().models.generate_content(
        model=get_model_name(),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=4096,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    if getattr(response, "parsed", None) is not None:
        return response.parsed
    return schema.model_validate_json(response.text)
