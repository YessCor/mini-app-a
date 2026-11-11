const screens = {
  home: document.querySelector("#home-screen"),
  quiz: document.querySelector("#quiz-screen"),
  result: document.querySelector("#result-screen"),
};
const letters = ["A", "B", "C", "D"];
let currentQuiz = null;
let questionIndex = 0;
let score = 0;
let selectedCategory = null;
let toastTimer;

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "No pudimos conectar con el juego. Inténtalo de nuevo.");
  }
  return response.json();
}

function showScreen(name) {
  Object.entries(screens).forEach(([key, screen]) => {
    screen.hidden = key !== name;
  });
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toast.hidden = true;
  }, 3600);
}

async function loadCategories() {
  const grid = document.querySelector("#category-grid");
  try {
    const categories = await api("/api/categories");
    grid.replaceChildren();
    categories.forEach((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `category-card ${category.color}`;
      button.setAttribute("aria-label", `Jugar ${category.name}`);

      const symbol = document.createElement("span");
      symbol.className = "category-symbol";
      symbol.textContent = category.icon;
      const name = document.createElement("span");
      name.className = "category-name";
      name.textContent = category.name;
      const description = document.createElement("span");
      description.className = "category-description";
      description.textContent = category.description;

      button.append(symbol, name, description);
      button.addEventListener("click", () => startQuiz(category.name));
      grid.append(button);
    });
  } catch (error) {
    grid.innerHTML = "";
    const message = document.createElement("div");
    message.className = "loading-card";
    message.textContent = error.message;
    grid.append(message);
  }
}

async function startQuiz(category = "Aleatoria") {
  try {
    currentQuiz = await api("/api/quiz", {
      method: "POST",
      body: JSON.stringify({ category, question_count: 5 }),
    });
    selectedCategory = category;
    questionIndex = 0;
    score = 0;
    document.querySelector("#quiz-category").textContent = category;
    document.querySelector("#score-label").textContent = "0 puntos";
    showScreen("quiz");
    renderQuestion();
  } catch (error) {
    showToast(error.message);
  }
}

function renderQuestion() {
  const question = currentQuiz.questions[questionIndex];
  document.querySelector("#quiz-counter").textContent =
    `${String(questionIndex + 1).padStart(2, "0")} / ${String(currentQuiz.total).padStart(2, "0")}`;
  document.querySelector("#progress-bar").style.width =
    `${(questionIndex / currentQuiz.total) * 100}%`;
  document.querySelector("#question-kicker").textContent =
    `PREGUNTA ${String(questionIndex + 1).padStart(2, "0")}`;
  document.querySelector("#question-text").textContent = question.text;
  document.querySelector("#feedback").hidden = true;
  document.querySelector("#feedback").classList.remove("wrong");
  document.querySelector("#next-button").hidden = true;

  const answerList = document.querySelector("#answer-list");
  answerList.replaceChildren();
  question.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "answer-option";
    const letter = document.createElement("span");
    letter.className = "answer-letter";
    letter.textContent = letters[index];
    const label = document.createElement("span");
    label.textContent = option;
    button.append(letter, label);
    button.addEventListener("click", () => submitAnswer(index));
    answerList.append(button);
  });
}

async function submitAnswer(answerIndex) {
  const buttons = [...document.querySelectorAll(".answer-option")];
  buttons.forEach((button) => {
    button.disabled = true;
  });

  try {
    const result = await api(`/api/quiz/${currentQuiz.id}/answer`, {
      method: "POST",
      body: JSON.stringify({ question_index: questionIndex, answer_index: answerIndex }),
    });
    score = result.score;
    document.querySelector("#score-label").textContent =
      `${score} ${score === 1 ? "punto" : "puntos"}`;
    buttons[answerIndex].classList.add(result.correct ? "selected-correct" : "selected-wrong");
    if (!result.correct) buttons[result.correct_answer].classList.add("reveal-correct");

    const feedback = document.querySelector("#feedback");
    feedback.hidden = false;
    feedback.classList.toggle("wrong", !result.correct);
    document.querySelector("#feedback-title").textContent =
      result.correct ? "¡Correcto! +1 punto" : "Casi… la respuesta era otra";
    document.querySelector(".feedback-check").textContent = result.correct ? "✓" : "↗";
    document.querySelector("#feedback-fact").textContent = result.fact;

    const nextButton = document.querySelector("#next-button");
    nextButton.innerHTML =
      questionIndex === currentQuiz.total - 1
        ? 'Ver mi resultado <span>→</span>'
        : 'Siguiente pregunta <span>→</span>';
    nextButton.hidden = false;
  } catch (error) {
    buttons.forEach((button) => {
      button.disabled = false;
    });
    showToast(error.message);
  }
}

async function showResult() {
  try {
    const result = await api(`/api/quiz/${currentQuiz.id}/result`);
    document.querySelector("#result-title").textContent =
      result.percentage === 100 ? "¡Eres increíble!" : "¡Buen trabajo!";
    document.querySelector("#result-message").textContent = result.message;
    document.querySelector("#final-score").textContent = `${result.score} / ${result.total}`;
    document.querySelector("#final-category").textContent =
      result.category === "Aleatoria" ? "Categorías mezcladas" : result.category;
    document.querySelector("#result-icon").textContent = result.percentage >= 60 ? "✦" : "↗";
    showScreen("result");
  } catch (error) {
    showToast(error.message);
  }
}

document.querySelector("#random-button").addEventListener("click", () => startQuiz());
document.querySelector("#quit-button").addEventListener("click", () => showScreen("home"));
document.querySelector("#next-button").addEventListener("click", () => {
  if (questionIndex === currentQuiz.total - 1) {
    showResult();
  } else {
    questionIndex += 1;
    renderQuestion();
  }
});
document.querySelector("#play-again-button").addEventListener("click", () => startQuiz(selectedCategory));
document.querySelector("#home-button").addEventListener("click", () => showScreen("home"));
loadCategories();
