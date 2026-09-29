from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import TextRequest, QuizRequest, ApiResponse
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins.split(",")] if origins != "*" else ["*"],
    allow_credentials=origins != "*",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa", response_model=ApiResponse)
async def qa(payload: TextRequest):
    try:
        return ApiResponse(success=True, result=answer_question(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/explain", response_model=ApiResponse)
async def explain(payload: TextRequest):
    try:
        return ApiResponse(success=True, result=explain_concept(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/quiz", response_model=ApiResponse)
async def quiz(payload: QuizRequest):
    try:
        return ApiResponse(success=True, result=generate_quiz(payload.text, payload.num_questions))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/summarize", response_model=ApiResponse)
async def summarize(payload: TextRequest):
    try:
        return ApiResponse(success=True, result=summarize_text(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/learn/recommendations", response_model=ApiResponse)
async def recommendations(payload: TextRequest):
    try:
        return ApiResponse(success=True, result=get_learning_recommendations(payload.text))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
