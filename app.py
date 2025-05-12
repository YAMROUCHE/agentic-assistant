from flask import Flask, redirect, url_for, session, render_template
from flask_dance.contrib.google import make_google_blueprint, google
import os
from pinecone import Pinecone, PodSpec
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_secret")

# Auth Google
blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url="/",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    return render_template("index.html", user=user_info)

# Pinecone (exemple minimal de client initialisé)
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# Exemple : vérifie si l’index existe
print(pc.list_indexes())

# Pas de app.run ici — Gunicorn prendra le relais

