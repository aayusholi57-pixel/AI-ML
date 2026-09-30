"""Core retrieval and grounded generation for the Exam Preparation RAG application.

The retrieval layer is deterministic and local. Gemini is contacted only when an
answer is requested, so importing this module is safe for tests and tooling.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import pymupdf
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
load_dotenv(BASE_DIR.parent / ".env")

MODEL_NAME = os.getenv("EXAM_RAG_MODEL", "gemini-2.5-flash")
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_TOP_K = 3
MAX_TOP_K = 10


def load_pdfs(documents_dir: Path = DOCUMENTS_DIR) -> list[dict[str, Any]]:
    """Extract non-empty PDF pages with stable source and page metadata."""
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"Documents folder was not found: {documents_dir}")

    documents: list[dict[str, Any]] = []
    for pdf_path in sorted(documents_dir.glob("*.pdf")):
        with pymupdf.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                if text:
                    documents.append(
                        {"source": pdf_path.name, "page": page_number, "text": text}
                    )

    if not documents:
        raise ValueError(f"No readable PDF text was found in {documents_dir}")
    return documents


def create_chunks(
    documents: list[dict[str, Any]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    """Split pages into overlapping character chunks while preserving provenance."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size")

    chunks: list[dict[str, Any]] = []
    step = chunk_size - overlap

    for document in documents:
        text = str(document["text"]).strip()
        for start in range(0, len(text), step):
            chunk_text = text[start : start + chunk_size].strip()
            if chunk_text:
                chunks.append(
                    {
                        "source": str(document["source"]),
                        "page": int(document["page"]),
                        "text": chunk_text,
                    }
                )
            if start + chunk_size >= len(text):
                break

    if not chunks:
        raise ValueError("No chunks were created from the supplied documents")
    return chunks


def create_index(chunks: list[dict[str, Any]]):
    """Create a normalized TF-IDF/SVD index.

    Very small corpora do not contain enough dimensions for SVD, so the
    implementation gracefully falls back to normalized TF-IDF vectors.
    """
    if not chunks:
        raise ValueError("chunks cannot be empty")

    texts = [chunk["text"] for chunk in chunks]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10_000)
    matrix = vectorizer.fit_transform(texts)

    if matrix.shape[0] >= 2 and matrix.shape[1] >= 2:
        max_components = min(matrix.shape[0] - 1, matrix.shape[1] - 1, 100)
        svd = TruncatedSVD(n_components=max_components, random_state=42)
        reduced = svd.fit_transform(matrix)
        normalizer = Normalizer()
        index = normalizer.fit_transform(reduced)
    else:
        svd = None
        normalizer = Normalizer()
        index = normalizer.fit_transform(matrix)

    return vectorizer, svd, normalizer, index


def retrieve(
    question: str,
    chunks: list[dict[str, Any]],
    vectorizer: TfidfVectorizer,
    svd: TruncatedSVD | None,
    normalizer: Normalizer,
    index,
    k: int = DEFAULT_TOP_K,
) -> list[dict[str, Any]]:
    """Return the highest-scoring chunks for a question."""
    question = question.strip()
    if not question:
        raise ValueError("question must be non-empty")
    if not 1 <= k <= MAX_TOP_K:
        raise ValueError(f"k must be between 1 and {MAX_TOP_K}")

    query = vectorizer.transform([question])
    query_vector = normalizer.transform(svd.transform(query) if svd else query)

    scores = index @ query_vector.T
    scores = scores.toarray().ravel() if hasattr(scores, "toarray") else scores.ravel()

    ranked = scores.argsort()[::-1][: min(k, len(chunks))]
    return [
        {
            "source": chunks[i]["source"],
            "page": chunks[i]["page"],
            "text": chunks[i]["text"],
            "score": float(scores[i]),
        }
        for i in ranked
    ]


def build_context(results: list[dict[str, Any]]) -> str:
    """Format retrieved chunks for the generation prompt."""
    return "\n\n".join(
        f"SOURCE {i}\nFile: {item['source']}\nPage: {item['page']}\n\n{item['text']}"
        for i, item in enumerate(results, start=1)
    )


def _client() -> OpenAI:
    """Create the Gemini OpenAI-compatible client only when generation is requested."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured")

    return OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


def generate_answer(question: str, context: str, mode: str = "explain") -> str:
    """Generate an answer constrained to the retrieved study material."""
    instructions = {
        "explain": "Explain clearly for a student.",
        "short": "Give a concise exam-oriented answer.",
        "5-mark": "Write a structured 5-mark answer with headings or bullet points.",
        "mcq": "Create 5 MCQs with four options, answers, and brief explanations.",
    }
    if mode not in instructions:
        raise ValueError(f"Unsupported mode: {mode}")

    prompt = f"""You are an Exam Preparation RAG assistant.

Answer ONLY from the supplied study material. Do not invent facts or use outside
knowledge. If the material is insufficient, say exactly:
"I couldn't find enough information in the provided study material."

Mode: {mode}
Instructions: {instructions[mode]}

STUDY MATERIAL
{context}

QUESTION
{question}
"""

    response = _client().chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Ground every answer in the supplied study material."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return (response.choices[0].message.content or "").strip()


@lru_cache(maxsize=1)
def knowledge_base():
    """Build and cache the retrieval index for the local study PDFs."""
    documents = load_pdfs()
    chunks = create_chunks(documents)
    vectorizer, svd, normalizer, index = create_index(chunks)
    return chunks, vectorizer, svd, normalizer, index


def clear_knowledge_base_cache() -> None:
    """Clear the cached index after study PDFs are added or replaced."""
    knowledge_base.cache_clear()


def exam_rag(question: str, mode: str = "explain", k: int = DEFAULT_TOP_K):
    """Retrieve evidence and generate a grounded exam-preparation answer."""
    chunks, vectorizer, svd, normalizer, index = knowledge_base()
    results = retrieve(question, chunks, vectorizer, svd, normalizer, index, k)
    return {
        "answer": generate_answer(question, build_context(results), mode),
        "sources": results,
    }


if __name__ == "__main__":
    print("Exam Preparation RAG — type 'exit' to quit.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() == "exit":
            break
        try:
            result = exam_rag(question)
            print("\n" + result["answer"])
            print("\nSources:")
            for source in result["sources"]:
                print(
                    f"- {source['source']} | page {source['page']} "
                    f"| score {source['score']:.4f}"
                )
        except Exception as error:
            print(f"Error: {error}")
