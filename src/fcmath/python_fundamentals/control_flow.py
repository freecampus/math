"""Control-flow examples for beginner Python lessons."""

from __future__ import annotations


def classify_number(value: float) -> str:
    """Classify a number as negative, zero, or positive."""

    if value < 0:
        return "negative"
    if value > 0:
        return "positive"
    return "zero"


def cumulative_sum(values: list[float]) -> list[float]:
    """Return running totals for a list of numbers."""

    totals: list[float] = []
    current = 0.0
    for value in values:
        current += value
        totals.append(current)
    return totals
