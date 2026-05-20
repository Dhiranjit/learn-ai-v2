# Overfitting and Regularization

A model **overfits** when it learns patterns specific to the training set that do not generalize to new data. The classic signature: training loss continues to decrease while validation loss stagnates or rises. Regularization is the umbrella of techniques used to combat this.

## The Bias-Variance Tradeoff

- **High bias** (underfitting): the model is too simple to capture the underlying signal. Both training and validation error are high.
- **High variance** (overfitting): the model captures noise in the training data. Training error is low, validation error is much higher.

The goal of regularization is to reduce variance without paying too much in bias.

## Weight-Based Regularization

- **L2 regularization (weight decay)**: adds `λ · Σ wᵢ²` to the loss. Pushes weights toward zero, discouraging any single weight from dominating. The standard default in deep learning.
- **L1 regularization**: adds `λ · Σ |wᵢ|`. Encourages sparsity — many weights become exactly zero. Useful for feature selection.
- **Elastic net**: a combination of L1 and L2.

## Architectural Regularization

- **Dropout**: during training, randomly zero out a fraction `p` of activations in each layer. Forces the network to learn redundant representations and prevents co-adaptation of neurons. At inference, all units are active and activations are scaled.
- **Batch normalization**: normalizes activations within each mini-batch. Originally proposed for optimization, it also has a regularizing effect through the noise of batch statistics.
- **Layer normalization**: normalizes across features for each example. Standard in transformers, where batch statistics are less reliable.

## Data-Based Regularization

- **Data augmentation**: synthetically expand the training set with transformations the model should be invariant to (image crops, flips, color jitter; for text, paraphrasing or back-translation).
- **Early stopping**: monitor validation loss and stop training when it begins to rise. Effectively a form of implicit regularization on optimization trajectory length.
- **Label smoothing**: replace hard one-hot targets with soft distributions (e.g. 0.9 for the true class, 0.1/(K-1) for others). Prevents overconfident predictions.

## Detecting Overfitting

Standard practice is to split data into train, validation, and test sets. Use validation loss to tune hyperparameters and detect overfitting; the test set is touched only once, at the end, for an unbiased estimate of generalization. See also [Hypothesis Testing](07_hypothesis_testing.md) for the statistical view of generalization claims.
