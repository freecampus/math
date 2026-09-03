"""Public validation API for answers and curriculum structure."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fcmath.validation.coverage import validate_coverage_matrix

_LAZY_EXPORTS = {
    "AlgebraicForm": ("fcmath.validation.answers", "AlgebraicForm"),
    "CurriculumValidationError": (
        "fcmath.validation.curriculum",
        "CurriculumValidationError",
    ),
    "DomainName": ("fcmath.validation.answers", "DomainName"),
    "ValidationIssue": ("fcmath.validation.curriculum", "ValidationIssue"),
    "ValidationMode": ("fcmath.validation.answers", "ValidationMode"),
    "ValidationPolicy": ("fcmath.validation.answers", "ValidationPolicy"),
    "check_answer": ("fcmath.validation.answers", "check_answer"),
    "load_structured_data": ("fcmath.validation.curriculum", "load_structured_data"),
    "parse_solution_set": ("fcmath.validation.answers", "parse_solution_set"),
    "validate_catalog": ("fcmath.validation.curriculum", "validate_catalog"),
    "validate_coverage_matrix": (
        "fcmath.validation.coverage",
        "validate_coverage_matrix",
    ),
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(name)
    module_name, attribute = _LAZY_EXPORTS[name]
    value = getattr(import_module(module_name), attribute)
    globals()[name] = value
    return value


__all__ = list(_LAZY_EXPORTS)
