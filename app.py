from flask import Flask, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")  # à sécuriser en prod

# Google OAuth via Flask-Dance
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    redirect_url="/login/google/authorized",
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))

    try:
        resp = google.get("/oauth2/v2/userinfo")
        resp.raise_for_status()
        email = resp.json()["email"]
        return f"✅ Connecté en tant que : {email}"
    except Exception as e:
        return f"❌ Erreur lors de l'authentification Google :<br><code>{str(e)}</code>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

