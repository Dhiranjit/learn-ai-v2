# Gradient Descent and Optimizers

Gradient descent is the workhorse optimization algorithm for training neural networks. It iteratively updates parameters in the direction that most reduces the loss, using the gradient computed by [Backpropagation](02_backpropagation.md).

## The Basic Update Rule

Given parameters `θ`, loss `L`, and learning rate `η`:

```
θ ← θ − η · ∇L(θ)
```

The learning rate controls step size. Too large and the optimization diverges; too small and convergence is slow or stalls in flat regions.

## Variants by Batch Size

- **Batch gradient descent**: computes the gradient over the entire training set per step. Stable but slow and memory-hungry.
- **Stochastic gradient descent (SGD)**: uses one example per step. Noisy but cheap; the noise can help escape sharp minima.
- **Mini-batch SGD**: the practical default — uses a small batch (e.g. 32–512 examples). Balances stability and throughput, exploits GPU parallelism.

## Momentum

Plain SGD oscillates in narrow ravines of the loss surface. Momentum accumulates a velocity vector that smooths updates:

```
v ← β·v + ∇L(θ)
θ ← θ − η·v
```

Typical `β = 0.9`. Momentum accelerates progress along consistent gradient directions and dampens oscillation across them.

## Adaptive Optimizers

These adapt the effective learning rate per parameter, based on the history of gradients:

- **AdaGrad**: accumulates squared gradients; learning rate shrinks over time. Useful for sparse features but can stall.
- **RMSProp**: exponentially weighted average of squared gradients; avoids AdaGrad's monotonic decay.
- **Adam**: combines momentum (first moment) with RMSProp (second moment). The de facto default for deep learning. Hyperparameters `β1=0.9`, `β2=0.999`, `ε=1e-8`.
- **AdamW**: Adam with decoupled weight decay. Now preferred over plain Adam for transformer training.

## Learning Rate Schedules

A fixed learning rate is rarely optimal. Common schedules:

- **Step decay**: drop LR by a factor every N epochs.
- **Cosine annealing**: smoothly decay LR following a cosine curve, often with warm restarts.
- **Warmup + decay**: linearly increase LR for the first few thousand steps, then decay. Standard for transformer pretraining.

The interaction between optimizer, batch size, and learning rate schedule is one of the most important practical tuning knobs in deep learning.
