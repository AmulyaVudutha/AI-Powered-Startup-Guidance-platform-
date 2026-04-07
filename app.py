from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gpt_handler import GPTHandler

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()

# 🔹 Global chat memory
chat_history = []

@app.route("/")
def home():
    return "🚀 Startup AI Platform API is running!"

@app.route("/ui")
def ui():
    return render_template("chat.html")

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


# ✅ IMPORTANT FOR VERCEL
# DO NOT use debug=True and keep it clean
if __name__ == "__main__":
    app.run()