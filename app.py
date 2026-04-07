from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_handler import GPTHandler

app = Flask(__name__, static_url_path='', static_folder='public')
CORS(app)

gpt = GPTHandler()
chat_history = []

# Serve the chat UI directly at /
@app.route("/")
def home():
    return app.send_static_file("chat.html")

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

# Required for Vercel
app = app
