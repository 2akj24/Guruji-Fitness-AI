import sqlite3

def connect_db():
    return sqlite3.connect("fitai.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        weight REAL,
        height REAL,
        goal TEXT,
        diet_type TEXT,
        activity_level TEXT,
        budget TEXT,
        region TEXT,
        time_pref TEXT,
        score INTEGER DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()