"""Reusable exercise models."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from edumath.core.answers import AnswerCheck
from edumath.core.solutions import WorkedSolution, render_solution_details

AnswerValidator = Callable[[object], AnswerCheck]
AnswerType = Literal["exact", "numeric", "symbolic", "multiple_choice", "proof", "code"]
Difficulty = Literal["check", "guided", "challenge"]


@dataclass(frozen=True)
class Exercise:
    """A practice prompt with an optional validator."""

    prompt: str
    expected: object | None = None
    validator: AnswerValidator | None = None
    hint: str = ""
    explanation: str = ""
    tags: tuple[str, ...] = ()
    exercise_id: str = ""
    difficulty: Difficulty = "check"
    answer_type: AnswerType = "exact"
    prerequisites: tuple[str, ...] = ()
    solution: WorkedSolution | None = None

    def check(self, received: object) -> AnswerCheck:
        """Check a learner answer."""

        if self.validator is not None:
            return self.validator(received)

        correct = received == self.expected
        message = "Correct." if correct else f"Expected {self.expected}."
        return AnswerCheck(
            correct=correct,
            received=received,
            expected=self.expected,
            message=message,
        )


def render_exercise_markdown(exercise: Exercise, *, index: int | None = None) -> str:
    """Render one exercise and its optional revealable solution as Markdown."""

    prefix = f"{index}. " if index is not None else ""
    parts = [f"{prefix}{exercise.prompt}"]
    if exercise.solution is not None:
        parts.append(render_solution_details(exercise.solution))
    return "\n\n".join(parts)


def render_practice_set(exercises: Sequence[Exercise]) -> str:
    """Render a practice set with per-exercise solution reveals."""

    rendered = [
        render_exercise_markdown(exercise, index=index)
        for index, exercise in enumerate(exercises, start=1)
    ]
    return "::: {.practice-box}\n" + "\n\n".join(rendered) + "\n:::\n"
