import os
from flask import Flask, redirect, url_for, session, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
from dotenv import load_dotenv
import pinecone

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
CORS(app)

# 🔐 Authentification Google OAuth
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url="/",
)
app.register_blueprint(google_bp, url_prefix="/login")

# ✅ Initialisation Pinecone
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="gcp-starter"  # ou "us-east1-gcp", "eu-west4" selon ta console Pinecone
)

index_name = "support-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

index = pinecone.Index(index_name)

@app.route("/")
def index_route():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()
    email = user_info.get("email", "Inconnu")

    return render_template("index.html", email=email)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

