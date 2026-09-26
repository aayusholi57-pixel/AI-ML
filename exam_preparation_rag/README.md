# Exam Preparation RAG

A retrieval-augmented generation system that answers student questions from a local collection of PDF study material.

## Architecture

1. Load PDF pages from `documents/`
2. Split page text into overlapping chunks
3. Build a TF-IDF representation
4. Reduce the representation with TruncatedSVD
5. Normalize vectors and rank chunks by cosine similarity
6. Send only retrieved context to Gemini through the OpenAI-compatible API
7. Return the answer together with source filename, page, and retrieval score

## Run

Install the project dependencies:

```bash
python -m pip install -r requirements-rag.txt
```

Set `GOOGLE_API_KEY` in a local `.env` file, then:

```bash
uvicorn exam_preparation_rag.app:app --reload
```

The API documentation is available at `/docs`.

For terminal use:

```bash
python exam_preparation_rag/rag_engine.py
```

## Important limitation

Retrieval quality depends on the study material and TF-IDF vocabulary. This is an educational RAG implementation, not a claim of production-grade retrieval quality.
