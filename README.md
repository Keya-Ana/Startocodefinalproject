# 🤖 Question Generator 🚀

Ever wanted to create your own smart study quiz? This app lets you pick any subject and topic, and an advanced AI instantly creates custom multiple-choice questions for you! 

You can test your knowledge right on the screen, get instant grading with explanations, and download a clean print-out sheet with or without the answers revealed.

---

## 🛠️ Quick Start

Follow these simple steps to run the app on your computer:

1. **Open your terminal or command prompt** and enter your project folder.
2. **Turn on your virtual environment** (this keeps your project tools organized and separate from the rest of your computer):
    * **Linux or Mac:** `source .venv/bin/activate`
    * **Windows:** `.venv\Scripts\activate`
3. **Install the project tools** (you only need to do this the very first time):
    ```bash
    pip install fastapi uvicorn google-genai python-dotenv
    ```
4. **Set up your secret API Key:** To protect your privacy and follow security guidelines, do not paste your key directly into the code. Instead, create a brand new file in your main folder named exactly `.env` and paste this line inside it:
   ```env
   GCP_API_KEY=your_actual_secret_gemini_key_here
   
Launch app:
uvicorn main:app --reload --port 3003
Open your web browser and go to this address: http://localhost:3003

🎮 How to Use It
1. Subject: Type a general field like "Science" or "History".

2. Topic: Type a specific focus like "Solar System" or "World War 2".

3. Number of Questions: Type or scroll to how many questions you want.

4. Click "Generate Questions" and watch the magic happen! ✨

🕹️ Interactive Features
* Real-time Practice: Click on your answer choices! The button turns Green if you are right and Red if you are wrong.

* Instant Explanations: The AI reveals a helpful explanation box below the question right away to help you learn.

* Score Tracker: Watch your live score update automatically at the bottom of the screen.

* Smart PDF Download: Click the single "Download PDF" button to open a menu. You can choose to save a paper (Questions Only) for an unrevealed test or (With Answers) for a complete study guide.

* About the App Link: A clean button placed in the top-left corner that opens a pop-up window explaining how the app works and who built it, without leaving or reloading the page.

📂 What's Inside Your Project?
- main.py: The main "brain" of the app. It talks to the AI and handles the logic.

- .env: A hidden, secure file holding your secret AI keys.

- static/index.html: The layout structure of what you see on the screen.

- static/style.css: The look, layout, colors, and background pictures of your app.

- static/background image.jpg: The gold Q&A image asset used for the homepage background.

- static/answer.jpg: The colorful question-mark collage image asset used for the quiz dashboard background.

Built with ❤️ by Eulalia Antwi-Agyei for clean, premium study dashboards.
