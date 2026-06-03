"""NumPy array helpers for beginner quantitative Python."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class ArraySummary:
    """Summary statistics for a numeric array."""

    shape: tuple[int, ...]
    mean: float
    minimum: float
    maximum: float
    total: float


def array_summary(values: npt.ArrayLike) -> ArraySummary:
    """Return basic summary statistics for numeric values."""

    array = np.asarray(values, dtype=float)
    return ArraySummary(
        shape=array.shape,
        mean=float(np.mean(array)),
        minimum=float(np.min(array)),
        maximum=float(np.max(array)),
        total=float(np.sum(array)),
    )
