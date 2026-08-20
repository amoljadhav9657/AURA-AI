from flask import Flask, request, jsonify, render_template_string

from src.brain.brain import Brain
from src.core.orchestrator import Orchestrator

app = Flask(__name__)

orchestrator = Orchestrator(Brain())

HTML = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>AURA AI</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
        }
        .app {
            width: 90%;
            max-width: 900px;
            margin: 30px auto;
            background: #1f2937;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,.4);
        }
        .header {
            padding: 20px;
            display: flex;
            justify-content: space-between;
            background: #111827;
        }
        .chat {
            height: 450px;
            overflow-y: auto;
            padding: 20px;
        }
        .msg {
            margin: 12px 0;
            line-height: 1.5;
        }
        .user { color: #93c5fd; }
        .aura { color: #c4b5fd; }
        .input {
            display: flex;
            padding: 15px;
            background: #111827;
        }
        input {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            margin-left: 10px;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>
<div class="app">
    <div class="header">
        <h2>🧠 AURA AI</h2>
        <b>● ONLINE</b>
    </div>

    <div id="chat" class="chat">
        <div class="msg aura"><b>AURA:</b> Hello! I am AURA AI. How can I help you?</div>
    </div>

    <div class="input">
        <input id="message" placeholder="Type your command..." autofocus>
        <button onclick="sendMessage()">SEND</button>
    </div>
</div>

<script>
async function sendMessage() {
    const input = document.getElementById("message");
    const text = input.value.trim();
    if (!text) return;

    const chat = document.getElementById("chat");
    chat.innerHTML += `<div class="msg user"><b>YOU:</b> ${text}</div>`;
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    });

    const data = await res.json();
    chat.innerHTML += `<div class="msg aura"><b>AURA:</b> ${data.response}</div>`;
    chat.scrollTop = chat.scrollHeight;
}

document.getElementById("message").addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please say something."})

    try:
        response = orchestrator.handle(message)
    except Exception as exc:
        response = f"Error: {exc}"

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
