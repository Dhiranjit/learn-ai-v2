# Hypothesis Testing

Hypothesis testing is a framework for deciding whether observed data provides enough evidence to reject a default assumption about the world. It is one of the foundational tools of frequentist statistics.

## The Setup

Two competing hypotheses are stated:

- **Null hypothesis (H₀)**: the default — typically "no effect", "no difference", or "the parameter equals some specific value".
- **Alternative hypothesis (H₁)**: what we suspect might be true instead.

We then collect data and ask: assuming H₀ is true, how surprising is what we observed?

## Test Statistics and p-values

A **test statistic** is a function of the data designed to be sensitive to deviations from H₀ (e.g. a t-statistic, z-statistic, chi-squared). Its sampling distribution under H₀ is known.

The **p-value** is the probability, assuming H₀ is true, of observing a test statistic at least as extreme as the one we got. A small p-value means the data would be surprising under H₀, suggesting H₀ should be rejected.

A **significance level α** (commonly 0.05) is chosen *before* looking at the data. If `p < α`, we reject H₀.

## Two Kinds of Error

- **Type I error (false positive)**: rejecting H₀ when it is actually true. Controlled by α.
- **Type II error (false negative)**: failing to reject H₀ when H₁ is true. The probability of avoiding this is the **power** of the test (1 − β).

There is an inherent tradeoff: lowering α (fewer false positives) raises β (more false negatives) for fixed sample size. Larger samples reduce both.

## Common Tests

- **t-test**: compares means; one-sample, two-sample, or paired variants. Assumes approximately normal data (or large enough sample for the CLT).
- **z-test**: like the t-test but for known population variance or very large samples.
- **Chi-squared test**: tests independence of categorical variables, or goodness-of-fit to a discrete distribution.
- **ANOVA**: compares means across more than two groups.
- **Mann-Whitney U / Wilcoxon**: non-parametric alternatives that don't assume normality.

## Pitfalls

- **p-hacking**: running many tests until one is significant by chance. With α = 0.05, one in twenty tests will be "significant" under pure noise.
- **Multiple comparisons**: when running many tests, adjust with Bonferroni, Benjamini-Hochberg, or similar.
- **Confusing statistical and practical significance**: a tiny effect can be highly significant with enough data, yet meaningless in practice. Always report effect sizes and confidence intervals alongside p-values.
- **p-values are not posterior probabilities**: they describe the data given the hypothesis, not the hypothesis given the data. For that, see [Bayesian Inference](08_bayesian_inference.md).
