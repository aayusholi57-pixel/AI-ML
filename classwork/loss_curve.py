"""
Day 21 · Exercise 1 — watch a network learn (the loss curve)
Training = thousands of tiny "less wrong" steps. Each step lowers the LOSS
(how wrong the network is). MLPClassifier records this in .loss_curve_ so we
can watch it fall. One full pass of steps is roughly one "epoch".
Run with:  python loss_curve.py
Needs:     pip install scikit-learn
"""

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# ---- DATA (real, from Day 16): scale it — neural nets need it ----
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train_s, X_test_s = scaler.transform(X_train), scaler.transform(X_test)

# ---- train and record the loss at every step ----
mlp = MLPClassifier(hidden_layer_sizes=(32,), max_iter=200, random_state=42)
mlp.fit(X_train_s, y_train)

lc = mlp.loss_curve_          # the loss after each training step
print(f"steps taken (iterations): {len(lc)}")
print(f"loss at the start : {lc[0]:.3f}")
print(f"loss after 10     : {lc[10]:.3f}")
print(f"loss at the end   : {lc[-1]:.3f}")
print(f"\ntrain accuracy: {mlp.score(X_train_s, y_train):.3f}")
print(f"test  accuracy: {mlp.score(X_test_s,  y_test):.3f}")
print("\nThe loss falls fast, then flattens — that's the network settling.")
