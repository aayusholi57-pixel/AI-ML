# Day 21 — Homework (your 2-hour self-study)

Do these before Day 22.

## 1. Three loss curves on one chart
Train the cancer MLP at `learning_rate_init` = 0.0001, 0.01, and 1.0. Plot all three
`loss_curve_`s on the same axes with matplotlib. Label which one is "too small".
```python
import matplotlib.pyplot as plt
# ... train each, then:
plt.plot(mlp.loss_curve_, label=f"lr={lr}")
plt.xlabel("step"); plt.ylabel("loss"); plt.legend(); plt.show()
```

## 2. Sweep the regularisation strength
On the **noisy** data (`make_classification` from `early_stopping.py`), sweep
`alpha` = 0.0001, 0.01, 1.0 on the big `(200, 200)` net. Which test accuracy is best?
Does a bigger `alpha` shrink the train/test gap?

## 3. Predict then run
```python
# Before running: a HUGE net vs a SMALL net on the noisy data — which overfits more?
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=40, n_informative=5,
                           flip_y=0.15, class_sep=0.7, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=0, stratify=y)
s = StandardScaler().fit(Xtr); Xtr, Xte = s.transform(Xtr), s.transform(Xte)

for size in [(4,), (200, 200)]:
    m = MLPClassifier(hidden_layer_sizes=size, max_iter=1000, random_state=0).fit(Xtr, ytr)
    print(size, "train", round(m.score(Xtr, ytr), 3), "test", round(m.score(Xte, yte), 3))
# Lesson: the bigger net has a bigger train/test gap — more capacity to memorise.
```

## 4. Commit
```bash
git add .
git commit -m "day 21"
```

## Coming up — Day 22
**A full neural-network project** — build, train well (everything from today), and evaluate
honestly, end to end.
