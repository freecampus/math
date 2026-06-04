"""Algebra quiz helpers and the correctly spelled import surface."""

from edumath.algebra.quizes import *  # noqa: F403
from edumath.algebra.quizes import __all__ as _legacy_quiz_exports
from edumath.core import Question, SympyResolver, SympyResolverName


def symbolic_question(
    prompt: str,
    expression: object,
    *,
    resolver: SympyResolverName | SympyResolver,
    variable: str = "x",
) -> Question:
    """Create a symbolic auto-checkable question backed by a SymPy resolver."""

    return Question(
        prompt=prompt,
        expression=expression,
        resolver=resolver,
        variable=variable,
        answer_type="symbolic",
    )


def expand_question(
    expression: object,
    *,
    prompt: str | None = None,
    variable: str = "x",
) -> Question:
    """Create a question that asks learners to expand an expression."""

    return symbolic_question(
        prompt or f"Expand `{expression}`.",
        expression,
        resolver="expand",
        variable=variable,
    )


def factor_question(
    expression: object,
    *,
    prompt: str | None = None,
    variable: str = "x",
) -> Question:
    """Create a question that asks learners to factor an expression."""

    return symbolic_question(
        prompt or f"Factor `{expression}`.",
        expression,
        resolver="factor",
        variable=variable,
    )


__all__ = [
    *_legacy_quiz_exports,
    "expand_question",
    "factor_question",
    "symbolic_question",
]
