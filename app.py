from flask import Flask, redirect, url_for, session, render_template
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os
import pinecone

load_dotenv()
app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route("/")
def index():
    return "✅ Version stable OK"

if __name__ == "__main__":
    app.run()

