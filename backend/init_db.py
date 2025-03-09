import sqlite3
import os
from werkzeug.security import generate_password_hash

# Ensure the database is created in backend/ folder
db_path = os.path.abspath("backend/database.db")

# Connect to SQLite and create table
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    credits INTEGER DEFAULT 20
)
""")

# Check if test user exists
cursor.execute("SELECT username FROM users WHERE username = ?", ("testuser",))
existing_user = cursor.fetchone()

if not existing_user:
    hashed_password = generate_password_hash("testpassword")  # Hash password
    cursor.execute("INSERT INTO users (username, password, credits) VALUES (?, ?, ?)", 
                   ("testuser", hashed_password, 20))
    conn.commit()
    print("Database initialized and test user created.")
else:
    print("Test user already exists.")

conn.close()
