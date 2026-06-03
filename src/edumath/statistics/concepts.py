"""Statistics helpers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class DescriptiveStats:
    """Basic descriptive statistics."""

    mean: float
    median: float
    variance: float
    standard_deviation: float
    minimum: float
    maximum: float


def describe(values: npt.ArrayLike, *, sample: bool = True) -> DescriptiveStats:
    """Return descriptive statistics for numeric data."""

    array = np.asarray(values, dtype=float)
    ddof = 1 if sample and array.size > 1 else 0
    return DescriptiveStats(
        mean=float(np.mean(array)),
        median=float(np.median(array)),
        variance=float(np.var(array, ddof=ddof)),
        standard_deviation=float(np.std(array, ddof=ddof)),
        minimum=float(np.min(array)),
        maximum=float(np.max(array)),
    )


def z_score(value: float, mean: float, standard_deviation: float) -> float:
    """Return a z-score."""

    return (value - mean) / standard_deviation


__all__ = ["DescriptiveStats", "describe", "z_score"]
