from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Sécurité Flask
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Authentification Google OAuth2
blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="index"
)
app.register_blueprint(blueprint, url_prefix="/login")

# Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
assistant = pc.assistant.Assistant(assistant_name="astreinte")

# Page d'accueil avec sécurité
@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template("index.html")

# API de réponse
@app.route("/ask", methods=["POST"])
def ask():
    if not google.authorized:
        return jsonify({"error": "Utilisateur non authentifié"}), 401

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
