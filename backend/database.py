import sqlite3
from config import Config

CREATE_CONTACTS_TABLE = """
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    reply TEXT,
    reply_timestamp TEXT
)
"""

def get_connection():
    conn = sqlite3.connect(Config.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema():
    with get_connection() as conn:
        conn.execute(CREATE_CONTACTS_TABLE)
        columns = [row['name'] for row in conn.execute("PRAGMA table_info(contacts)").fetchall()]

        if 'reply' not in columns:
            conn.execute("ALTER TABLE contacts ADD COLUMN reply TEXT")
        if 'reply_timestamp' not in columns:
            conn.execute("ALTER TABLE contacts ADD COLUMN reply_timestamp TEXT")
        conn.commit()


def init_db():
    ensure_schema()


def insert_contact(name, email, message, timestamp):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO contacts (name, email, message, timestamp) VALUES (?, ?, ?, ?)",
            (name, email, message, timestamp)
        )
        conn.commit()
        return cursor.lastrowid


def fetch_all_contacts():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


def fetch_contact_by_id(contact_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
        return dict(row) if row else None


def set_contact_reply(contact_id, reply, reply_timestamp):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE contacts SET reply = ?, reply_timestamp = ? WHERE id = ?",
            (reply, reply_timestamp, contact_id)
        )
        conn.commit()
        return cursor.rowcount
