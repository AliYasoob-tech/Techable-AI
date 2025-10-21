# Techable: An Accessible Multimodal AI Tutor 🤖


Techable is a prototype for the Multi-Modal AI Hackathon, designed to make education accessible for everyone. It transforms standard lesson materials into an interactive, multimodal, and adaptive learning experience tailored to users with different needs, including visual impairments and learning disabilities.

## Core Features (Prototype)
## Features

Adaptive Learning Modes:
 - -> Standard Mode: 
  A balanced experience with text and media (images/videos).
- -> Visual Assist Mode: For visually impaired users, this mode uses AI to provide rich, detailed audio descriptions of all visual content.
- -> Simplified Mode: For users who benefit from simpler language, this mode instructs the AI to use short, clear sentences.


- 🧠 Multimodal RAG (Retrieval-Augmented Generation): The AI chatbot doesn't just guess. It retrieves specific text and media (images or video frames) from a "Knowledge Core" based on the user's question, sending both to the Gemini model to synthesize a truly context-aware answer.
- 🗣️ Dual Input (Voice & Text): Interact by typing or by using your voice with the built-in speech-to-text.
- 🔊 Toggleable Text-to-Speech (TTS):AI responses can be read aloud using a high-quality browser voice.On by default for "Visual Assist" mode.Can be toggled on/off at any time with a dedicated button.




## ⚙️ Setup and Installation
Follow these steps to get the project running locally.

#### 1. Prerequisites:
- Python 3.9+
- GitGoogle Gemini API Key

#### 2. Clone the Repository
- git clone https://github.com/AliYasoob-tech/Techable-AI.git

#### 3. Set Up the Backend:
- The backend is powered by Flask.# Navigate to the backend directory

- cd backend

## Create a Python virtual environment
python -m venv venv

## Activate the virtual environment
### On Windows:
venv\Scripts\activate
### On macOS/Linux:
source venv/bin/activate

### Install the required Python packages
pip install -r requirements.txt

## 4. API Key Setup (Crucial!)
The project uses the Google Gemini API for its AI capabilities.
- Create a file named .env inside the backend directory.
- Open the .env file and add your Google API 

- - key:GOOGLE_API_KEY="YOUR_API_KEY_HERE"

## ▶️ How to Run the Project;
You must have both the backend and frontend running simultaneously.

- Step 1: Run the Backend ServerMake sure you are in the backend directory with your virtual environment activated.Run the Flask application:flask run

- You should see output indicating the server is running on http://127.0.0.1:5000. Keep this terminal open.Step 2: Run the FrontendOpen a new terminal window.Navigate to the frontend directory:cd frontend

- The easiest way to run the frontend is with a simple web server. If you have VS Code, we recommend using the "Live Server" extension.Right-click on index.html and select "Open with Live Server".

