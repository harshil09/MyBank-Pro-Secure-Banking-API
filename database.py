import sqlite3
import os

DB_PATH = os.path.join("/opt/render/data", "user.db")

def get_connection():
    conn= sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
