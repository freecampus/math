"""General-purpose symbolic solvers for edu-math lessons and apps."""

from edumath.settings import DEFAULT_OPENAI_MODEL
from edumath.solvers.equations import solve_equation, solve_equation_steps
from edumath.solvers.explanations import (
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
    "solve_equation",
    "solve_equation_steps",
]
