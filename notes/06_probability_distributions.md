# Probability Distributions

A probability distribution describes how likely each possible outcome of a random variable is. Distributions are the language of uncertainty and underpin most of statistics and machine learning.

## Discrete vs Continuous

- **Discrete distributions** assign probabilities to countable outcomes via a probability mass function (PMF). Example: a die roll.
- **Continuous distributions** assign probability density over a continuous range via a probability density function (PDF). The probability of any single exact value is zero; probability is measured over intervals via integration.

In both cases, total probability sums (or integrates) to 1.

## Common Discrete Distributions

- **Bernoulli(p)**: a single binary trial with success probability `p`. Mean `p`, variance `p(1-p)`.
- **Binomial(n, p)**: the number of successes in `n` independent Bernoulli trials.
- **Poisson(λ)**: the number of events occurring in a fixed interval at average rate `λ`. Useful for rare-event counts.
- **Categorical**: a generalization of Bernoulli to `K` outcomes. The output distribution of softmax-classified neural networks.

## Common Continuous Distributions

- **Uniform(a, b)**: constant density over `[a, b]`. The maximum-entropy distribution given only support bounds.
- **Normal/Gaussian(μ, σ²)**: the bell curve. Justified by the Central Limit Theorem: sums of many independent variables tend toward normal regardless of their original distribution.
- **Exponential(λ)**: time between events in a Poisson process. Memoryless.
- **Beta(α, β)**: distribution over probabilities in `[0,1]`. Conjugate prior for the Bernoulli/binomial likelihood — see [Bayesian Inference](08_bayesian_inference.md).
- **Gamma(α, β)**: generalizes the exponential; models positive continuous quantities like waiting times.

## Moments and Summary Statistics

- **Mean (expectation)**: the average outcome, `E[X]`.
- **Variance**: `E[(X - μ)²]`, a measure of spread.
- **Skewness**: asymmetry of the distribution.
- **Kurtosis**: heaviness of the tails relative to a normal.

## Why This Matters for ML

- Cross-entropy loss is the KL divergence between the predicted categorical distribution and the empirical label distribution.
- Variational inference, diffusion models, and normalizing flows all build on tractable continuous distributions.
- Generative models try to learn or approximate the data distribution `p(x)` itself.

Understanding distributions is also essential for [Hypothesis Testing](07_hypothesis_testing.md) and [Bayesian Inference](08_bayesian_inference.md).
