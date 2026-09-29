from typing import Any
from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=20000)

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty.")
        return value


class QuizRequest(TextRequest):
    num_questions: int = Field(default=3, ge=1, le=10)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResult(BaseModel):
    questions: list[QuizQuestion]


class ApiResponse(BaseModel):
    success: bool
    result: Any
