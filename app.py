from flask import Flask, request, jsonify
from flask_cors import CORS
from gpt_handler import GPTHandler

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()
chat_history = []

@app.route("/")
def home():
    return {"message": "🚀 Startup AI Platform API is running!"}

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
