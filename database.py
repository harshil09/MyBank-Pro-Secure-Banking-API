import sqlite3
import os

# Persistent DB location on Render
DB_PATH = os.path.join("/opt/render/data", "user.db")

def get_connection():
    # Ensure the folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)
