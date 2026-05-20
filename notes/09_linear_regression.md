# Linear Regression

Linear regression models the relationship between one or more input features and a continuous target by fitting a linear function. Despite its simplicity, it remains a workhorse of statistics and ML — both as a baseline and as a building block in more complex methods.

## The Model

For input features `x ∈ ℝᵈ` and target `y ∈ ℝ`:

```
y = w · x + b + ε
```

where `w` is a weight vector, `b` is the intercept, and `ε` is a noise term, typically assumed Gaussian with zero mean. The model has `d + 1` parameters.

## Fitting: Ordinary Least Squares

The standard objective is to minimize the sum of squared residuals:

```
L(w, b) = Σᵢ (yᵢ − (w · xᵢ + b))²
```

This has a closed-form solution. Stacking inputs into a matrix `X` (with a column of ones for the intercept) and targets into a vector `y`:

```
ŵ = (Xᵀ X)⁻¹ Xᵀ y
```

This is the normal equation. In practice we use QR or SVD decompositions for numerical stability rather than literally inverting `XᵀX`.

## Assumptions

OLS estimates are unbiased and minimum-variance among linear estimators (Gauss-Markov theorem) when:

- The relationship is truly linear in parameters.
- Errors are independent.
- Errors have constant variance (homoscedasticity).
- Errors are uncorrelated with the inputs.
- For inference (confidence intervals, p-values): errors are normally distributed.

When assumptions fail, estimates may still be useful but standard errors and tests become unreliable.

## Regularized Variants

- **Ridge regression (L2)**: adds `λ‖w‖²` to the loss. Shrinks weights, helps when features are correlated. Has a closed form: `ŵ = (XᵀX + λI)⁻¹ Xᵀy`.
- **Lasso (L1)**: adds `λ‖w‖₁`. Produces sparse solutions — many weights become exactly zero, effectively selecting features. No closed form; solved iteratively.
- **Elastic net**: a mix of L1 and L2.

These connect directly to the regularization techniques used in [Neural Networks](01_neural_networks.md) and [Overfitting and Regularization](05_overfitting_regularization.md).

## Diagnostics

After fitting, examine:

- **R²**: fraction of variance explained.
- **Residual plots**: should look like random noise. Patterns suggest model misspecification.
- **Q-Q plots**: check normality of residuals.
- **VIF (Variance Inflation Factor)**: detect multicollinearity among features.

## Beyond Linear

Linear regression generalizes naturally: polynomial features, splines, and basis expansions allow it to capture nonlinearities while staying linear in parameters. Generalized linear models (GLMs) extend it to non-Gaussian targets via link functions — logistic regression for binary outcomes, Poisson regression for counts.
