"""Public validation API for answers and curriculum structure."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fcmath.validation.answers import AlgebraicForm as AlgebraicForm
    from fcmath.validation.answers import DomainName as DomainName
    from fcmath.validation.answers import ValidationMode as ValidationMode
    from fcmath.validation.answers import ValidationPolicy as ValidationPolicy
    from fcmath.validation.answers import check_answer as check_answer
    from fcmath.validation.answers import parse_solution_set as parse_solution_set
    from fcmath.validation.coverage import (
        validate_coverage_matrix as validate_coverage_matrix,
    )
    from fcmath.validation.curriculum import (
        CurriculumValidationError as CurriculumValidationError,
    )
    from fcmath.validation.curriculum import ValidationIssue as ValidationIssue
    from fcmath.validation.curriculum import (
        load_structured_data as load_structured_data,
    )
    from fcmath.validation.curriculum import validate_catalog as validate_catalog
    from fcmath.validation.resources import (
        validate_external_resources as validate_external_resources,
    )

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
    "validate_external_resources": (
        "fcmath.validation.resources",
        "validate_external_resources",
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
