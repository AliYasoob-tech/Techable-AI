import os
import json
import pathlib
import cv2 
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# --- Configuration ---
load_dotenv()
app = Flask(__name__)
CORS(app)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

content_path = pathlib.Path(__file__).parent.parent / "content"

@app.route('/content/<path:path>')
def send_content(path):
    return send_from_directory(content_path, path)

# --- Helper Functions ---
def find_relevant_module(query, knowledge_core):
    query_words = set(query.lower().split())
    best_match = None
    max_score = 0
    for module in knowledge_core.get("modules", []):
        topic_words = set(module.get("topic", "").lower().split())
        content_words = set(module.get("text_content", "").lower().split())
        score = len(query_words.intersection(topic_words)) * 2 + len(query_words.intersection(content_words))
        if score > max_score:
            max_score = score
            best_match = module
    return best_match

def extract_frame_from_video(video_path):
    try:
        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        middle_frame_index = total_frames // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_index)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame_rgb)
        return None
    except Exception as e:
        print(f"Error processing video: {e}")
        return None

def build_prompt(mode, lesson_title, context_text, user_query):
    # 1. Define the Persona based on the mode
    if mode == 'visual_assist':
        persona = (
            f"You are a 'Visual Assist' tutor for the lesson '{lesson_title}'. "
            "You are speaking to a visually impaired user. Your primary goal is to be their eyes. "
            "If media (an image or video frame) is provided, you MUST describe it in rich, vivid detail FIRST, painting a mental picture. "
            "After describing the media, answer the user's question based on the media and the text context."
        )
    elif mode == 'simplified':
        persona = (
            f"You are a 'Simplified Text' tutor for the lesson '{lesson_title}'. "
            "You are speaking to a user who benefits from simple language (e.g., for Dyslexia). "
            "You MUST explain concepts clearly, using short sentences and simple words. Avoid jargon. "
            "Answer the user's question using only the provided context."
        )
    else: # Standard Mode
        persona = (
            f"You are an expert tutor for the lesson '{lesson_title}'. "
            "Your answer MUST synthesize information from BOTH the text context and the media (if provided). "
            "When you use information from the media, explicitly refer to it (e.g., 'As you can see in the video...' or 'The diagram shows...')."
        )

    # 2. Define the Core Task and "Fallback" Logic 
    task_instructions = (
        "\n--- TASK ---\n"
        "Here is the context and the user's question. Follow these rules:\n"
        "1. Base your answer *strictly* on the provided context text and media.\n"
        "2. If the user's question IS ANSWERED by the context, answer it directly and thoroughly.\n"
        "3. **If the user's question is NOT DIRECTLY ANSWERED** by the context, do NOT invent an answer. Instead, you MUST say 'That's not covered in this part of the lesson, but here is some related information:' and then provide the most relevant information from the context.\n"
        "4. If the provided context is empty or irrelevant, just say 'I'm sorry, I don't have any information on that topic for this lesson.'"
    )
    
    # 3. Assemble the final prompt
    prompt_parts = [
        persona,
        task_instructions,
        f"\n--- CONTEXT TEXT ---\n{context_text}\n--- END CONTEXT ---",
        f"\n--- USER'S QUESTION ---\n{user_query}"
    ]
    return prompt_parts

# --- API Endpoints ---
@app.route('/lessons', methods=['GET'])
def get_lessons():
    lessons = []
    for lesson_dir in content_path.iterdir():
        if lesson_dir.is_dir():
            manifest_path = lesson_dir / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path, "r") as f:
                    manifest_data = json.load(f)
                    lessons.append({
                        "id": lesson_dir.name,
                        "title": manifest_data.get("title", "Untitled Lesson")
                    })
    return jsonify(lessons)

@app.route('/ask', methods=['POST'])
@app.route('/ask', methods=['POST'])
def ask():
    # --- 1. Data Ingestion ---
    data = request.get_json()
    user_query = data.get('question')
    lesson_id = data.get('lesson_id')
    mode = data.get('mode', 'standard')

    # --- 2. Load Knowledge ---
    lesson_path = content_path / lesson_id
    manifest_path = lesson_path / "manifest.json"
    if not manifest_path.exists():
        return jsonify({"error": "Lesson not found"}), 404
    with open(manifest_path, "r") as f:
        knowledge_core = json.load(f)
    lesson_title = knowledge_core.get('title', 'Untitled Lesson')

    # --- 3. (RAG) ---
    context_text = ""
    relevant_module = None
    media_to_display = None
    prompt_media_files = [] 

    # Define keywords for general questions
    general_keywords = ['summary', 'summarize', 'lesson about', 'overview', 'tell me about this', 'general idea']
    is_general_query = any(keyword in user_query.lower() for keyword in general_keywords)

    if is_general_query:
        # Case 1: General question. Build context from the main summary and all module topics.
        context_text = knowledge_core.get('summary', '') + "\n\nThis lesson includes the following topics:\n"
        for module in knowledge_core.get("modules", []):
            # We add all text here so the AI can give a complete summary if asked
            context_text += f"- {module.get('topic', '')}: {module.get('text_content', '')}\n"
    else:
        # Case 2: Specific question. Try to find the best module.
        relevant_module = find_relevant_module(user_query, knowledge_core)
        
        if relevant_module:
            # Case 2a: Found a perfect match. Use its context and media.
            context_text = relevant_module.get("text_content", "")
            
            # Extract media for both the API and the frontend
            media_files = relevant_module.get("related_media", [])
            if media_files:
                media_filename = media_files[0]
                media_path = lesson_path / media_filename
                
                if media_path.exists():
                    file_extension = media_path.suffix.lower()
                    media_to_display = {"path": media_filename} # For frontend
                    
                    if file_extension in ['.png', '.jpg', '.jpeg', '.gif']:
                        img = Image.open(media_path)
                        prompt_media_files.append(img) # For API
                        media_to_display["type"] = "image"
                        
                    elif file_extension in ['.mp4', '.mov', '.webm']:
                        frame = extract_frame_from_video(media_path)
                        if frame:
                            prompt_media_files.append(frame) # For API
                        media_to_display["type"] = "video"
        
        else:
            # Case 2b: NO specific module matched.
            # Build a "best-effort" context from ALL text in the lesson.
            # The AI will then use Rule #3 from our prompt.
            context_text = "No single module matched the query. Here is all available text for the lesson:\n"
            context_text += knowledge_core.get('summary', '') + "\n"
            for module in knowledge_core.get("modules", []):
                context_text += f"- {module.get('topic', '')}: {module.get('text_content', '')}\n"
            # We don't attach any media here, as we don't know which one is relevant.

    # --- 4. Build the Prompt  ---
    prompt_parts = build_prompt(mode, lesson_title, context_text, user_query)

    # Insert the media *after* the first prompt part (the persona/instructions)
    if prompt_media_files:
        prompt_parts.insert(1, prompt_media_files[0]) 

    # --- 5. Call API 
    try:
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content(prompt_parts)
        
        return jsonify({
            "answer": response.text,
            "media": media_to_display, 
            "lesson_id": lesson_id
        })
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate a response from the AI model."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)