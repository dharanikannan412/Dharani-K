# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:
- Q&A
- simplified concept explanations
- 3-question MCQ quizzes
- summaries
- personalized learning paths

## Architecture

FastAPI serves both the REST API and the HTML/CSS frontend. Gemini is called only from the server, so the API key is never exposed to the browser.

The original documentation describes Gemini 1.5 Pro and LaMini-Flan-T5. This implementation uses Google's current `google-genai` SDK and a configurable Gemini model (`gemini-2.5-flash` by default). The explanation module includes an optional local LaMini-Flan-T5 path; if it is disabled or unavailable, it safely falls back to Gemini.

## Requirements

- Python 3.10+
- A Gemini API key
- Internet access for Gemini
- Optional: enough RAM/disk for the local LaMini model

## Quick start

### Windows PowerShell

```powershell
cd EduGenie
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

### macOS/Linux

```bash
cd EduGenie
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

## VS Code

1. Open the `EduGenie` folder.
2. Install the Microsoft Python extension.
3. Select `.venv` as the Python interpreter.
4. Open a terminal.
5. Activate the environment and install requirements.
6. Copy `.env.example` to `.env` and add your Gemini key.
7. Run `uvicorn main:app --reload`.
8. Open http://127.0.0.1:8000.

## API

- `GET /health`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`

Interactive API documentation:
- http://127.0.0.1:8000/docs

Example:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Which is the largest ocean?\"}"
```

## Configuration

See `.env.example`.

Important:
- Never commit `.env`.
- Never put `GEMINI_API_KEY` in frontend JavaScript.
- The server reads the key from the environment.

## Testing

With the server running:

```bash
pytest -q
```

The tests cover health checks, validation, the frontend route, and mocked AI service behavior. They do not consume your Gemini quota.

## Local explanation model

To enable the documentation's LaMini-Flan-T5 path:

```env
ENABLE_LOCAL_EXPLAINER=true
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

This downloads a model on first use and requires `torch`, `transformers`, and `sentencepiece`. The default is `false` so a fresh installation remains small and fast. Gemini remains the reliable fallback.
