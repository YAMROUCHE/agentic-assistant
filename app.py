from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import os

from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Config
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # pour Render

# Google OAuth config
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = "google.login"

# User model
class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Pinecone setup
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
assistant = pc.assistant.Assistant(assistant_name="astreinte")

@app.route("/")
@login_required
def index():
    return render_template("index.html", user=current_user.id)

@app.route("/ask", methods=["POST"])
@login_required
def ask():
    try:
        data = request.json
        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"error": "Message manquant"}), 400

        msg = Message(content=user_input)
        response = assistant.chat(messages=[msg])
        content = response["message"]["content"]
        return jsonify({"response": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/login/google/authorized")
def authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Erreur lors de la connexion", 403

    email = resp.json()["email"]
    user = User(email)
    login_user(user)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

