from pydantic import BaseModel, Field

from gemini_client import generate_structured


class QuizQuestion(BaseModel):
    question: str = Field(description="A clear multiple-choice question.")
    options: list[str] = Field(
        min_length=4,
        max_length=4,
        description="Exactly four answer choices.",
    )
    correct_answer: str = Field(
        description="The exact text of the correct option."
    )
    explanation: str = Field(
        description="A short explanation of why the correct option is correct."
    )


class QuizResult(BaseModel):
    questions: list[QuizQuestion]


def generate_quiz(text: str, num_questions: int = 3) -> dict:
    schema = QuizResult.model_json_schema()

    prompt = f"""
Generate exactly {num_questions} educational multiple-choice questions
from the material below.

Rules:
- Exactly four options per question.
- Only one option is correct.
- `correct_answer` must exactly match one of the four option strings.
- Questions must be answerable from the supplied material.
- Make distractors plausible but clearly incorrect when the material is understood.
- Add a short explanation for each answer.
- Return only data matching the requested schema.

Material:
{text}
"""

    result = generate_structured(prompt, QuizResult)
    return result.model_dump()
