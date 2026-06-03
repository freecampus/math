"""Reusable quiz models and scoring helpers."""

from __future__ import annotations

from dataclasses import dataclass, field

from edumath.core.answers import AnswerCheck


@dataclass(frozen=True)
class AnswerOption:
    """One selectable answer option."""

    label: str
    value: object


@dataclass(frozen=True)
class Question:
    """A quiz question."""

    prompt: str
    expected: object
    options: tuple[AnswerOption, ...] = ()
    explanation: str = ""
    tags: tuple[str, ...] = ()

    def check(self, received: object) -> AnswerCheck:
        """Check a learner answer by exact value equality."""

        correct = received == self.expected
        message = "Correct." if correct else f"Expected {self.expected}."
        return AnswerCheck(
            correct=correct,
            received=received,
            expected=self.expected,
            message=message,
        )


@dataclass(frozen=True)
class QuizResult:
    """The result of one answered quiz question."""

    question: Question
    received: object
    check: AnswerCheck


@dataclass
class QuizSession:
    """Stateful quiz session for notebooks and applications."""

    questions: tuple[Question, ...]
    results: list[QuizResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        """Number of correct answers."""

        return sum(1 for result in self.results if result.check.correct)

    @property
    def total(self) -> int:
        """Total number of questions."""

        return len(self.questions)

    @property
    def complete(self) -> bool:
        """Whether all questions have been answered."""

        return len(self.results) >= self.total

    def answer(self, question_index: int, received: object) -> QuizResult:
        """Answer one question and store the result."""

        question = self.questions[question_index]
        result = QuizResult(
            question=question,
            received=received,
            check=question.check(received),
        )
        self.results.append(result)
        return result

    def reset(self) -> None:
        """Clear quiz results."""

        self.results.clear()
