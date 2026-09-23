# Code and Notebook Audit

This audit separates maintained portfolio code from historical learning material and records the engineering hardening applied to the repository.

## Current inventory

- Python files: 101
- Jupyter notebooks: 118
- The learning archive remains intentionally preserved.

## Engineering hardening completed

### Core Python

- Sentiment model loading is now lazy, preventing model download/network work during import.
- FastAPI examples use validation and path-safe application structure.
- PyTorch MLP training uses deterministic dataset generation and explicit model persistence.
- MLP inference loads weights safely on CPU and reports a clear missing-model response.

### Computer vision

- Dal Bhat Streamlit application is inference-only at startup.
- Training is an explicit command instead of an expensive hidden side effect.
- CV training uses deterministic seeds, validated class folders, balanced sampling, versioned checkpoints, and a reproducible split.
- Model loading uses CPU-safe state loading.

### RAG

- Exam Preparation RAG was separated into reusable retrieval/generation functions.
- Importing the RAG engine does not require an API key or perform model calls.
- PDF loading, chunking, retrieval parameters, and source metadata are validated.
- Knowledge-base construction is cached.
- FastAPI exposes a documented /ask interface.

### Portfolio structure

Dedicated portfolio documentation now exists for:

- Exam Preparation RAG
- Dal Bhat Image Classifier
- PyTorch MLP API
- NLP Sentiment Analysis
- LLM Agent with Memory
- RAG Retrieval Lab

A shared project standard defines the expected portfolio structure: problem, architecture, stack, reproducibility, evaluation, limitations, inference, and future improvements.

## Notebook quality signals

The focused notebook review found historical notebooks containing saved errors and empty cells. Examples included:

- rag_again_full_pipeline.ipynb: 7 saved error outputs and 13 empty code cells
- sentiment_analysis.ipynb: 3 saved error outputs and 15 empty code cells
- Student rags/Exampreparation_RAG.ipynb: 3 saved error outputs and 57 empty code cells
- real_life_gemini_ai_agent.ipynb: 2 empty code cells
- project5.ipynb: 1 empty code cell
- cnn/cnn10.ipynb: 9 empty code cells

These notebooks are retained as learning evidence. Promoted project pages point reviewers toward maintained implementations rather than pretending every historical cell is production-ready.

## Security finding and remediation

A historical agent notebook contained a hardcoded Google API credential in source. The credential was removed and replaced with environment-variable configuration.

**Action required outside Git history:** if that credential was real and ever usable, it must be revoked/rotated at the provider. Removing it from the latest tree does not invalidate a credential that may exist in earlier commits.

Future notebook review should also inspect saved outputs for accidentally exposed credentials before public publication.

## Naming and archive strategy

Wholesale renaming of historical folders was deliberately avoided where notebook-relative paths, imports, datasets, or binary assets could break. Portfolio-facing project names are standardized in the curated project index while historical learning paths remain stable.

## Quality policy

New promoted projects should include:

- clear README and architecture
- explicit dependencies
- deterministic or documented data preparation
- input validation
- tests for important behavior
- evaluation metrics and limitations
- no secrets or generated local artifacts
- a clear distinction between experiment, demo, and production-ready component
