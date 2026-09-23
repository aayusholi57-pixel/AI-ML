# AI Engineering & Machine Learning Portfolio

A structured AI/ML engineering portfolio covering machine learning, deep learning, NLP, computer vision, LLM applications, RAG, agents, APIs, and reproducible experimentation.

> **Portfolio principle:** the repository preserves the learning journey, but the strongest work is promoted into documented, reusable, testable projects.

## Start here

### Featured engineering projects

| Project | What it demonstrates |
| --- | --- |
| [Exam Preparation RAG](Student%20rags/) | PDF ingestion, chunking, retrieval, grounded Gemini generation, FastAPI |
| [Dal Bhat Image Classifier](cnn/foodclassifier/) | PyTorch, ResNet18 transfer learning, class balancing, Streamlit |
| [Breast Cancer Classification](breastcancer.ipynb) | scikit-learn, preprocessing, classification, evaluation |
| [PyTorch MLP API](new1/) | PyTorch training, reproducibility, model persistence, FastAPI |
| [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/) | Tokenization, embeddings, PyTorch classification |
| [LLM Agent with Memory](projects/llm-agent-memory/) | Gemini, agent tools, LangGraph/LangChain, SQLite memory |
| [RAG Retrieval Lab](projects/rag-retrieval-lab/) | Retrieval experiments and RAG architecture |

**[Open the full portfolio index →](projects/)**

## Engineering capabilities

- Python and software fundamentals
- NumPy, pandas, data cleaning, and visualization
- scikit-learn machine learning workflows
- Feature preprocessing and model evaluation
- PyTorch neural networks and training loops
- CNN and transfer-learning workflows
- NLP tokenization, embeddings, and classification
- LLM APIs and prompt design
- Retrieval-Augmented Generation
- Agents, tool calling, and memory
- FastAPI inference services
- Streamlit ML interfaces
- Git, GitHub, testing, linting, and CI

## Portfolio structure

~~~
AI-ML/
├── projects/                 # curated portfolio entry points
├── Student rags/             # Exam Preparation RAG application
├── cnn/foodclassifier/       # Dal Bhat computer-vision application
├── new1/                     # PyTorch MLP + FastAPI
├── docs/                     # engineering and audit documentation
├── tests/                    # automated tests
├── .github/workflows/        # CI quality checks
└── learning archive/         # original experiments and notebooks
~~~

The learning archive is intentionally preserved. Historical notebook names are not treated as portfolio project names unless the work has been promoted and documented.

## Engineering standards

Promoted projects aim to provide:

- clear problem definition
- reproducible setup
- explicit dependencies
- path-safe code
- input validation
- separated training and inference
- evaluation metrics where meaningful
- documented limitations
- tests for important behavior
- environment-based secrets
- no local databases, caches, checkpoints, or credentials in source control

See [Portfolio Project Standard](projects/PROJECT_STANDARD.md) and [Code Audit](docs/CODE_AUDIT.md).

## Environment

Python 3.10+ is the baseline.

~~~bash
python -m venv .venv
~~~

Windows PowerShell:

~~~powershell
.\\.venv\\Scripts\\Activate.ps1
~~~

Install the core environment:

~~~bash
python -m pip install -r requirements.txt
~~~

Individual portfolio applications may have their own dependency files.

## Maintained APIs

### Core FastAPI example

~~~bash
uvicorn servermodel:app --reload
~~~

### Exam Preparation RAG

~~~bash
python -m pip install -r "Student rags/requirements-rag.txt"
uvicorn "Student rags.app:app" --reload
~~~

### PyTorch MLP API

~~~bash
python new1/train.py
uvicorn new1.main:app --reload
~~~

## Quality checks

~~~bash
python -m py_compile model.py route.py servermodel.py
pytest
ruff check model.py route.py servermodel.py tests
~~~

CI runs these checks for the maintained core entry points.

## Security

Never commit API keys, passwords, tokens, private data, local databases, or generated credentials.

If a credential is ever committed, remove it from the working tree **and rotate/revoke it immediately**. Historical notebook outputs should also be reviewed before public sharing.

## For recruiters and LinkedIn viewers

If you arrive here from LinkedIn, start with:

1. [Portfolio Projects](projects/)
2. [Exam Preparation RAG](Student%20rags/)
3. [Dal Bhat Image Classifier](cnn/foodclassifier/)
4. [PyTorch MLP API](new1/)
5. [LLM Agent with Memory](projects/llm-agent-memory/)
6. [NLP Sentiment Analysis](projects/nlp-sentiment-analysis/)

Each promoted project is documented around **problem → architecture → implementation → evaluation → limitations → future improvements**.

## Author

**Aayush Oli**

AI/ML engineering learner building practical systems across machine learning, deep learning, NLP, computer vision, RAG, agents, and AI application development.
