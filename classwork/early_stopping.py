"""
Day 21 · Exercise 3 — overfitting & early stopping (Day 14, for neural nets)
Networks have huge capacity, so given a NOISY dataset they can MEMORISE the
training rows (train acc ~1.0) while doing poorly on new data — a big train/test
gap. 'early_stopping' watches a validation slice and halts when it stops
improving, keeping the network honest.
Run with:  python early_stopping.py
Needs:     pip install scikit-learn
"""

from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# ---- DATA: a deliberately NOISY dataset (label noise + 35 useless features) ----
X, y = make_classification(n_samples=600, n_features=40, n_informative=5,
                           n_redundant=0, n_repeated=0, flip_y=0.15,
                           class_sep=0.7, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=0, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train_s, X_test_s = scaler.transform(X_train), scaler.transform(X_test)

big = dict(hidden_layer_sizes=(200, 200), max_iter=1000, random_state=0)

# 1) no early stopping — the big net MEMORISES the training set
plain = MLPClassifier(**big).fit(X_train_s, y_train)
tr, te = plain.score(X_train_s, y_train), plain.score(X_test_s, y_test)
print("No early stopping:")
print(f"  train acc {tr:.3f} | test acc {te:.3f}   (gap {tr - te:.3f}  <- overfitting!)")

# 2) early stopping — halt when a validation slice stops improving
stopped = MLPClassifier(early_stopping=True, validation_fraction=0.2,
                        n_iter_no_change=15, **big).fit(X_train_s, y_train)
tr2, te2 = stopped.score(X_train_s, y_train), stopped.score(X_test_s, y_test)
print("With early stopping:")
print(f"  train acc {tr2:.3f} | test acc {te2:.3f}   (gap {tr2 - te2:.3f})")
print(f"  stopped after {stopped.n_iter_} steps instead of 1000")

print("\nPerfect on train, weak on test = memorising, not learning. Early stopping")
print("shrinks the gap and generalises better with far less training (Day 14).")
