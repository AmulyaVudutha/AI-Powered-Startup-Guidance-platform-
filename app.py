from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from gpt_handler import GPTHandler

app = Flask(__name__)
CORS(app)

gpt = GPTHandler()
chat_history = []

# Directly serve HTML in the root route
@app.route("/")
def home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Startup AI Platform</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin:0; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f2f5; }
        .chat-container { width:90%; max-width:800px; height:80vh; background:white; border-radius:10px; display:flex; flex-direction:column; box-shadow:0 10px 20px rgba(0,0,0,0.2); }
        .chat-messages { flex:1; overflow-y:auto; padding:20px; }
        .message { padding:10px 15px; margin:10px 0; border-radius:10px; max-width:70%; }
        .user { background:#4f46e5; color:white; margin-left:auto; }
        .bot { background:#e5e7eb; color:#111; margin-right:auto; }
        .chat-input { display:flex; border-top:1px solid #ccc; padding:10px; }
        .chat-input input { flex:1; padding:10px; border-radius:5px; border:1px solid #ccc; }
        .chat-input button { margin-left:10px; padding:10px 15px; border:none; border-radius:5px; background:#4f46e5; color:white; cursor:pointer; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-messages" id="messages">
            <div class="message bot">Hi 👋 I’m Startup AI — ask me anything about startups!</div>
        </div>
        <div class="chat-input">
            <input id="input" placeholder="Type your question..." onkeydown="if(event.key==='Enter'){send()}">
            <button onclick="send()">Send</button>
        </div>
    </div>
    <script>
        async function send() {
            let inputEl = document.getElementById("input");
            let msg = inputEl.value.trim();
            if (!msg) return;
            inputEl.value = "";
            const messages = document.getElementById("messages");
            messages.innerHTML += `<div class="message user">${msg}</div>`;
            try {
                let response = await fetch("/chatbot", {
                    method: "POST",
                    headers: {"Content-Type":"application/json"},
                    body: JSON.stringify({ message: msg })
                });
                let data = await response.json();
                messages.innerHTML += `<div class="message bot">${data.response}</div>`;
            } catch (err) {
                messages.innerHTML += `<div class="message bot">Error: ${err.message}</div>`;
            }
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""
    return Response(html_content, mimetype="text/html")

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
