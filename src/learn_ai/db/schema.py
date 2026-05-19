CREATE_NOTEBOOKS_TABLE = """
    CREATE TABLE IF NOT EXISTS notebooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

CREATE_MESSAGES_TABLE = """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        notebook_id INTEGER NOT NULL REFERENCES notebooks(id),
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""


CREATE_TRACES_TABLE = """
    CREATE TABLE IF NOT EXISTS traces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        notebook_id INTEGER NOT NULL REFERENCES notebooks(id),
        user_message TEXT,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ended_at TIMESTAMP,
        duration_ms INTEGER
    );
"""

CREATE_TRACE_STAGES_TABLE = """
    CREATE TABLE IF NOT EXISTS trace_stages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trace_id INTEGER NOT NULL REFERENCES traces(id),
        ord INTEGER NOT NULL,
        name TEXT NOT NULL,
        input_json TEXT,
        output_json TEXT,
        meta_json TEXT,
        duration_ms INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""


def init_db(conn):
    conn.execute(CREATE_NOTEBOOKS_TABLE)
    conn.execute(CREATE_MESSAGES_TABLE)
    conn.execute(CREATE_TRACES_TABLE)
    conn.execute(CREATE_TRACE_STAGES_TABLE)
    conn.commit()
