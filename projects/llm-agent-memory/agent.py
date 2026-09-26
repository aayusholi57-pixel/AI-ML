"""Offline-first long-term-memory agent core.

The SQLite memory layer is fully local and testable without an API key.
Gemini remains an optional online adapter for live generation.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class MemoryStore:
    """SQLite-backed conversation memory with keyword retrieval."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self._memory_connection: sqlite3.Connection | None = (
            sqlite3.connect(":memory:") if self.db_path == ":memory:" else None
        )
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        if self._memory_connection is not None:
            return self._memory_connection
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row
            connection.execute(
                """CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)"
            )
            connection.commit()

    def add(self, session_id: str, role: str, content: str) -> None:
        if not session_id.strip():
            raise ValueError("session_id must be non-empty")
        if role not in {"user", "assistant"}:
            raise ValueError("role must be user or assistant")
        if not content.strip():
            raise ValueError("content must be non-empty")
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO messages(session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (session_id, role, content.strip(),
                 datetime.now(timezone.utc).isoformat(timespec="seconds")),
            )
            connection.commit()

    def recent(self, session_id: str, limit: int = 12) -> list[dict[str, str]]:
        if limit < 1:
            raise ValueError("limit must be positive")
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT role, content, created_at FROM messages
                   WHERE session_id = ? ORDER BY id DESC LIMIT ?""",
                (session_id, limit),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def search(self, session_id: str, query: str, limit: int = 8) -> list[dict[str, str]]:
        if not query.strip():
            raise ValueError("query must be non-empty")
        terms = [term.lower() for term in query.split() if term.strip()]
        rows = self.recent(session_id, limit=1000)
        scored = []
        for row in rows:
            score = sum(row["content"].lower().count(term) for term in terms)
            if score:
                scored.append((score, row))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [row for _, row in scored[:limit]]

    def count(self, session_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM messages WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return int(row["count"])


class LocalAgent:
    """Deterministic memory harness used by the demo and CI."""

    def __init__(self, memory: MemoryStore, session_id: str) -> None:
        self.memory = memory
        self.session_id = session_id

    def remember(self, text: str) -> None:
        self.memory.add(self.session_id, "user", text)

    def recall(self, query: str) -> list[dict[str, str]]:
        return self.memory.search(self.session_id, query)

    def stats(self) -> int:
        return self.memory.count(self.session_id)


def build_local_agent(
    db_path: str | Path = ":memory:", session_id: str = "demo"
) -> LocalAgent:
    return LocalAgent(MemoryStore(db_path), session_id)


def gemini_configured() -> bool:
    """Return whether a Gemini API key is available."""
    return bool(os.getenv("GOOGLE_API_KEY"))
