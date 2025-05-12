from flask import Flask, redirect, url_for, session
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os

# ✅ Nouveau import correct
from pinecone import Pinecone, PodSpec

# ✅ Charger les variables d’environnement
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)

# ✅ Authentification Google
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_url="/",
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json().get("email", "inconnu")
    return f"Bonjour, {email} ! Authentification réussie ✅"

if __name__ == "__main__":
    app.run(debug=True)

