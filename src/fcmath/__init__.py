"""Small public Python interface supporting the FreeCampus Math curriculum."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__version__ = "0.1.0"  # semantic-release

_LAZY_EXPORTS = {
    "QuizBank": ("fcmath.quizzes", "QuizBank"),
    "QuizQuestion": ("fcmath.quizzes", "QuizQuestion"),
    "ValidationPolicy": ("fcmath.validation", "ValidationPolicy"),
    "check_answer": ("fcmath.validation", "check_answer"),
    "load_quiz": ("fcmath.quizzes", "load_quiz"),
    "parse_equation": ("fcmath.core", "parse_equation"),
    "parse_expression": ("fcmath.core", "parse_expression"),
    "parse_solution_set": ("fcmath.validation", "parse_solution_set"),
    "solve_equation": ("fcmath.solvers", "solve_equation"),
    "solve_equation_steps": ("fcmath.solvers", "solve_equation_steps"),
}


def __getattr__(name: str) -> Any:
    """Load public features only when requested.

    This keeps catalog tooling and package-version checks independent of
    plotting, SymPy, and notebook frontends while preserving a concise API.
    """

    if name not in _LAZY_EXPORTS:
        raise AttributeError(name)
    module_name, attribute = _LAZY_EXPORTS[name]
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value


__all__ = [*_LAZY_EXPORTS, "__version__"]
