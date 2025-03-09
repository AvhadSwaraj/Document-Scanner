import sqlite3
import os

# Function to get SQLite database connection
def get_db():
    db_path = os.path.abspath("backend/database.db")  # Ensure correct path
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return results as dictionaries
    return conn
