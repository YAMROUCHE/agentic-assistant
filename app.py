
from flask import Flask, request, jsonify, render_template
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Clé API Pinecone (directement dans le code ou en variable d'environnement)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY", "pcsk_6Wm1rB_49P1pymANZnW7YCGbkAqbUP49vhidkv7Vg2unmtLgBtU3FZZ2k67RaYqYddfjhZ"))
assistant = pc.assistant.Assistant(assistant_name="astreinte")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
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

# ✅ Ce bloc permet à Render d'exposer publiquement l'application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

