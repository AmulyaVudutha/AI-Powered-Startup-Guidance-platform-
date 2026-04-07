from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gpt_handler import GPTHandler

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()
chat_history = []

@app.route("/")
def home():
    return send_file("public/chat.html")

@app.route("/chat.html")
def serve_html():
    return send_file("chat.html")

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

app = app
