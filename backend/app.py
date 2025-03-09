from flask import Flask, send_from_directory
from auth import auth_bp  # Import auth routes
from profile import profile_blueprint  # ✅ Import profile routes
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")  # ✅ Serve frontend files
app.secret_key = "your_secret_key"

# ✅ Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(profile_blueprint, url_prefix="/profile")  # ✅ Fix: Register profile routes

# ✅ Serve static files (HTML, CSS, JS)
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
