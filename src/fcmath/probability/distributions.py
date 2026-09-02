"""Probability distribution helpers."""

from __future__ import annotations

import math
from collections.abc import Sequence


def factorial(value: int) -> int:
    """Return ``value!`` for non-negative integers."""

    if value < 0:
        msg = "value must be non-negative"
        raise ValueError(msg)
    return math.factorial(value)


def combinations(n: int, k: int) -> int:
    """Return the number of ways to choose ``k`` items from ``n``."""

    _validate_count_parameters(n, k)
    return math.comb(n, k)


def permutations(n: int, k: int) -> int:
    """Return the number of ordered ways to choose ``k`` items from ``n``."""

    _validate_count_parameters(n, k)
    return math.perm(n, k)


def bernoulli_pmf(value: int, probability: float) -> float:
    """Return a Bernoulli probability for value ``0`` or ``1``."""

    _validate_probability(probability)
    if value not in (0, 1):
        return 0.0
    return float(probability if value == 1 else 1 - probability)


def binomial_pmf(trials: int, successes: int, probability: float) -> float:
    """Return a binomial probability mass value."""

    _validate_count_parameters(trials, successes)
    _validate_probability(probability)
    return float(
        combinations(trials, successes)
        * probability**successes
        * (1 - probability) ** (trials - successes)
    )


def binomial_mean(trials: int, probability: float) -> float:
    """Return the mean of a binomial distribution."""

    _validate_trials_probability(trials, probability)
    return float(trials * probability)


def binomial_variance(trials: int, probability: float) -> float:
    """Return the variance of a binomial distribution."""

    _validate_trials_probability(trials, probability)
    return float(trials * probability * (1 - probability))


def expected_value(values: Sequence[float], probabilities: Sequence[float]) -> float:
    """Return expected value for a discrete distribution."""

    _validate_distribution(values, probabilities)
    return float(
        sum(
            value * probability
            for value, probability in zip(values, probabilities, strict=True)
        )
    )


def variance(values: Sequence[float], probabilities: Sequence[float]) -> float:
    """Return variance for a discrete distribution."""

    mean = expected_value(values, probabilities)
    return float(
        sum(
            probability * (value - mean) ** 2
            for value, probability in zip(values, probabilities, strict=True)
        )
    )


def standard_deviation(
    values: Sequence[float], probabilities: Sequence[float]
) -> float:
    """Return standard deviation for a discrete distribution."""

    return math.sqrt(variance(values, probabilities))


def _validate_count_parameters(n: int, k: int) -> None:
    if n < 0 or k < 0:
        msg = "n and k must be non-negative"
        raise ValueError(msg)
    if k > n:
        msg = "k must be no greater than n"
        raise ValueError(msg)


def _validate_probability(probability: float) -> None:
    if not 0 <= probability <= 1:
        msg = "probability must be between 0 and 1"
        raise ValueError(msg)


def _validate_trials_probability(trials: int, probability: float) -> None:
    if trials < 0:
        msg = "trials must be non-negative"
        raise ValueError(msg)
    _validate_probability(probability)


def _validate_distribution(
    values: Sequence[float], probabilities: Sequence[float]
) -> None:
    if len(values) != len(probabilities):
        msg = "values and probabilities must have the same length"
        raise ValueError(msg)
    if not values:
        msg = "distribution must contain at least one value"
        raise ValueError(msg)
    if any(probability < 0 for probability in probabilities):
        msg = "probabilities must be non-negative"
        raise ValueError(msg)
    if not math.isclose(sum(probabilities), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        msg = "probabilities must sum to 1"
        raise ValueError(msg)


__all__ = [
    "bernoulli_pmf",
    "binomial_mean",
    "binomial_pmf",
    "binomial_variance",
    "combinations",
    "expected_value",
    "factorial",
    "permutations",
    "standard_deviation",
    "variance",
]
