"""Basic Python value helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueInfo:
    """A small summary of a Python value."""

    value: object
    type_name: str
    representation: str


def describe_value(value: object) -> ValueInfo:
    """Return a beginner-friendly summary of a Python value."""

    return ValueInfo(
        value=value,
        type_name=type(value).__name__,
        representation=repr(value),
    )
