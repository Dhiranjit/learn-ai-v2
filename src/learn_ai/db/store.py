import sqlite3
from learn_ai.db.schema import init_db


class ConversationStore:
    def __init__(self, db_path: str = "learn_ai.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        init_db(self.conn)

    def create_notebook(self, title: str) -> int:
        curr = self.conn.execute(
            "INSERT INTO notebooks (title) VALUES(?)",
            (title,),
        )
        self.conn.commit()
        return curr.lastrowid
    
    def list_notebooks(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT id, title, created_at FROM notebooks ORDER BY created_at DESC"
        ).fetchall()

        return [dict(r) for r in rows]
    
    def append_message(self, notebook_id: int, role: str, content: str) -> None:
        self.conn.execute(
            "INSERT INTO messages (notebook_id, role, content) VALUES(?, ?, ?)",
            (notebook_id, role, content),
        )
        self.conn.commit()

    def load_messages(self, notebook_id: int) -> list[dict]:
        rows = self.conn.execute(
            "SELECT role, content FROM messages WHERE notebook_id = ? ORDER BY id ASC",
            (notebook_id,),
        ).fetchall()

        return [dict(r) for r in rows]
    
    def close(self) -> None:
        self.conn.close()
