# Bayesian Inference

Bayesian inference is a framework for updating beliefs in light of evidence. Instead of treating parameters as fixed unknowns (as in frequentist statistics), it treats them as random variables with their own probability distributions.

## Bayes' Theorem

Given data `D` and a parameter `θ`:

```
P(θ | D) = P(D | θ) · P(θ) / P(D)
```

Each piece has a name:

- **Prior, `P(θ)`**: what we believed about `θ` before seeing the data.
- **Likelihood, `P(D | θ)`**: how probable the data is under a given `θ`.
- **Posterior, `P(θ | D)`**: our updated belief after seeing the data.
- **Evidence, `P(D)`**: the marginal likelihood, a normalizing constant.

The whole framework is just: posterior ∝ likelihood × prior.

## Why It Matters

Bayesian inference gives you a full distribution over parameters, not a point estimate. This is naturally informative about uncertainty — useful in:

- Small-data regimes where point estimates are unreliable.
- Decision-making under uncertainty where you need to weight outcomes by their probability.
- Sequential learning, where the posterior after one batch of data becomes the prior for the next.

It also contrasts with [Hypothesis Testing](07_hypothesis_testing.md): a Bayesian asks "what is the probability the hypothesis is true given the data?" rather than "how surprising is the data under the null?".

## Priors

The choice of prior is both the strength and the controversy of Bayesian methods.

- **Informative priors** encode genuine prior knowledge (e.g. "this drug effect is probably small").
- **Weakly informative priors** rule out absurd values without committing to a strong belief.
- **Non-informative / flat priors** try to "let the data speak", though they are often improper and basis-dependent.
- **Conjugate priors** are mathematically convenient: the posterior has the same family as the prior. Examples: Beta is conjugate to Bernoulli; Gamma is conjugate to Poisson. See [Probability Distributions](06_probability_distributions.md).

## Computing the Posterior

Closed-form posteriors are rare outside conjugate cases. In practice:

- **Markov Chain Monte Carlo (MCMC)**: sample from the posterior. Algorithms: Metropolis-Hastings, Gibbs sampling, Hamiltonian Monte Carlo (HMC), NUTS.
- **Variational inference**: approximate the posterior with a simpler distribution by optimization. Faster, scalable, but biased.
- **Laplace approximation**: a Gaussian centered at the posterior mode.

## Bayesian Machine Learning

Bayesian ideas appear throughout ML: Gaussian processes, Bayesian neural networks, latent Dirichlet allocation, and the variational lens on VAEs. The Bayesian perspective also justifies regularization — L2 regularization (see [Overfitting and Regularization](05_overfitting_regularization.md)) corresponds to a Gaussian prior on weights, and L1 corresponds to a Laplace prior.
