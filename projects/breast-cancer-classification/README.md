# Breast Cancer Classification

## Portfolio summary

A reproducible binary-classification project based on the repository's existing breast-cancer CSV and original notebook. The maintained implementation uses a leakage-safe scikit-learn pipeline with feature standardization and logistic regression.

## Evaluation

The benchmark uses a fixed **80/20 stratified holdout** with `random_state=42` and calculates accuracy, precision, recall, and F1 at runtime.

Run:

```bash
python train.py
pytest -q
```

## Demo

```bash
python demo.py
```

The demo trains the model and prints the measured holdout metrics.

## Engineering focus

- Dataset validation
- Explicit feature selection
- Stratified train/test split
- StandardScaler + LogisticRegression pipeline
- Accuracy, precision, recall, and F1
- Reproducible evaluation
- Automated tests

## Important limitation

This is an educational machine-learning benchmark, **not a medical diagnostic system**. The reported metrics describe this dataset and split only and should not be interpreted as clinical performance.

The original `breastcancer.ipynb` is retained as the learning notebook and historical experiment.

## LinkedIn framing

**Built a reproducible breast-cancer classification benchmark using a leakage-safe scikit-learn pipeline, stratified holdout evaluation, and automated tests for dataset integrity, metrics, and inference.**
