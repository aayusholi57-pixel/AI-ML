"""
Day 21 · Exercise 2 — the learning rate (step size)
Gradient descent nudges weights by:  new = old - (learning_rate * slope).
Too SMALL and it crawls (never arrives in the time we give it); too BIG and it
overshoots and thrashes. There's a "just right" middle. Let's see all three.
Run with:  python learning_rate.py
Needs:     pip install scikit-learn
"""

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# ---- DATA: scale it ----
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler().fit(X_train)
X_train_s, X_test_s = scaler.transform(X_train), scaler.transform(X_test)

print("learning_rate   final_loss   test_acc")
for lr in [0.0001, 0.001, 0.01, 0.1, 1.0]:
    mlp = MLPClassifier(hidden_layer_sizes=(32,), learning_rate_init=lr,
                        max_iter=200, random_state=42)
    mlp.fit(X_train_s, y_train)
    print(f"  {lr:<12} {mlp.loss_curve_[-1]:8.3f}   {mlp.score(X_test_s, y_test):.3f}")

print("\nToo small -> loss still high (didn't arrive). Too big -> unstable.")
print("A middle value (about 0.01) learns fast AND lands well.")
