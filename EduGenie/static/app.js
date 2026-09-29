const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const status = document.getElementById("status");
const quizOptions = document.getElementById("quizOptions");
const numQuestions = document.getElementById("numQuestions");
const copyBtn = document.getElementById("copyBtn");

task.addEventListener("change", () => {
  quizOptions.classList.toggle("hidden", task.value !== "quiz");

  const placeholders = {
    qa: "Which is the largest ocean?",
    explain: "Pythagoras theorem",
    quiz: "Paste a topic or study passage here.",
    summarize: "Paste a long educational passage here.",
    learn: "SQL from beginner to advanced",
  };
  inputText.placeholder = placeholders[task.value];
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderResult(data) {
  result.innerHTML = "";

  if (typeof data === "string") {
    const pre = document.createElement("div");
    pre.className = "result";
    pre.textContent = data;
    result.appendChild(pre);
    return;
  }

  if (data && Array.isArray(data.questions)) {
    data.questions.forEach((q, index) => {
      const wrapper = document.createElement("div");
      wrapper.className = "quiz-question";
      wrapper.innerHTML = `<h3>${index + 1}. ${escapeHtml(q.question)}</h3>`;

      q.options.forEach(option => {
        const button = document.createElement("button");
        button.className = "option";
        button.textContent = option;
        button.addEventListener("click", () => {
          const all = wrapper.querySelectorAll(".option");
          all.forEach(x => x.disabled = true);
          if (option === q.correct_answer) {
            button.classList.add("correct");
            button.insertAdjacentHTML("afterend",
              `<div class="answer-note"><strong>Correct.</strong> ${escapeHtml(q.explanation)}</div>`);
          } else {
            button.classList.add("incorrect");
            const correct = [...all].find(x => x.textContent === q.correct_answer);
            if (correct) correct.classList.add("correct");
            button.insertAdjacentHTML("afterend",
              `<div class="answer-note"><strong>Not quite.</strong> Correct answer: ${escapeHtml(q.correct_answer)}. ${escapeHtml(q.explanation)}</div>`);
          }
        });
        wrapper.appendChild(button);
      });

      result.appendChild(wrapper);
    });
    return;
  }

  const pre = document.createElement("div");
  pre.className = "result";
  pre.textContent = JSON.stringify(data, null, 2);
  result.appendChild(pre);
}

async function runTask() {
  const text = inputText.value.trim();
  if (!text) {
    status.textContent = "Please enter some text first.";
    return;
  }

  const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations",
  };

  status.textContent = "EduGenie is thinking…";
  submitBtn.disabled = true;
  resultCard.classList.add("hidden");

  const payload = { text };
  if (task.value === "quiz") payload.num_questions = Number(numQuestions.value);

  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const body = await response.json();
    if (!response.ok) {
      throw new Error(body.detail || "Request failed.");
    }

    renderResult(body.result);
    resultCard.classList.remove("hidden");
    status.textContent = "Completed.";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    submitBtn.disabled = false;
  }
}

submitBtn.addEventListener("click", runTask);

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(result.innerText);
  status.textContent = "Result copied.";
});
