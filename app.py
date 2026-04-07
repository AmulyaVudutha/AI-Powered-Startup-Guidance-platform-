from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gpt_handler import GPTHandler
import os

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()

# ⚠️ Note: Not persistent in Vercel (serverless)
chat_history = []

# ✅ Base directory fix for Vercel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Serve UI from public folder
@app.route("/")
def home():
    try:
        return send_file(os.path.join(BASE_DIR, "public", "chat.html"))
    except Exception as e:
        return f"Error loading UI: {str(e)}"

# Optional route
@app.route("/ui")
def ui():
    return send_file(os.path.join(BASE_DIR, "public", "chat.html"))

# Chat API
@app.route("/chatbot", methods=["POST"])
def chatbot():
    global chat_history

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please ask a question."})

    try:
        chat_history.append({
            "role": "user",
            "content": user_message
        })

        response = gpt.generate_response(chat_history)

        chat_history.append({
            "role": "assistant",
            "content": response
        })

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"})

# Required for Vercel
app = app
