"""Execution tests for the local retrieval layer of Exam Preparation RAG."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from rag_engine import build_context, create_chunks, create_index, load_pdfs, retrieve  # noqa: E402


def test_real_study_pdfs_build_a_retrieval_index() -> None:
    documents = load_pdfs(PROJECT_DIR / "documents")
    assert documents
    chunks = create_chunks(documents)
    vectorizer, svd, normalizer, index = create_index(chunks)
    results = retrieve(
        "software engineering requirements", chunks, vectorizer, svd, normalizer, index, k=3
    )
    assert results
    assert len(results) <= 3
    assert all(result["source"] and result["page"] >= 1 for result in results)
    assert "SOURCE 1" in build_context(results)
