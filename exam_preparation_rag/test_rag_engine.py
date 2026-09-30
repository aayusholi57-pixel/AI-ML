"""Tests for the local retrieval layer of Exam Preparation RAG."""
from pathlib import Path
import sys

import pytest

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
    assert all(0.0 <= result["score"] <= 1.0 for result in results)
    assert "SOURCE 1" in build_context(results)


def test_small_corpus_falls_back_without_svd() -> None:
    chunks = [{"source": "notes.pdf", "page": 1, "text": "Python functions and variables."}]
    vectorizer, svd, normalizer, index = create_index(chunks)
    assert svd is None
    results = retrieve("Python functions", chunks, vectorizer, svd, normalizer, index, k=1)
    assert len(results) == 1
    assert results[0]["source"] == "notes.pdf"


@pytest.mark.parametrize("question", ["", "   "])
def test_rejects_empty_questions(question: str) -> None:
    chunks = [{"source": "notes.pdf", "page": 1, "text": "Python functions and variables."}]
    vectorizer, svd, normalizer, index = create_index(chunks)
    with pytest.raises(ValueError, match="non-empty"):
        retrieve(question, chunks, vectorizer, svd, normalizer, index)
