# Exam Preparation RAG

A portfolio-grade retrieval-augmented generation service for answering exam questions from a local PDF knowledge base.

## What it demonstrates

- PDF ingestion with page-level provenance
- Overlapping chunking
- TF-IDF retrieval with an optional SVD acceleration layer
- Graceful fallback for very small corpora
- Grounded Gemini generation through an OpenAI-compatible client
- FastAPI serving with typed request validation
- Health/readiness endpoints
- Automated retrieval tests

## Architecture

`PDF study material → page extraction → chunking → TF-IDF → optional SVD → cosine ranking → grounded Gemini → source metadata`

The generator is explicitly instructed to refuse unsupported answers instead of filling gaps with outside knowledge.

## Setup

From the repository root:

```bash
python -m pip install -r exam_preparation_rag/requirements-rag.txt
```

Create a `.env` file in the repository root:

```env
GOOGLE_API_KEY=your_key_here
```

Do not commit the real key.

## Run

```bash
uvicorn exam_preparation_rag.app:app --reload
```

Open `/docs` for Swagger UI.

Endpoints:
- `GET /` — service metadata
- `GET /health` — process health
- `GET /ready` — builds/verifies the local retrieval index
- `POST /ask` — retrieves evidence and generates a grounded answer

Example:
```json
{"question":"What are software requirements?","mode":"5-mark","k":3}
```

## CLI

```bash
python exam_preparation_rag/rag_engine.py
```

## Test

```bash
python -m pytest exam_preparation_rag/test_rag_engine.py -q
```

The tests cover real PDF ingestion, retrieval, provenance, small-corpus fallback, and invalid questions.

## Engineering note

This is a compact educational/portfolio RAG. TF-IDF is deterministic, inexpensive, and inspectable. A future dense-embedding evaluator can be added without changing the API contract.
