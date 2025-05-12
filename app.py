from flask import Flask, redirect, url_for, session, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Auth Google
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url="/",
)
app.register_blueprint(google_bp, url_prefix="/login")

# Pinecone test
@app.route("/pinecone-test")
def pinecone_test():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return f"Pinecone client version OK – namespaces: {pc.list_indexes()}"

# Page d’accueil
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

