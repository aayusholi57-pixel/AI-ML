# AI Engineering & Machine Learning Portfolio

[![CI](https://github.com/aayusholi57-pixel/AI-ML/actions/workflows/quality.yml/badge.svg)](https://github.com/aayusholi57-pixel/AI-ML/actions/workflows/quality.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-not%20specified-lightgrey)](https://github.com/aayusholi57-pixel/AI-ML)

A practical AI/ML engineering portfolio covering classical machine learning, deep learning, NLP, computer vision, RAG, LLM agents, APIs, evaluation, testing, and reproducible experimentation.

> **Portfolio principle:** learning history is preserved as evidence of progression; promoted projects are organized as reusable, documented, testable engineering work.

## Start here

If you are reviewing this repository for an internship, start with the **[Portfolio Projects](projects/)** index and then open the featured projects below.

### Featured engineering projects

| Project | What it demonstrates |
| --- | --- |
| [Exam Preparation RAG](exam_preparation_rag/) | PDF ingestion, retrieval, grounded Gemini generation, FastAPI |
| [Dal Bhat Image Classifier](computer_vision/dal_bhat_classifier/) | PyTorch, ResNet18 transfer learning, class-aware training, Streamlit |
| [Breast Cancer Classification](projects/breast-cancer-classification/) | Leakage-safe preprocessing, Logistic Regression, stratified evaluation |
| [PyTorch MLP API](pytorch_mlp_api/) | Deterministic training, model persistence, FastAPI inference |
| [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/) | TF-IDF, Logistic Regression, precision/recall/F1 evaluation |
| [LLM Agent with Memory](projects/llm-agent-memory/) | Session-scoped SQLite memory, agent abstractions, Gemini-ready configuration |
| [RAG Retrieval Lab](projects/rag-retrieval-lab/) | Retrieval experiments, ranking behavior, RAG architecture |

**[Open the full portfolio index →](projects/)**

## Engineering capabilities

- Python, packaging, virtual environments, and clean module design
- NumPy, pandas, visualization, and data preparation
- scikit-learn pipelines, preprocessing, validation, and metrics
- PyTorch tensors, autograd, neural networks, and training loops
- CNNs and transfer learning
- NLP tokenization, TF-IDF, embeddings, and classification
- LLM APIs, prompt design, and grounded generation
- Retrieval-Augmented Generation and semantic search
- Agent architecture, tools, and persistent memory
- FastAPI inference services and API validation
- Streamlit ML applications
- Git/GitHub workflows, automated tests, linting, dependency management, and CI

## Portfolio architecture

```text
AI-ML/
├── projects/                         # curated portfolio projects
├── exam_preparation_rag/             # Exam Preparation RAG application
├── computer_vision/
│   └── dal_bhat_classifier/          # Dal Bhat computer-vision application
├── pytorch_mlp_api/                  # PyTorch MLP + FastAPI
├── tests/                            # automated regression tests
├── docs/                             # standards, audits, references
├── learning-history/                 # preserved learning progression
├── day22 ... day34/                  # original learning experiments
└── .github/workflows/                # automated validation
```

Historical notebooks and reference material are preserved under the learning/documentation areas so the repository remains a learning record without overwhelming the portfolio entry point.

## Engineering standards

Promoted projects follow these principles where applicable:

- clear problem definition and scope
- reproducible execution
- explicit, pinned dependencies
- path-safe code
- input validation
- training/inference separation
- meaningful evaluation metrics
- documented limitations
- automated tests
- environment-based secrets
- no local databases, model checkpoints, caches, or credentials committed as runtime artifacts

See [Portfolio Project Standard](projects/PROJECT_STANDARD.md), [Portfolio Guide](docs/PORTFOLIO.md), [Code Audit](docs/CODE_AUDIT.md), and the [Internship Readiness Review](docs/INTERNSHIP_READINESS.md).

## Environment

Python 3.10+ is the baseline.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Individual applications have their own dependency files when they need isolated stacks.

## Run the maintained APIs

### Core FastAPI example

```bash
uvicorn servermodel:app --reload
```

### Exam Preparation RAG

```bash
python -m pip install -r "exam_preparation_rag/requirements-rag.txt"
uvicorn exam_preparation_rag.app:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive FastAPI documentation.

### PyTorch MLP API

```bash
python pytorch_mlp_api/train.py
uvicorn pytorch_mlp_api.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive API.

## Quality gates

Run the core checks locally:

```bash
python -m py_compile model.py route.py servermodel.py
pytest tests/test_api.py -q
ruff check model.py route.py servermodel.py tests
```

GitHub Actions validates the maintained MLP, RAG retrieval, vision, NLP, breast-cancer, agent, and core API projects with dedicated jobs.

## Security

Never commit API keys, passwords, access tokens, private data, local databases, or generated credentials.

If a credential is ever committed, remove it from the working tree **and rotate/revoke it at the provider**. Historical notebook outputs should also be reviewed before redistribution.

See [SECURITY.md](SECURITY.md).

## Learning progression

The repository records progression from:

**Python → traditional ML → NLP/vector representations → semantic search → PyTorch → computer vision → RAG → RAG evaluation → LLM agents → API/application engineering**

See [Learning History](learning-history/).

## For recruiters and internship reviewers

Recommended review path:

1. [Portfolio Projects](projects/)
2. [Exam Preparation RAG](exam_preparation_rag/)
3. [Dal Bhat Image Classifier](computer_vision/dal_bhat_classifier/)
4. [Breast Cancer Classification](projects/breast-cancer-classification/)
5. [PyTorch MLP API](pytorch_mlp_api/)
6. [LLM Agent with Memory](projects/llm-agent-memory/)
7. [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/)

Each promoted project is organized around **problem → architecture → implementation → evaluation → limitations → future improvements**.

## Contributing and maintenance

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and [CITATION.cff](CITATION.cff) for repository citation metadata.

## Author

**Aayush Oli**

AI/ML engineer-in-training building practical systems across machine learning, deep learning, NLP, computer vision, RAG, agents, APIs, and software engineering.
