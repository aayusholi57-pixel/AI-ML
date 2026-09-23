# NLP Sentiment Analysis

## Portfolio summary

A two-layer NLP portfolio project: the educational PyTorch/BPE experiment is preserved in the learning archive, while this folder contains a reproducible offline TF-IDF + Logistic Regression baseline with held-out evaluation and a CLI demo.

## Evaluation

The executable evaluation reports **accuracy, precision, recall, and F1** on a fixed held-out split. Metrics are calculated at runtime by `sentiment.py`; no performance numbers are hard-coded into the documentation.

```bash
python sentiment.py
pytest -q
```

## Demo

```bash
python demo.py
```

The demo trains the lightweight baseline locally and accepts sentences interactively.

## Engineering focus

- TF-IDF text features
- Logistic-regression classification
- Held-out evaluation
- Accuracy, precision, recall, and F1
- Deterministic training
- Testable inference entry point

## Transformer connection

The repository root also contains `model.py`, a lazy Hugging Face sentiment pipeline example. It remains separate from the offline benchmark so CI does not require model downloads or API access.

## Limitation

The benchmark dataset is intentionally tiny and educational. Its metrics demonstrate an evaluation workflow, not production-level generalization. A production system should use a larger representative labeled dataset and a locked test set.

## LinkedIn framing

**Built a reproducible NLP sentiment-analysis baseline with TF-IDF and logistic regression, then added held-out evaluation for accuracy, precision, recall, and F1 plus an executable CLI demo and CI tests.**
