"""Validators for discrete mathematics answers."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import SupportsFloat, cast

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer

TERM_TOLERANCE = NumericTolerance(absolute=1e-9, relative=1e-9)


def validate_truth_value(received: object, expected: bool) -> AnswerCheck:
    """Validate a Boolean answer."""

    try:
        value = _parse_bool(received)
    except ValueError as error:
        return AnswerCheck(False, received, expected, str(error))
    correct = value is expected
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


def validate_set_answer(received: object, expected: Iterable[object]) -> AnswerCheck:
    """Validate a finite set answer from common student formats."""

    try:
        received_set = _normalize_set(received)
        expected_set = set(expected)
    except ValueError as error:
        return AnswerCheck(False, received, set(expected), str(error))
    correct = received_set == expected_set
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected_set,
        message="Correct." if correct else f"Expected {expected_set}.",
    )


def validate_ordered_pairs(
    received: Iterable[Sequence[object]],
    expected: Iterable[Sequence[object]],
) -> AnswerCheck:
    """Validate a finite set of ordered pairs."""

    received_pairs = {_as_pair(pair) for pair in received}
    expected_pairs = {_as_pair(pair) for pair in expected}
    correct = received_pairs == expected_pairs
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected_pairs,
        message="Correct." if correct else f"Expected {expected_pairs}.",
    )


def validate_sequence_terms(
    received: Sequence[object],
    expected: Sequence[object],
    *,
    tolerance: NumericTolerance = TERM_TOLERANCE,
) -> AnswerCheck:
    """Validate numeric sequence terms."""

    if len(received) != len(expected):
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Expected {len(expected)} terms, received {len(received)}.",
        )
    for index, (received_value, expected_value) in enumerate(
        zip(received, expected, strict=True),
        start=1,
    ):
        check = check_numeric_answer(
            float(cast(SupportsFloat, received_value)),
            float(cast(SupportsFloat, expected_value)),
            tolerance=tolerance,
        )
        if not check.correct:
            return AnswerCheck(
                correct=False,
                received=received,
                expected=expected,
                message=f"Term {index}: {check.message}",
            )
    return AnswerCheck(True, received, expected, "Correct.")


def validate_relation_properties(
    received: Iterable[object],
    expected: Iterable[str],
) -> AnswerCheck:
    """Validate selected relation-property labels."""

    received_set = {str(value).strip().lower() for value in received}
    expected_set = {value.strip().lower() for value in expected}
    correct = received_set == expected_set
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected_set,
        message="Correct." if correct else f"Expected {expected_set}.",
    )


def validate_graph_degree_sequence(
    received: Sequence[object],
    expected: Sequence[int],
) -> AnswerCheck:
    """Validate a graph degree sequence."""

    try:
        received_values = tuple(int(str(value)) for value in received)
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not read degree sequence: {error}",
        )
    expected_values = tuple(expected)
    correct = received_values == expected_values
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected_values,
        message="Correct." if correct else f"Expected {expected_values}.",
    )


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "t", "1", "yes", "y"}:
        return True
    if normalized in {"false", "f", "0", "no", "n"}:
        return False
    msg = "Use a truth value such as true or false."
    raise ValueError(msg)


def _normalize_set(value: object) -> set[object]:
    if isinstance(value, (set, frozenset, list, tuple)):
        return set(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped in {"", "{}", "∅"}:
            return set()
        stripped = stripped.removeprefix("{").removesuffix("}")
        return {
            _parse_atom(part.strip()) for part in stripped.split(",") if part.strip()
        }
    msg = "Enter a set, list, tuple, or comma-separated string."
    raise ValueError(msg)


def _parse_atom(text: str) -> object:
    try:
        return int(text)
    except ValueError:
        return text.strip("'\"")


def _as_pair(value: Sequence[object]) -> tuple[object, object]:
    if len(value) != 2:
        msg = "ordered pairs must have exactly two entries"
        raise ValueError(msg)
    return (value[0], value[1])


__all__ = [
    "TERM_TOLERANCE",
    "validate_graph_degree_sequence",
    "validate_ordered_pairs",
    "validate_relation_properties",
    "validate_sequence_terms",
    "validate_set_answer",
    "validate_truth_value",
]
