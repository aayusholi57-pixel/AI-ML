# Learning History — Days 22–34

This section preserves the progression of the AI/ML learning journey while making the meaningful experiments easier to understand on GitHub.

## Progression

| Day | Learning milestone | Highlight |
|---|---|---|
| 22 | Scikit-learn MLP on the digits dataset | Neural-network classification with train/test split, scaling, cross-validation and accuracy evaluation |
| 23 | No day-23 folder currently present | Preserved as a documented gap rather than inventing missing work |
| 24 | Word vectors + TF-IDF sentiment foundations | Handmade vector representations and a small text-classification experiment |
| 25 | Semantic-search foundations | TF-IDF retrieval, cosine similarity and ML concept knowledge-base work |
| 26 | Knowledge-base semantic search | Expanded retrieval knowledge base and semantic-search workflow |
| 27 | PyTorch foundations | Tensor/autograd setup and linear-regression learning experiments |
| 28 | PyTorch model building | Linear regression and an MLP digit classifier |
| 29 | PyTorch sentiment classifier | End-to-end tokenization, embeddings, pooling, classification, training and evaluation |
| 30 | AI text analyzer | Hugging Face tokenization, token IDs and text-analysis workflow |
| 31 | Complete RAG engine | Retrieval pipeline and a larger real-world RAG experiment |
| 32 | Full RAG pipeline | Chunks, TF-IDF/SVD retrieval and pipeline integration |
| 33 | RAG evaluation + agentic RAG experiment | Ragas evaluation work plus a LangGraph/Chroma experiment |
| 34 | LLM agent with memory | LangChain/LangGraph agent workflow with SQLite-style memory concepts |

## Renamed learning artifacts

Meaningful notebooks have been renamed from generic Jupyter names such as `Untitled.ipynb` while preserving their contents:

- `day22/neural_network_digits_mlp.ipynb`
- `day 24/handmade_word_vectors.ipynb`
- `day 24/tfidf_sentiment_basics.ipynb`
- `day 25/semantic_search_basics.ipynb`
- `day 26/knowledge_base_semantic_search.ipynb`
- `day 27/pytorch_setup_basics.ipynb`
- `day 27/pytorch_linear_regression.ipynb`
- `day 28/pytorch_linear_model.ipynb`
- `day 28/pytorch_mlp_digits_classifier.ipynb`
- `day 29/pytorch_sentiment_classifier.ipynb`
- `day 30/ai_text_analyzer.ipynb`
- `day 31/complete_rag_engine.ipynb`
- `day 32/rag_full_pipeline_completed.ipynb`
- `day 33/ragas_evaluation.ipynb`

The empty Day 31 scratch notebook was removed because it contained no learning content.

## Portfolio connection

The strongest progression in this range is:

**traditional ML → NLP/vector representations → PyTorch → sentiment classification → text analysis → RAG → RAG evaluation → LLM agents with memory**

The later learning artifacts directly connect to the maintained projects under `projects/`, especially the NLP sentiment, RAG, and LLM-agent work.

## Historical-artifact policy

These notebooks are learning history, not production applications. They are intentionally preserved as evidence of experimentation and progression. Production-quality implementations belong under `projects/` with tests, requirements and documentation.

## Security note

During the audit, `day 33/new_data.ipynb` was found to contain a credential-like API key assignment in its historical notebook source. Do not use or publish that credential. Any real credential that was ever committed should be revoked/rotated at its provider; removing it from a current file does not invalidate Git history.
