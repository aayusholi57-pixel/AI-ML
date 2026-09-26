# AI Engineering & Machine Learning Portfolio

A practical AI/ML engineering portfolio covering classical machine learning, deep learning, NLP, computer vision, RAG, LLM agents, APIs, evaluation, testing, and reproducible experimentation.

> **Portfolio principle:** learning history is preserved as evidence of progression; promoted projects are organized as reusable, documented, testable engineering work.

## Start here

### Featured engineering projects

| Project | What it demonstrates |
| --- | --- |
| [Exam Preparation RAG](exam_preparation_rag/) | PDF ingestion, chunking, TF-IDF/SVD retrieval, grounded Gemini generation, FastAPI |
| [Dal Bhat Image Classifier](computer_vision/foodclassifier/) | PyTorch, ResNet18 transfer learning, class-aware training, Streamlit inference |
| [Breast Cancer Classification](projects/breast-cancer-classification/) | Leakage-safe preprocessing, Logistic Regression, stratified evaluation |
| [PyTorch MLP API](pytorch_mlp_api/) | Deterministic data generation, PyTorch training, persistence, FastAPI inference |
| [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/) | TF-IDF features, Logistic Regression, precision/recall/F1 evaluation |
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
- Git/GitHub workflows, automated tests, linting, and CI

## Portfolio architecture

~~~text
AI-ML/
├── projects/                 # curated, documented portfolio projects
├── exam_preparation_rag/             # Exam Preparation RAG application
├── computer_vision/foodclassifier/       # Dal Bhat computer-vision application
├── pytorch_mlp_api/                     # PyTorch MLP + FastAPI
├── docs/                     # portfolio standards and engineering audits
├── tests/                    # core automated tests
├── learning-history/         # curated map of the learning progression
├── day22 ... day34/          # original learning experiments
└── .github/workflows/        # automated project validation
~~~

Historical notebooks are intentionally preserved. They show how the work evolved and are clearly separated from the maintained project implementations.

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

See [Portfolio Project Standard](projects/PROJECT_STANDARD.md), [Portfolio Guide](docs/PORTFOLIO.md), and [Code Audit](docs/CODE_AUDIT.md).

## Environment

Python 3.10+ is the baseline.

~~~bash
python -m venv .venv
python -m pip install -r requirements.txt
~~~

Windows PowerShell:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

Individual applications have their own dependency files when they need isolated stacks.

## Run the maintained APIs

### Core FastAPI example

~~~bash
uvicorn servermodel:app --reload
~~~

### Exam Preparation RAG

~~~bash
python -m pip install -r "exam_preparation_rag/requirements-rag.txt"
uvicorn exam_preparation_rag.app:app --reload
~~~

### PyTorch MLP API

~~~bash
python pytorch_mlp_api/train.py
uvicorn pytorch_mlp_api.main:app --reload
~~~

## Quality gates

Run the core checks locally:

~~~bash
python -m py_compile model.py route.py servermodel.py
pytest
ruff check model.py route.py servermodel.py tests
~~~

GitHub Actions also validates the maintained MLP, RAG retrieval, vision, NLP, breast-cancer, and agent projects with dedicated jobs.

## Security

Never commit API keys, passwords, access tokens, private data, local databases, or generated credentials.

If a credential is ever committed, remove it from the working tree **and rotate/revoke it at the provider**. Historical notebook outputs should be treated as potentially sensitive and reviewed before redistribution.

## Learning progression

The current learning-history map covers Days 22–34:

**traditional ML → NLP/vector representations → semantic search → PyTorch → sentiment classification → text analysis → RAG → RAG evaluation → LLM agents with memory**

See [Learning History — Days 22–34](learning-history/).

## For recruiters and LinkedIn viewers

Recommended path:

1. [Portfolio Projects](projects/)
2. [Exam Preparation RAG](exam_preparation_rag/)
3. [Dal Bhat Image Classifier](computer_vision/foodclassifier/)
4. [Breast Cancer Classification](projects/breast-cancer-classification/)
5. [PyTorch MLP API](pytorch_mlp_api/)
6. [LLM Agent with Memory](projects/llm-agent-memory/)
7. [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/)

Each promoted project is organized around **problem → architecture → implementation → evaluation → limitations → future improvements**.

## Author

**Aayush Oli**

AI/ML engineer-in-training building practical systems across machine learning, deep learning, NLP, computer vision, RAG, agents, APIs, and software engineering.
