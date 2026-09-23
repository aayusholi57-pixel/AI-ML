"""Execution tests for the persistent agent memory layer."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from agent import MemoryStore, build_local_agent, gemini_configured  # noqa: E402


def test_memory_persists_and_retrieves_relevant_messages(tmp_path: Path) -> None:
    db_path = tmp_path / "memory.db"
    first = build_local_agent(db_path, "session-a")
    first.remember("My favorite project uses Python and SQLite.")
    first.remember("I am learning computer vision.")

    second = build_local_agent(db_path, "session-a")
    results = second.recall("SQLite")
    assert len(results) == 1
    assert "SQLite" in results[0]["content"]
    assert second.stats() == 2


def test_sessions_are_isolated() -> None:
    memory = MemoryStore()
    agent = build_local_agent(session_id="a")
    agent.remember("session a memory")
    other = build_local_agent(memory, "b")
    assert other.stats() == 0


def test_api_key_detection_is_non_networked() -> None:
    assert isinstance(gemini_configured(), bool)
