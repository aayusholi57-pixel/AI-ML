# Day 21 — Quick Reference (Training a Network Well)

## Read the loss curve
```python
mlp = MLPClassifier(hidden_layer_sizes=(32,), max_iter=200, random_state=42)
mlp.fit(X_train_s, y_train)
mlp.loss_curve_          # loss after each step — plot it!
import matplotlib.pyplot as plt
plt.plot(mlp.loss_curve_); plt.xlabel("step"); plt.ylabel("loss"); plt.show()
```
| curve shape | meaning | fix |
|-------------|---------|-----|
| falling | learning | let it run |
| flat & low | done | stop / fewer iters |
| flat & high | stuck | raise learning rate / bigger net |
| jumping | rate too big | lower learning rate |

## Learning rate (step size)
```python
MLPClassifier(learning_rate_init=0.001)   # default; tune this first
# new_weight = old_weight - learning_rate * slope
```
Verified sweep (cancer, 200 steps): lr 0.0001 → loss 0.202 (too small), 0.01 → 0.003 (sweet spot).

## Overfitting = train/test gap
```python
print(mlp.score(X_train_s, y_train), mlp.score(X_test_s, y_test))
# big gap (e.g. 1.000 vs 0.771) = memorising, not learning
```

## Guards against overfitting
```python
MLPClassifier(early_stopping=True, validation_fraction=0.2)  # halt at best validation
MLPClassifier(alpha=1.0)          # L2 penalty — keeps weights small
MLPClassifier(hidden_layer_sizes=(16,))   # smaller net = less capacity
# + more data;  + dropout (in TensorFlow/PyTorch)
```
Verified: plain big net train 1.000 / test 0.771 (gap 0.229); with early_stopping
train 0.936 / test 0.775 (gap 0.161, stopped at 40 of 1000 steps).

## Always
- **Scale first** (neural nets are gradient-based, like logistic & k-means).
- **Trust the test number**, never the train number.
- **Plot the loss curve** before trusting any run.

## Key numbers (today, verified)
```
loss curve : 0.961 -> 0.314 -> 0.036   (train 0.991, test 0.956)
learn rate : 0.0001->0.202   0.01->0.003 (final loss, 200 steps)
overfit    : plain 1.000/0.771  ->  early-stop 0.936/0.775
```
