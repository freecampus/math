"""Finite relation helpers."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import TypeVar

T = TypeVar("T", bound=Hashable)
U = TypeVar("U", bound=Hashable)
V = TypeVar("V", bound=Hashable)
Pair = tuple[Hashable, Hashable]


def domain(pairs: Iterable[tuple[T, U]]) -> set[T]:
    """Return first coordinates in a finite relation."""

    return {left for left, _ in pairs}


def range_(pairs: Iterable[tuple[T, U]]) -> set[U]:
    """Return second coordinates in a finite relation."""

    return {right for _, right in pairs}


def is_function(pairs: Iterable[tuple[T, U]]) -> bool:
    """Return whether each input has at most one output."""

    outputs: dict[T, U] = {}
    for left, right in pairs:
        if left in outputs and outputs[left] != right:
            return False
        outputs[left] = right
    return True


def is_reflexive(pairs: Iterable[tuple[T, T]], universe: Iterable[T]) -> bool:
    """Return whether every element relates to itself."""

    relation = set(pairs)
    return all((value, value) in relation for value in universe)


def is_symmetric(pairs: Iterable[tuple[T, T]]) -> bool:
    """Return whether every pair has its reverse pair."""

    relation = set(pairs)
    return all((right, left) in relation for left, right in relation)


def is_antisymmetric(pairs: Iterable[tuple[T, T]]) -> bool:
    """Return whether two-way relationships only occur for equal elements."""

    relation = set(pairs)
    return all(
        left == right or (right, left) not in relation for left, right in relation
    )


def is_transitive(pairs: Iterable[tuple[T, T]]) -> bool:
    """Return whether ``aRb`` and ``bRc`` always imply ``aRc``."""

    relation = set(pairs)
    for left, middle in relation:
        for second_middle, right in relation:
            if middle == second_middle and (left, right) not in relation:
                return False
    return True


def compose_relations(
    first: Iterable[tuple[T, U]],
    second: Iterable[tuple[U, V]],
) -> set[tuple[T, V]]:
    """Return composition ``second after first`` for finite relations."""

    first_set = set(first)
    second_set = set(second)
    return {
        (left, right)
        for left, middle in first_set
        for second_middle, right in second_set
        if middle == second_middle
    }


__all__ = [
    "Pair",
    "compose_relations",
    "domain",
    "is_antisymmetric",
    "is_function",
    "is_reflexive",
    "is_symmetric",
    "is_transitive",
    "range_",
]
