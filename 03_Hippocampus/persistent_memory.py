import sqlite3

DB = "memory.db"


class PersistentMemory:
    def __init__(self, db=DB):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                confidence REAL DEFAULT 1.0
            )
        """)
        self.conn.commit()

    def save(self, question, answer, confidence=1.0):
        self.conn.execute(
            "INSERT INTO memories (question, answer, confidence) VALUES (?, ?, ?)",
            (question, answer, confidence)
        )
        self.conn.commit()

    def recall(self, question):
        return self.conn.execute(
            "SELECT answer, confidence FROM memories WHERE question = ? ORDER BY id DESC LIMIT 1",
            (question,)
        ).fetchone()

    def close(self):
        self.conn.close()
