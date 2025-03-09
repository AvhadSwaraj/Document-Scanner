from flask import Blueprint, request, jsonify, session, send_from_directory
import os
import sqlite3

profile_blueprint = Blueprint("profile", __name__, url_prefix="/profile")

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Always use the correct database path
DB_PATH = os.path.abspath("backend/database.db")

# Helper function to connect to the database
def get_db():
    conn = sqlite3.connect(DB_PATH)  # ✅ Use the correct path
    conn.row_factory = sqlite3.Row  # Return results as dictionaries
    return conn

# ✅ Fetch user profile details
@profile_blueprint.route("/details", methods=["GET"])
def get_profile():
    username = session.get("username")

    if not username:
        return jsonify({"error": "Not logged in"}), 401

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, credits FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
    except sqlite3.OperationalError:
        return jsonify({"error": "Database error: Table 'users' not found"}), 500
    finally:
        conn.close()

    if user:
        return jsonify({"username": user["username"], "credits": user["credits"]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# ✅ Upload document (Deduct 1 credit)
@profile_blueprint.route("/upload", methods=["POST"])
def upload_document():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Check user credits
        cursor.execute("SELECT credits FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user["credits"] <= 0:
            return jsonify({"error": "Not enough credits"}), 403

        if "document" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["document"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Deduct 1 credit
        new_credits = user["credits"] - 1
        cursor.execute("UPDATE users SET credits = ? WHERE username = ?", (new_credits, username))
        conn.commit()

    except sqlite3.OperationalError:
        return jsonify({"error": "Database error: Table 'users' not found"}), 500
    finally:
        conn.close()

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename,
        "credits": new_credits  # Send updated credits to frontend
    }), 200

# ✅ Fetch all uploaded documents
@profile_blueprint.route("/documents", methods=["GET"])
def get_uploaded_documents():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    documents = os.listdir(UPLOAD_FOLDER)
    return jsonify({"documents": documents}), 200

# ✅ Serve uploaded documents
@profile_blueprint.route("/uploads/<filename>", methods=["GET"])
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
