"""Small, renderer-independent helpers for learning mathematical proof."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ProofStep:
    """One mathematical statement and the reason that licenses it."""

    statement: str
    justification: str

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("proof step statement must not be empty")
        if not self.justification.strip():
            raise ValueError("proof step justification must not be empty")


def proof_steps_markdown(steps: Sequence[ProofStep]) -> str:
    """Render proof steps as an accessible Markdown audit table."""

    if not steps:
        raise ValueError("at least one proof step is required")
    rows = [
        "| Step | Statement | Justification |",
        "|---:|---|---|",
    ]
    rows.extend(
        f"| {index} | {_escape_cell(step.statement)} | "
        f"{_escape_cell(step.justification)} |"
        for index, step in enumerate(steps, start=1)
    )
    return "\n".join(rows)


def find_implication_counterexample(
    candidates: Iterable[T],
    hypothesis: Callable[[T], bool],
    conclusion: Callable[[T], bool],
) -> T | None:
    """Return the first candidate making an implication false, if one exists.

    A counterexample to ``hypothesis(value) -> conclusion(value)`` must make
    the hypothesis true and the conclusion false. Candidate order is
    preserved so lessons can search a small, explainable domain before using a
    larger computational experiment.
    """

    for value in candidates:
        if hypothesis(value) and not conclusion(value):
            return value
    return None


def _escape_cell(value: str) -> str:
    return value.strip().replace("|", "\\|").replace("\n", "<br>")


__all__ = [
    "ProofStep",
    "find_implication_counterexample",
    "proof_steps_markdown",
]
