import json
import sqlite3
import time
from backend.app.config import settings


def _conn():
    conn = sqlite3.connect(settings.db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                result TEXT,
                error TEXT,
                created_at REAL
            )""")
        # jobs interrupted by a server restart can never finish
        c.execute("UPDATE jobs SET status='failed', error='server restarted' "
                  "WHERE status='processing'")


def create_job(job_id: str):
    with _conn() as c:
        c.execute("INSERT INTO jobs (job_id, status, created_at) VALUES (?, 'processing', ?)",
                  (job_id, time.time()))


def set_done(job_id: str, result: dict):
    with _conn() as c:
        c.execute("UPDATE jobs SET status='done', result=? WHERE job_id=?",
                  (json.dumps(result), job_id))


def set_failed(job_id: str, error: str):
    with _conn() as c:
        c.execute("UPDATE jobs SET status='failed', error=? WHERE job_id=?", (error, job_id))


def get_job(job_id: str) -> dict | None:
    with _conn() as c:
        row = c.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
    if row is None:
        return None
    return {
        "job_id": row["job_id"],
        "status": row["status"],
        "result": json.loads(row["result"]) if row["result"] else None,
        "error": row["error"],
    }