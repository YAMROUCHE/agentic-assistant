
from flask import Flask, request, jsonify, render_template
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

pc = Pinecone(api_key="pcsk_6Wm1rB_49P1pymANZnW7YCGbkAqbUP49vhidkv7Vg2unmtLgBtU3FZZ2k67RaYqYddfjhZ")
assistant = pc.assistant.Assistant(assistant_name="astreinte")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Message manquant"}), 400
    msg = Message(content=user_input)
    try:
        response = assistant.chat(messages=[msg])
        content = response["message"]["content"]
        return jsonify({"response": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
