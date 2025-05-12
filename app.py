from flask import request, redirect, session, url_for

app.secret_key = "agentic_secret_key"  # 🔒 à personnaliser

PASSWORD = "agentic2025"  # 🔐 le mot de passe que tu veux

@app.before_request
def require_login():
    if request.path.startswith('/static'):
        return  # on autorise les fichiers statiques (logo, CSS, etc.)
    if 'logged_in' not in session and request.path not in ['/login', '/auth']:
        return redirect('/login')

@app.route("/login", methods=["GET"])
def login_page():
    return '''
        <form action="/auth" method="post">
            <h2>Connexion requise</h2>
            <input type="password" name="password" placeholder="Mot de passe" required/>
            <button type="submit">Se connecter</button>
        </form>
    '''

@app.route("/auth", methods=["POST"])
def login_action():
    if request.form.get("password") == PASSWORD:
        session["logged_in"] = True
        return redirect("/")
    return "Mot de passe incorrect", 403

