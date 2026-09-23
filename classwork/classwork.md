# Day 21 — Classwork (Training a Network Well)

`pip install scikit-learn`. All data is built inside each script — no downloads.

## Exercise 1: Watch it learn (`loss_curve.py`) — ~15 min
1. Train `MLPClassifier(hidden_layer_sizes=(32,), max_iter=200)` on scaled cancer data.
2. Print `loss_curve_[0]`, `[10]`, `[-1]`. Plot the whole curve.

**Expected:** loss falls **0.961 → 0.314 → 0.036**; train acc 0.991, test 0.956. Fast fall, then flat.

**Stretch:** set `max_iter=20` — is the loss still high? (Stopped before settling = underfit.)

## Exercise 2: Tune the step size (`learning_rate.py`) — ~15 min
Loop `learning_rate_init` over 0.0001, 0.001, 0.01, 0.1, 1.0; print final loss + test acc.

**Expected (final loss):**
```
0.0001  0.202   0.947    # too small — hasn't arrived
0.001   0.036   0.956
0.01    0.003   0.956    # fast AND low — sweet spot
0.1     0.001   0.956
1.0     0.012   0.956    # starting to overshoot
```
A tiny rate leaves the loss stuck high; a good rate drives it near zero in the same steps.

**Stretch:** push the rate to 5.0 — does the loss curve start to jump instead of fall?

## Exercise 3: Catch overfitting (`early_stopping.py`) — ~20 min
1. Train a big net `(200, 200)` on the noisy data. Note the train vs test gap.
2. Add `early_stopping=True`. Did the gap shrink? How many steps did it run?
3. Try `alpha=1.0` instead — does that also help?

**Expected:**
```
No early stopping:  train 1.000 | test 0.771   (gap 0.229 <- overfitting!)
Early stopping:     train 0.936 | test 0.775   (gap 0.161, stopped at 40 steps)
```

---

## Key idea
Training well = **read the loss curve**, **tune the learning rate**, and **stop before the
network memorises**. Perfect on train + weak on test = memorising, not learning (Day 14 again).
The number to trust is always the *test* number.
