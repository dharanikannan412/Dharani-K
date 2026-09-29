from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_frontend():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_validation_rejects_empty_input():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422


def test_qa_with_mock(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda text: "The Pacific Ocean is the largest.")
    response = client.post("/qa", json={"text": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert response.json()["result"] == "The Pacific Ocean is the largest."


def test_explain_with_mock(monkeypatch):
    monkeypatch.setattr(main, "explain_concept", lambda text: "A simple explanation.")
    response = client.post("/explain", json={"text": "Photosynthesis"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_quiz_with_mock(monkeypatch):
    fake = {
        "questions": [{
            "question": "2 + 2 = ?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4",
            "explanation": "Adding two and two gives four."
        }]
    }
    monkeypatch.setattr(main, "generate_quiz", lambda text, num_questions: fake)
    response = client.post("/quiz", json={"text": "Basic arithmetic", "num_questions": 1})
    assert response.status_code == 200
    assert response.json()["result"]["questions"][0]["correct_answer"] == "4"


def test_summary_with_mock(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda text: "Short summary.")
    response = client.post("/summarize", json={"text": "A long passage."})
    assert response.status_code == 200
    assert response.json()["result"] == "Short summary."


def test_learning_path_with_mock(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda text: "Step 1, Step 2.")
    response = client.post("/learn/recommendations", json={"text": "SQL"})
    assert response.status_code == 200
    assert "Step 1" in response.json()["result"]
