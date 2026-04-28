import sqlite3

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    query TEXT,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_chat(user_id: str, query: str, response: str):
    cursor.execute(
        "INSERT INTO chat_history (user_id, query, response) VALUES (?, ?, ?)",
        (user_id, query, response),
    )
    conn.commit()


def get_chat_history(user_id: str, limit: int = 5):
    cursor.execute(
        "SELECT query, response FROM chat_history WHERE user_id=? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    )
    return cursor.fetchall()