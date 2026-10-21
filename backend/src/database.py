import json
import sqlite3
from pathlib import Path
from typing import Any

from src.config import settings

DB_PATH = Path(settings.database_path)


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS adaptations (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                level TEXT NOT NULL,
                preview TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )


def save_adaptation(payload: dict[str, Any]) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO adaptations (id, created_at, level, preview, payload)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                payload["id"],
                payload["created_at"],
                payload["level"],
                payload["adapted_text"][:180],
                json.dumps(payload, ensure_ascii=False),
            ),
        )


def list_adaptations() -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, created_at, level, preview FROM adaptations ORDER BY created_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_adaptation(adaptation_id: str) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute(
            "SELECT payload FROM adaptations WHERE id = ?", (adaptation_id,)
        ).fetchone()
    return json.loads(row["payload"]) if row else None


def delete_adaptation(adaptation_id: str) -> bool:
    with _connect() as connection:
        cursor = connection.execute("DELETE FROM adaptations WHERE id = ?", (adaptation_id,))
    return cursor.rowcount > 0
