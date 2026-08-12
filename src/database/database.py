import sqlite3
import os


class Database:

    def __init__(self):

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_folder = os.path.join(base_path, "data")

        os.makedirs(db_folder, exist_ok=True)

        self.db_path = os.path.join(db_folder, "aura.db")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
        """)

        self.conn.commit()

    def save_memory(self, key, value):

        self.cursor.execute("""
        INSERT OR REPLACE INTO memory(key,value)
        VALUES(?,?)
        """, (key, value))

        self.conn.commit()

    def load_memory(self, key):

        self.cursor.execute("""
        SELECT value FROM memory
        WHERE key=?
        """, (key,))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

    def get_all_memories(self):

        self.cursor.execute("""
        SELECT key, value
        FROM memory
        ORDER BY id ASC
        """)

        rows = self.cursor.fetchall()

        return [
            {
                "key": row[0],
                "value": row[1]
            }
            for row in rows
        ]