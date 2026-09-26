"""Reusable Exam Preparation RAG engine.

Importing this module has no network or model-loading side effects.
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
MODEL_NAME = "gemini-2.5-flash"


def load_pdfs(documents_dir: Path = DOCUMENTS_DIR) -> list[dict[str, Any]]:
    """Load non-empty text pages from PDFs."""
    if not documents_dir.is_dir():
        raise FileNotFoundError(f"Documents folder was not found: {documents_dir}")
    documents = []
    for pdf_path in sorted(documents_dir.glob("*.pdf")):
        with pymupdf.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                if text:
                    documents.append({"source": pdf_path.name, "page": page_number, "text": text})
    if not documents:
        raise ValueError(f"No readable PDF text was found in {documents_dir}")
    return documents


def create_chunks(documents: list[dict[str, Any]], chunk_size: int = 800, overlap: int = 100):
    """Split page text into overlapping character chunks."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller than chunk_size")
    chunks = []
    step = chunk_size - overlap
    for document in documents:
        text = str(document["text"])
        for start in range(0, len(text), step):
            chunk_text = text[start:start + chunk_size].strip()
            if chunk_text:
                chunks.append({"source": document["source"], "page": document["page"], "text": chunk_text})
            if start + chunk_size >= len(text):
                break
    if not chunks:
        raise ValueError("No chunks were created from the supplied documents")
    return chunks


def create_index(chunks: list[dict[str, Any]]):
    """Create a normalized TF-IDF/SVD retrieval index."""
    if not chunks:
        raise ValueError("chunks cannot be empty")
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10_000)
    matrix = vectorizer.fit_transform([chunk["text"] for chunk in chunks])
    max_components = min(matrix.shape[0] - 1, matrix.shape[1] - 1, 100)
    if max_components < 1:
        raise ValueError("Not enough vocabulary/chunks to create an SVD index")
    svd = TruncatedSVD(n_components=max_components, random_state=42)
    reduced = svd.fit_transform(matrix)
    normalizer = Normalizer()
    return vectorizer, svd, normalizer, normalizer.fit_transform(reduced)


def retrieve(question: str, chunks, vectorizer, svd, normalizer, index, k: int = 3):
    """Return the highest-scoring chunks for a question."""
    if not question.strip():
        raise ValueError("question must be non-empty")
    if k < 1:
        raise ValueError("k must be at least 1")
    query_vector = normalizer.transform(svd.transform(vectorizer.transform([question.strip()])))
    scores = index @ query_vector[0]
    return [
        {"source": chunks[i]["source"], "page": chunks[i]["page"],
         "text": chunks[i]["text"], "score": float(scores[i])}
        for i in scores.argsort()[::-1][:k]
    ]


def build_context(results):
    """Format retrieved chunks with source metadata."""
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
    """Generate an answer grounded only in retrieved study material."""
    instructions = {
        "explain": "Explain clearly for a student.",
        "short": "Give a concise exam-oriented answer.",
        "5-mark": "Write a structured 5-mark answer.",
        "mcq": "Create 5 MCQs with four options, answers, and brief explanations.",
    }
    instruction = instructions.get(mode, instructions["explain"])
    prompt = f"""You are an Exam Preparation RAG assistant.
Answer ONLY from the supplied study material. Do not invent facts or use outside knowledge.
If the material is insufficient, say: "I couldn't find enough information in the provided study material."

Mode: {mode}
Instructions: {instruction}

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
    return response.choices[0].message.content or ""


@lru_cache(maxsize=1)
def knowledge_base():
    """Build and cache the local retrieval index."""
    documents = load_pdfs()
    chunks = create_chunks(documents)
    vectorizer, svd, normalizer, index = create_index(chunks)
    return chunks, vectorizer, svd, normalizer, index


def exam_rag(question: str, mode: str = "explain", k: int = 3):
    """Retrieve study material and generate a grounded answer."""
    chunks, vectorizer, svd, normalizer, index = knowledge_base()
    results = retrieve(question, chunks, vectorizer, svd, normalizer, index, k)
    return {"answer": generate_answer(question, build_context(results), mode), "sources": results}


if __name__ == "__main__":
    print("Exam Preparation RAG — type exit to quit.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() == "exit":
            break
        try:
            result = exam_rag(question)
            print("\n" + result["answer"])
            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source['source']} | page {source['page']} | score {source['score']:.4f}")
        except Exception as error:
            print(f"Error: {error}")
