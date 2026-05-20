# Principal Component Analysis (PCA)

PCA is a linear dimensionality reduction technique that finds the directions of maximum variance in a dataset and projects the data onto those directions. It is one of the most widely used unsupervised methods — for visualization, compression, denoising, and as a preprocessing step before downstream models.

## The Intuition

Suppose your data lives in `ℝᵈ` but most of the variation occurs along a few directions. PCA finds a new orthogonal basis (the principal components) ordered by how much variance each captures. Keeping only the top `k` components yields a lower-dimensional representation that preserves most of the information.

## The Algorithm

Given a data matrix `X` of shape `(n, d)`:

1. **Center the data**: subtract the column-wise mean from each feature so that each column has zero mean.
2. **Compute the covariance matrix**: `C = (1 / (n − 1)) · XᵀX`.
3. **Eigendecompose**: find eigenvectors and eigenvalues of `C`. Eigenvectors are the principal components; eigenvalues are the variance captured along each.
4. **Sort and select**: order components by descending eigenvalue. Keep the top `k`.
5. **Project**: transformed data is `Z = X · Wₖ`, where `Wₖ` is a `(d × k)` matrix of the top `k` eigenvectors.

In practice, PCA is computed via the SVD of the centered data matrix, which is numerically more stable than forming the covariance matrix explicitly.

## Choosing the Number of Components

Common heuristics:

- **Explained variance threshold**: keep enough components to explain, say, 95% of variance.
- **Scree plot**: plot eigenvalues in descending order and look for an elbow.
- **Downstream task performance**: choose `k` by cross-validation if PCA precedes a supervised model.

## When to Standardize

If features are measured on different scales (e.g. age in years vs income in dollars), high-variance features dominate the principal components purely because of units. Standardize (mean 0, std 1) each feature first unless scales are inherently comparable.

## Limitations

- **Linear only**: PCA cannot capture curved structure. For nonlinear data, consider kernel PCA, t-SNE, UMAP, or autoencoders (see [Neural Networks](01_neural_networks.md)).
- **Variance ≠ information**: high-variance directions are not always the most discriminative. For supervised tasks, Linear Discriminant Analysis (LDA) directly maximizes class separability.
- **Interpretability**: principal components are linear combinations of original features and can be hard to label semantically.
- **Sensitive to outliers**: a few extreme points can warp the covariance estimate. Robust PCA variants exist.

## Connections

PCA is closely related to many other techniques: factor analysis, probabilistic PCA (a latent variable model amenable to [Bayesian Inference](08_bayesian_inference.md)), and the bottleneck layers of linear autoencoders. Understanding PCA is also helpful background for matrix factorization methods used in recommendation systems and collaborative filtering.
