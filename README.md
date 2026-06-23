# 🤖 Question Generator 🚀

Ever wanted to create your own super-powered quiz? This app lets you pick a subject and a topic, and then it finds cool questions for you!

## 🛠️ Quick Start

1.  **Open your terminal** and enter the folder.
2.  **Turn on your Python environment**:
    *   Linux/Mac: `source .venv/bin/activate`
    *   Windows: `.venv\Scripts\activate`
3.  **Install the magic tools** (only the first time):
    ```bash
    pip install fastapi uvicorn requests
    ```
4.  **Launch the app**:
    ```bash
    uvicorn main:app --reload --port 3003
    ```
5.  **Open your browser** and go to: `http://localhost:3003`

## 🎮 How to Play

1.  **Subject**: Type something like "Science" or "History".
2.  **Topic**: Type something specific like "Space" or "Dinosaurs".
3.  **Count**: Pick how many questions you want.
4.  **Click "Generate"** and watch the magic happen! ✨

## 📂 What's inside?
- `main.py`: The "brain" of our app.
- `static/index.html`: The "face" of our app that you see in the browser.

Built with ❤️ by Startocode.
