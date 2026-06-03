"""Probability distribution helpers."""

from __future__ import annotations

import math


def factorial(value: int) -> int:
    """Return ``value!`` for non-negative integers."""

    if value < 0:
        msg = "value must be non-negative"
        raise ValueError(msg)
    return math.factorial(value)


def combinations(n: int, k: int) -> int:
    """Return the number of ways to choose k items from n."""

    return math.comb(n, k)


def binomial_pmf(trials: int, successes: int, probability: float) -> float:
    """Return a binomial probability mass value."""

    return float(
        combinations(trials, successes)
        * probability**successes
        * (1 - probability) ** (trials - successes)
    )


def expected_value(values: list[float], probabilities: list[float]) -> float:
    """Return expected value for a discrete distribution."""

    if len(values) != len(probabilities):
        msg = "values and probabilities must have the same length"
        raise ValueError(msg)
    return float(
        sum(
            value * probability
            for value, probability in zip(values, probabilities, strict=True)
        )
    )


__all__ = ["binomial_pmf", "combinations", "expected_value", "factorial"]
