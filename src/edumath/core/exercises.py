"""Reusable exercise models."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from edumath.core.answers import AnswerCheck

AnswerValidator = Callable[[object], AnswerCheck]


@dataclass(frozen=True)
class Exercise:
    """A practice prompt with an optional validator."""

    prompt: str
    expected: object | None = None
    validator: AnswerValidator | None = None
    hint: str = ""
    explanation: str = ""
    tags: tuple[str, ...] = ()

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
