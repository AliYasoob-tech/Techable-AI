# Techable: An Accessible Multimodal AI Tutor

Techable is a prototype multimodal tutor built for the Multi-Modal AI Hackathon. It converts lesson materials into an interactive, adaptive learning experience that supports different user needs (visual assist, simplified text, and standard tutoring). This README explains how to set up, run, and test the project locally and includes a concise grading checklist for mid-submission.
## What this repo contains
- `backend/` — Flask backend that provides the API and serves lesson content from `content/`.
- `frontend/` — Static frontend (HTML/CSS/JS) that interacts with the backend.
- `content/` — Example lesson content (manifests, media, text). (Will be generated automatically using uploaded educational content)
- `requirements.txt` — Python dependencies for the backend.

## Key features (prototype)
- Adaptive learning modes: Standard, Visual Assist (detailed visual descriptions), and Simplified (plain language).
- Multimodal RAG: retrieves text + media and sends both to the AI model to generate context-aware responses.
- Text & voice input with optional TTS in the frontend.
---

## Prerequisites
- Python 3.9 or later
- Git
- A Google Gemini API key (set as `GOOGLE_API_KEY` in a `.env` file under `backend/`)

Recommended (for Windows PowerShell):
- Use a Python virtual environment for isolation.

---

## Setup (Windows PowerShell)

1. Clone the repo (if you haven't already):

```powershell
git clone https://github.com/AliYasoob-tech/Techable-AI.git
cd Techable-AI
```

2. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install backend dependencies:

```powershell
cd backend
pip install --upgrade pip
pip install -r ..\requirements.txt
```

Note: `requirements.txt` includes `opencv-python`, `Pillow`, `google-generativeai`, `Flask`, `Flask-Cors`, `python-dotenv`, and `numpy`.

---

## Environment variables
Create a `.env` file inside the `backend/` directory with at least the following variable:

```
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Replace `YOUR_API_KEY_HERE` with your actual key. The backend uses `python-dotenv` to load this variable.

---

## Running the project

You should run both the backend and the frontend. The backend serves the API and lesson content; the frontend is static files that call the backend.

### Start the backend (PowerShell)

From `backend/` with the virtual environment activated:

```powershell
# Option A: run with Python directly
python app.py

# Option B: use Flask CLI (optional)
# $env:FLASK_APP = 'app.py'; flask run --host=0.0.0.0 --port=5000
```

The backend will listen on port 5000 by default (http://127.0.0.1:5000).

### Serve the frontend

The frontend is static HTML/CSS/JS in the `frontend/` folder. Several options:

- Use VS Code Live Server extension: right-click `index.html` → "Open with Live Server".
- Use Python's simple HTTP server (from the repo root or inside `frontend/`):

```powershell
# from the frontend directory
cd ..\frontend
python -m http.server 5500
```

Open the frontend in the browser at http://127.0.0.1:5500 (or the Live Server URL). The frontend expects the backend API to be reachable at http://127.0.0.1:5000 by default.

---

## API endpoints (quick reference)

- GET /lessons — returns a list of available lessons from `content/`.
- POST /ask — send a JSON body with `question`, `lesson_id`, and optional `mode` (`standard`|`visual_assist`|`simplified`). Example request body:

```json
{
  "question": "What is photosynthesis?",
  "lesson_id": "photosynthesis",
  "mode": "standard"
}
```

Example PowerShell request:

```powershell
$body = @{ question = 'What is photosynthesis?'; lesson_id = 'photosynthesis'; mode = 'standard' } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/ask -Method POST -Body $body -ContentType 'application/json'
```

The response contains `answer` (text), optional `media` (path and type), and `lesson_id`.

---

## Troubleshooting

- If you see import errors for `cv2` or `numpy`, ensure you installed `requirements.txt` inside the active venv and that pip installation completed without errors.
- If audio/voice features don't work, make sure browser has permissions
- If the Google model returns errors, confirm that `GOOGLE_API_KEY` is set and valid.

---

## Core Features (Prototype)
## Features

Adaptive Learning Modes:
  -> Standard Mode: A balanced experience with text and media (images/videos).
  -> Visual Assist Mode: For visually impaired users, this mode uses AI to provide rich, detailed audio descriptions of all visual content.
  -> Simplified Mode: For users who benefit from simpler language, this mode instructs the AI to use short, clear sentences.


- 🧠 Multimodal RAG (Retrieval-Augmented Generation): The AI chatbot doesn't just guess. It retrieves specific text and media (images or video frames) from a "Knowledge Core" based on the user's question, sending both to the Gemini model to synthesize a truly context-aware answer.
- 🗣️ Dual Input (Voice & Text): Interact by typing or by using your voice with the built-in speech-to-text.
- 🔊 Toggleable Text-to-Speech (TTS):AI responses can be read aloud using a high-quality browser voice.On by default for "Visual Assist" mode.Can be toggled on/off at any time with a dedicated button.



## ⚙️ Setup and Installation
Follow these steps to get the project running locally.

#### 1. Prerequisites:
- Python 3.9+
- Git
- Google Gemini API Key

#### 2. Clone the Repository
- git clone https://github.com/AliYasoob-tech/Techable-AI.git

#### 3. Set Up the Backend:
- The backend is powered by Flask
 -  cd backend

## Create a Python virtual environment
> python -m venv venv

## Activate the virtual environment
### On Windows:
> venv\Scripts\activate

### Install the required Python packages
> pip install -r requirements.txt

## 4. API Key Setup (Crucial!)
The project uses the Google Gemini API for its AI capabilities.
- Create a file named .env inside the backend directory.
- Open the .env file and add your Google API 

  > key:GOOGLE_API_KEY="YOUR_API_KEY_HERE"

## ▶️ How to Run the Project;
You must have both the backend and frontend running simultaneously.

- Step 1: Run the Backend ServerMake sure you are in the backend directory with your virtual environment activated.
  - Run the Flask application:flask run. You should see output indicating the server is running on http://127.0.0.1:5000. Keep this terminal open.

- Step 2: Run the Frontend. Open a new terminal window. Navigate to the frontend directory:
  > cd frontend

- The easiest way to run the frontend is with a simple web server. If you have VS Code, use the "Live Server" extension.
  - Right-click on index.html and select "Open with Live Server".

