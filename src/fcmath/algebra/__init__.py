"""Algebra learning tools."""

from fcmath.algebra.concepts import COLLEGE_ALGEBRA_PATH
from fcmath.algebra.exercises import (
    expand_expression_exercise,
    linear_equation_exercise,
)
from fcmath.algebra.functions import (
    LinearModel,
    QuadraticModel,
    line_from_points,
    quadratic_from_vertex,
)
from fcmath.algebra.plots import (
    compare_functions_scene,
    expression_table,
    function_scene,
    input_output_scene,
    transformation_scene,
    transformed_expression,
)
from fcmath.algebra.polynomials import (
    PolynomialSummary,
    polynomial_from_roots,
    polynomial_root_scene,
    polynomial_summary,
)
from fcmath.algebra.quizzes import (
    GuessingQuiz,
    GuessingQuizWidget,
    GuessQuestion,
    GuessResult,
    SympyGuessGame,
    expand_question,
    factor_question,
    symbolic_question,
)
from fcmath.algebra.validators import (
    validate_expression_equivalence,
    validate_numeric_solution,
)

__all__ = [
    "COLLEGE_ALGEBRA_PATH",
    "GuessQuestion",
    "GuessResult",
    "GuessingQuiz",
    "GuessingQuizWidget",
    "LinearModel",
    "PolynomialSummary",
    "QuadraticModel",
    "SympyGuessGame",
    "compare_functions_scene",
    "expand_expression_exercise",
    "expand_question",
    "expression_table",
    "factor_question",
    "function_scene",
    "input_output_scene",
    "line_from_points",
    "linear_equation_exercise",
    "polynomial_from_roots",
    "polynomial_root_scene",
    "polynomial_summary",
    "quadratic_from_vertex",
    "symbolic_question",
    "transformation_scene",
    "transformed_expression",
    "validate_expression_equivalence",
    "validate_numeric_solution",
]
