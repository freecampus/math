"""General-purpose symbolic solvers for edu-math lessons and apps."""

from edumath.solvers.equations import (
    parse_equation,
    solve_equation,
    solve_equation_steps,
)
from edumath.solvers.explanations import (
    DEFAULT_OPENAI_MODEL,
    DEFAULT_OPENAI_RESPONSES_URL,
    EquationExplanationClient,
    OpenAIEquationExplanationClient,
    extract_openai_response_text,
)
from edumath.solvers.models import (
    EquationSolution,
    EquationSolutionCheck,
    EquationStep,
)

__all__ = [
    "DEFAULT_OPENAI_MODEL",
    "DEFAULT_OPENAI_RESPONSES_URL",
    "EquationExplanationClient",
    "EquationSolution",
    "EquationSolutionCheck",
    "EquationStep",
    "OpenAIEquationExplanationClient",
    "extract_openai_response_text",
    "parse_equation",
    "solve_equation",
    "solve_equation_steps",
]
