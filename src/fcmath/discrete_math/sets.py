"""Set helpers for discrete mathematics lessons."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from itertools import chain, combinations, product
from typing import TypeVar

T = TypeVar("T", bound=Hashable)
U = TypeVar("U", bound=Hashable)
SetOperationTable = dict[str, set[T]]
VennRegionCounts = dict[str, int]


def set_operation_table(a: Iterable[T], b: Iterable[T]) -> SetOperationTable[T]:
    """Return common operations for two finite sets."""

    left = set(a)
    right = set(b)
    return {
        "union": left | right,
        "intersection": left & right,
        "a_minus_b": left - right,
        "b_minus_a": right - left,
        "symmetric_difference": left ^ right,
    }


def power_set(values: Iterable[T]) -> tuple[frozenset[T], ...]:
    """Return the power set of a small finite iterable."""

    items = tuple(dict.fromkeys(values))
    subsets = chain.from_iterable(
        combinations(items, size) for size in range(len(items) + 1)
    )
    return tuple(frozenset(subset) for subset in subsets)


def cartesian_product(a: Iterable[T], b: Iterable[U]) -> tuple[tuple[T, U], ...]:
    """Return ordered pairs in ``A x B``."""

    return tuple(product(tuple(a), tuple(b)))


def venn_region_counts(
    a: Iterable[T],
    b: Iterable[T],
    *,
    universe: Iterable[T] | None = None,
) -> VennRegionCounts:
    """Return counts for a two-set Venn diagram."""

    left = set(a)
    right = set(b)
    both = left & right
    only_a = left - right
    only_b = right - left
    if universe is None:
        neither_count = 0
    else:
        neither_count = len(set(universe) - (left | right))
    return {
        "only_a": len(only_a),
        "only_b": len(only_b),
        "both": len(both),
        "neither": neither_count,
    }


__all__ = [
    "SetOperationTable",
    "VennRegionCounts",
    "cartesian_product",
    "power_set",
    "set_operation_table",
    "venn_region_counts",
]
