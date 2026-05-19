import json
import sqlite3
import time
from typing import Any

from learn_ai.db.schema import init_db


def _dumps(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, default=str, ensure_ascii=False)


class Trace:
    def __init__(self, conn: sqlite3.Connection, trace_id: int):
        self.conn = conn
        self.id = trace_id
        self._order = 0
        self._started = time.perf_counter()

    def stage(
        self,
        name: str,
        *,
        input: Any = None,
        output: Any = None,
        meta: dict | None = None,
        duration_ms: int | None = None,
    ) -> None:
        self._order += 1
        self.conn.execute(
            """
            INSERT INTO trace_stages
                (trace_id, ord, name, input_json, output_json, meta_json, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.id,
                self._order,
                name,
                _dumps(input),
                _dumps(output),
                _dumps(meta),
                duration_ms,
            ),
        )
        self.conn.commit()

    def end(self) -> None:
        duration_ms = int((time.perf_counter() - self._started) * 1000)
        self.conn.execute(
            "UPDATE traces SET ended_at = CURRENT_TIMESTAMP, duration_ms = ? WHERE id = ?",
            (duration_ms, self.id),
        )
        self.conn.commit()


class Tracer:
    def __init__(self, db_path: str = "learn_ai.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        init_db(self.conn)

    def start_trace(self, notebook_id: int, user_message: str) -> Trace:
        cur = self.conn.execute(
            "INSERT INTO traces (notebook_id, user_message) VALUES (?, ?)",
            (notebook_id, user_message),
        )
        self.conn.commit()
        return Trace(self.conn, cur.lastrowid)

    def list_traces(self, notebook_id: int | None = None, limit: int = 50) -> list[dict]:
        if notebook_id is None:
            rows = self.conn.execute(
                """
                SELECT id, notebook_id, user_message, started_at, duration_ms
                FROM traces ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT id, notebook_id, user_message, started_at, duration_ms
                FROM traces WHERE notebook_id = ? ORDER BY id DESC LIMIT ?
                """,
                (notebook_id, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_stages(self, trace_id: int) -> list[dict]:
        rows = self.conn.execute(
            """
            SELECT ord, name, input_json, output_json, meta_json, duration_ms
            FROM trace_stages WHERE trace_id = ? ORDER BY ord ASC
            """,
            (trace_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self.conn.close()
