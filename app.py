from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from gpt_handler import GPTHandler
import os

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()
chat_history = []

# Serve UI directly from public/chat.html
@app.route("/", methods=["GET"])
def home():
    try:
        with open(os.path.join("public", "chat.html"), "r", encoding="utf-8") as f:
            html_content = f.read()
        return Response(html_content, mimetype="text/html")
    except FileNotFoundError:
        return "Error: chat.html not found in public folder.", 404

# Chatbot API
@app.route("/chatbot", methods=["POST"])
def chatbot():
    global chat_history
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please ask a question."})
    try:
        chat_history.append({"role": "user", "content": user_message})
        response = gpt.generate_response(chat_history)
        chat_history.append({"role": "assistant", "content": response})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"})

# Required for Vercel serverless
app = app
