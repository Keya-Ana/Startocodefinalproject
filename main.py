import json
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def build_page(results_html=""):
    file = open("static/index.html")
    html = file.read()
    file.close()

    # put the results where the placeholder is
    html = html.replace("<!-- RESULTS -->", results_html)

    return html

@app.get("/")
def home():
    return HTMLResponse(build_page())

@app.post("/generate")
def generate(subject: str = Form(), topic: str = Form(), num_questions: int = Form()):
    intructions = (
        f"Generate exactly {num_questions} questions about the topic "
        f'"{topic}" in the subject "{subject}". '
        f"Return ONLY a JSON array of strings, no other text. "
        f'Example: ["Question 1?", "Question 2?"]'
    )

    response = requests.post(
        STARTOCODE_QUESTION_GENERATOR, json={"question": intructions}, timeout=30)
    data = response.json()

    # parse the questions from the API response
    answers = data["answer"]
    try:
        questions = json.loads(answers)
    except:
        questions = answers.split("\n")

    # build the results list
    questions_html = ""
    for question in questions:
        question = question.strip()
        if question:
            questions_html = questions_html + f"<li>{question}</li>"

    results_html = f"""
       <div class="results">
           <h2>{subject} - {topic}</h2>
           <ol>{questions_html}</ol>
       </div>
       """

    return HTMLResponse(build_page(results_html))



