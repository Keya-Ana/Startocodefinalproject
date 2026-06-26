import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

GEMINI_API_KEY = "AQ.Ab8RN6J3nzRS0xE4IN5QK3xnYg8_E9aYJ4jJQDFj4TEp_eqKnA"
client = genai.Client(api_key=GEMINI_API_KEY)


def build_page(results_html=""):
    try:
        with open("static/index.html", "r") as file:
            html = file.read()
        if "" in html:
            html = html.replace("", results_html)
        else:
            html = html + results_html
        return html
    except FileNotFoundError:
        return f"<h3>Error: static/index.html not found</h3>{results_html}"


@app.get("/")
def home():
    return HTMLResponse(build_page())


@app.post("/generate")
def generate(subject: str = Form(), topic: str = Form(), num_questions: int = Form()):
    prompt = (
        f"Generate exactly {num_questions} multiple-choice test questions about the topic "
        f"'{topic}' inside the subject '{subject}'. "
        f"For each question, provide exactly 4 options labeled exactly as 'A', 'B', 'C', and 'D', "
        f"and specify which key ('A', 'B', 'C', or 'D') is the correct_answer. "
        f"Also provide a short explanation for the correct answer."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "question": {"type": "STRING"},
                            "options": {
                                "type": "OBJECT",
                                "properties": {
                                    "A": {"type": "STRING"},
                                    "B": {"type": "STRING"},
                                    "C": {"type": "STRING"},
                                    "D": {"type": "STRING"}
                                },
                                "required": ["A", "B", "C", "D"]
                            },
                            "correct_answer": {"type": "STRING"},
                            "explanation": {"type": "STRING"}
                        },
                        "required": ["question", "options", "correct_answer", "explanation"]
                    }
                },
                temperature=0.6
            ),
        )
        questions = json.loads(response.text)

    except Exception as e:
        print(f"!!! API ERROR LOG: {e}")
        friendly_error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8"><title>Preparing Quiz</title>
            <link rel="stylesheet" href="/static/style.css?v=master_error">
        </head>
        <body class="quiz-body">
            <div class="results-container" style="text-align: center; margin-top: 80px; background: white;">
                <h1>AI System is Busy...</h1>
                <p>We encountered a temporary rate issue. Click below to try again seamlessly!</p>
                <a href="/" class="btn-primary" style="text-decoration: none; display: inline-block; margin-top: 20px; max-width: 200px;">Try Again</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(friendly_error_html)

    questions_html = ""
    for index, item in enumerate(questions, start=1):
        q_text = item.get("question", "").strip()
        opts = item.get("options", {})
        correct = item.get("correct_answer", "").strip().upper()
        explanation = item.get("explanation", "").strip().replace("'", "\\'")

        options_markup = ""
        for key in ["A", "B", "C", "D"]:
            opt_text = opts.get(key, "").strip()
            options_markup += f"""
            <button type="button" class="option-btn" data-key="{key}" onclick="checkAnswer(this, '{key}', '{correct}', '{index}')">
                <span class="option-letter">{key}</span> {opt_text}
            </button>
            """

        questions_html += f"""
        <div class="question-card" id="q-card-{index}">
            <div class="card-header">
                <span class="q-badge">Question {index}</span>
                <span class="status-badge" id="status-{index}">Unanswered</span>
            </div>
            <p class="question-text">{q_text}</p>
            <div class="options-grid">
                {options_markup}
            </div>
            <div class="feedback-box hidden" id="feedback-{index}">
                <p class="feedback-title"></p>
                <p class="feedback-text"><strong>Explanation:</strong> {explanation}</p>
            </div>
        </div>
        """

    final_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Questions Sheet</title>
        <link rel="stylesheet" href="/static/style.css?v=master">
    </head>
    <body class="quiz-body">
        <div class="results-container">
            <div class="results-header">
                <span class="category-tag">{subject}</span>
                <h1>{topic} Test Sheet</h1>
                <p class="meta-info">Interactive Assessment • {num_questions} Questions</p>
            </div>

            <div class="questions-grid">
                {questions_html}
            </div>

            <div class="action-bar-bottom">
                <a href="/" class="btn-secondary">← Create Another Assessment</a>
                <div class="score-tracker">Score: <span id="correct-count">0</span> / {num_questions}</div>
            </div>
        </div>

        <script>
        let answeredQuestions = new Set();
        let correctAnswersCount = 0;

        function checkAnswer(button, selectedKey, correctKey, qIdx) {{
            if (answeredQuestions.has(qIdx)) return;
            answeredQuestions.add(qIdx);

            const card = document.getElementById('q-card-' + qIdx);
            const feedbackBox = document.getElementById('feedback-' + qIdx);
            const statusBadge = document.getElementById('status-' + qIdx);
            const allButtons = card.querySelectorAll('.option-btn');

            allButtons.forEach(btn => btn.classList.add('disabled'));

            if (selectedKey === correctKey) {{
                button.classList.add('correct');
                statusBadge.textContent = "Correct";
                statusBadge.className = "status-badge correct-badge";
                feedbackBox.querySelector('.feedback-title').innerHTML = "✨ Excellent! That is correct.";
                feedbackBox.className = "feedback-box correct-feedback";
                correctAnswersCount++;
                document.getElementById('correct-count').textContent = correctAnswersCount;
            }} else {{
                button.classList.add('incorrect');
                statusBadge.textContent = "Incorrect";
                statusBadge.className = "status-badge incorrect-badge";
                feedbackBox.querySelector('.feedback-title').innerHTML = "❌ Incorrect. The correct answer was option " + correctKey + ".";
                feedbackBox.className = "feedback-box incorrect-feedback";

                allButtons.forEach(btn => {{
                    if (btn.getAttribute('data-key') === correctKey) {{
                        btn.classList.add('correct');
                    }}
                }});
            }}

            feedbackBox.classList.remove('hidden');
        }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(final_html)