# AI Engineering & Machine Learning Portfolio

A practical engineering repository covering Python, data analysis, machine learning, deep learning, NLP, computer vision, LLM applications, RAG, APIs, and experimentation.

This repository is organized as an evolving engineering workspace: fundamentals first, then progressively more applied AI systems. Each notebook or script is kept close to the original learning context while reusable code is separated into clearer modules where practical.

## What this repository demonstrates

- Python programming and problem solving
- NumPy, pandas, visualization, and data cleaning
- SQL and SQLite fundamentals
- Classical machine learning with scikit-learn
- Regression, classification, preprocessing, evaluation, and model selection
- Neural networks, CNNs, RNNs, and training concepts
- NLP, tokenization, and sentiment analysis
- LLM application patterns and API integration
- Retrieval-Augmented Generation (RAG)
- Semantic search and vector databases
- AI agents and memory concepts
- FastAPI model-serving fundamentals
- Reproducible Python environments and Git workflows

## Engineering principles

The repository follows a few rules:

1. Keep experiments reproducible
2. Keep secrets out of source control
3. Prefer small, testable Python modules over hidden notebook logic
4. Use explicit dependencies
5. Document assumptions and data sources
6. Separate generated artifacts, caches, and local environments from source code

## Environment

Python 3.10+ is the intended baseline.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the core environment:

```bash
python -m pip install -r requirements.txt
```

For the broader AI/RAG experiments, use the dependency set documented in `requirement.txt` when the specific notebook requires it.

## Running the FastAPI example

The repository contains a small API example in `servermodel.py`.

```bash
uvicorn servermodel:app --reload
```

Then open the local API documentation at `/docs`.

## Project areas

| Area | Focus |
| --- | --- |
| Python | Syntax, functions, collections, files, and problem solving |
| Data | pandas, NumPy, CSV workflows, cleaning, and visualization |
| Machine Learning | Regression, classification, preprocessing, evaluation |
| Deep Learning | Neural networks, CNNs, RNNs, training experiments |
| NLP | Tokenization and sentiment analysis |
| Generative AI | LLM calls, agents, RAG, semantic search |
| APIs | FastAPI model-serving examples |
| Experiments | Small experiments and exploratory notebooks |

## Public-repository hygiene

Local environments, notebook checkpoints, Python caches, database files, credentials, and generated vector-store files should not be committed.

Never place real API keys in this repository. Copy `.env.example` to `.env` locally and provide real credentials only through your local environment or a secret manager.

## Status

This is an actively maintained AI/ML engineering portfolio. Older experiments are retained as learning evidence, while reusable projects are progressively cleaned, documented, tested, and promoted into standalone applications.

## Author

**Aayush Oli**

AI/ML Engineering learner building practical systems across machine learning, deep learning, NLP, RAG, agents, and AI application development.
