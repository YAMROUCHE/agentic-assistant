import os
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
from pinecone import Pinecone, PodSpec
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
CORS(app)

# Authentification Google
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    redirect_url="/",
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

# Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("support-index")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    return render_template("index.html", user=user_info)

@app.route("/ask", methods=["POST"])
def ask():
    if not google.authorized:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message manquant"}), 400

    # 👉 ici : ajouter un traitement si nécessaire avec Pinecone ou autre
    return jsonify({"response": f"Vous avez dit : {message}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

