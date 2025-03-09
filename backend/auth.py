from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from models import get_db
import sqlite3  # ✅ FIXED: Import sqlite3

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    conn.row_factory = sqlite3.Row  # ✅ FIXED: Make rows accessible as dictionaries
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, password, credits FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        session["username"] = user["username"]
        session.permanent = True  # ✅ Ensure session persists

        response = jsonify({
            "message": "Login successful",
            "redirect": "/profile.html",
            "username": user["username"],
            "credits": user["credits"]
        })
        response.set_cookie("session", "valid", httponly=True, samesite="Lax", secure=False)
        return response, 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie("session", "", expires=0)
    return response, 200
