"""General-purpose symbolic solvers for FreeCampus Math lessons and apps."""

from fcmath.settings import DEFAULT_OPENAI_MODEL
from fcmath.solvers.equations import solve_equation, solve_equation_steps
from fcmath.solvers.explanations import (
    DEFAULT_OPENAI_RESPONSES_URL,
    EquationExplanationClient,
    OpenAIEquationExplanationClient,
    extract_openai_response_text,
)
from fcmath.solvers.models import (
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
