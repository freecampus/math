"""Reusable quiz models and scoring helpers."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal, SupportsFloat, SupportsIndex, TypeAlias, cast

import sympy as sp

from edumath.core.answers import (
    AnswerCheck,
    check_expression_answer,
    check_numeric_answer,
)
from edumath.core.expressions import parse_expression

QuestionAnswerType = Literal[
    "auto",
    "exact",
    "numeric",
    "symbolic",
    "multiple_choice",
    "proof",
    "code",
]
QuestionValidator = Callable[[object], AnswerCheck]
SympyResolverName = Literal[
    "simplify",
    "expand",
    "factor",
    "solve",
    "diff",
    "differentiate",
    "integrate",
    "limit",
    "evaluate",
    "substitute",
]
SympyExpression: TypeAlias = str | sp.Basic
SympyResolverCallable: TypeAlias = Callable[[SympyExpression], object]
NumericComparable: TypeAlias = str | bytes | bytearray | SupportsFloat | SupportsIndex


@dataclass(frozen=True)
class AnswerOption:
    """One selectable answer option."""

    label: str
    value: object


@dataclass(frozen=True)
class SympyResolver:
    """Resolve the expected answer to a question with SymPy."""

    operation: SympyResolverName
    variable: str | sp.Symbol | None = None
    point: object | None = None
    value: object | None = None
    order: int = 1
    lower: object | None = None
    upper: object | None = None

    def resolve(
        self,
        expression: SympyExpression,
        *,
        variable: str | sp.Symbol = "x",
    ) -> object:
        """Return the expected answer for ``expression``."""

        symbol = _symbol(self.variable if self.variable is not None else variable)
        parsed = _sympify_expression(expression, variable=symbol)

        if self.operation == "simplify":
            return cast(object, sp.simplify(parsed))

        if self.operation == "expand":
            return cast(object, sp.expand(parsed))

        if self.operation == "factor":
            return cast(object, sp.factor(parsed))

        if self.operation == "solve":
            return cast(object, sp.solve(parsed, symbol))

        if self.operation in {"diff", "differentiate"}:
            return cast(object, sp.diff(parsed, symbol, self.order))

        if self.operation == "integrate":
            if self.lower is not None or self.upper is not None:
                if self.lower is None or self.upper is None:
                    msg = "both lower and upper are required for definite integrals"
                    raise ValueError(msg)
                return cast(
                    object,
                    sp.integrate(parsed, (symbol, self.lower, self.upper)),
                )
            return cast(object, sp.integrate(parsed, symbol))

        if self.operation == "limit":
            if self.point is None:
                msg = "point is required for limits"
                raise ValueError(msg)
            return cast(object, sp.limit(parsed, symbol, self.point))

        if self.operation in {"evaluate", "substitute"}:
            if self.value is None:
                msg = "value is required for evaluation"
                raise ValueError(msg)
            return cast(object, sp.simplify(parsed.subs(symbol, self.value)))

        msg = f"unsupported SymPy resolver operation: {self.operation}"
        raise ValueError(msg)


SympyResolverSpec: TypeAlias = SympyResolver | SympyResolverName | SympyResolverCallable


@dataclass(frozen=True)
class Question:
    """A quiz question."""

    prompt: str
    expected: object | None = None
    options: tuple[AnswerOption, ...] = ()
    explanation: str = ""
    tags: tuple[str, ...] = ()
    expression: SympyExpression | None = None
    resolver: SympyResolverSpec | None = None
    answer_type: QuestionAnswerType = "auto"
    variable: str | sp.Symbol = "x"
    validator: QuestionValidator | None = None

    def resolve_expected(self) -> object | None:
        """Return the explicit or derived expected answer."""

        if self.expected is not None:
            return self.expected

        if self.expression is None or self.resolver is None:
            return None

        if isinstance(self.resolver, SympyResolver):
            return self.resolver.resolve(self.expression, variable=self.variable)

        if isinstance(self.resolver, str):
            return SympyResolver(self.resolver).resolve(
                self.expression,
                variable=self.variable,
            )

        return self.resolver(self.expression)

    def check(self, received: object) -> AnswerCheck:
        """Check a learner answer."""

        if self.validator is not None:
            return self.validator(received)

        expected = self.resolve_expected()
        if expected is None:
            return AnswerCheck(
                correct=False,
                received=received,
                expected=None,
                message="This question does not define an automatic checker.",
            )

        answer_type = self._effective_answer_type(expected)
        if answer_type == "symbolic":
            return self._check_symbolic(received, expected)

        if answer_type == "numeric":
            return self._check_numeric(received, expected)

        if answer_type in {"proof", "code"}:
            return AnswerCheck(
                correct=False,
                received=received,
                expected=expected,
                message=f"{answer_type} answers require a custom validator.",
            )

        received_value = _answer_value(received)
        correct = received_value == expected
        message = "Correct." if correct else f"Expected {_format_answer(expected)}."
        return AnswerCheck(
            correct=correct,
            received=received,
            expected=expected,
            message=message,
        )

    def _effective_answer_type(self, expected: object) -> QuestionAnswerType:
        if self.answer_type != "auto":
            return self.answer_type

        if self.options:
            return "multiple_choice"

        if isinstance(expected, sp.Expr):
            return "symbolic"

        if _is_number(expected):
            return "numeric"

        return "exact"

    def _check_symbolic(self, received: object, expected: object) -> AnswerCheck:
        received_value = _answer_value(received)
        try:
            return check_expression_answer(
                cast(str | sp.Expr, received_value),
                cast(str | sp.Expr, expected),
                variable=_symbol(self.variable).name,
            )
        except (TypeError, ValueError, sp.SympifyError) as error:
            return AnswerCheck(
                correct=False,
                received=received,
                expected=expected,
                message=f"Could not compare symbolic answer: {error}",
            )

    def _check_numeric(self, received: object, expected: object) -> AnswerCheck:
        received_value = _answer_value(received)
        try:
            return check_numeric_answer(_to_float(received_value), _to_float(expected))
        except (TypeError, ValueError) as error:
            return AnswerCheck(
                correct=False,
                received=received,
                expected=expected,
                message=f"Could not compare numeric answer: {error}",
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


def _answer_value(received: object) -> object:
    if isinstance(received, AnswerOption):
        return received.value
    return received


def _format_answer(answer: object) -> str:
    if isinstance(answer, sp.Basic):
        return cast(str, sp.sstr(answer))
    return str(answer)


def _is_number(value: object) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _symbol(variable: str | sp.Symbol) -> sp.Symbol:
    if isinstance(variable, str):
        return sp.Symbol(variable)
    return variable


def _sympify_expression(
    expression: SympyExpression,
    *,
    variable: str | sp.Symbol = "x",
) -> sp.Basic:
    if isinstance(expression, sp.Basic):
        return expression

    return parse_expression(expression, variables=(_symbol(variable),))


def _to_float(value: object) -> float:
    return float(cast(NumericComparable, value))
