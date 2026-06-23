"""Calculus learning tools."""

from edumath.calculus.concepts import (
    CALCULUS_APPLICATIONS,
    CALCULUS_PATH,
    DERIVATIVE_RULES,
    DERIVATIVES,
    INTEGRALS,
    INTEGRATION_TECHNIQUES,
    LIMITS,
    OPTIMIZATION,
)
from edumath.calculus.derivatives import (
    average_rate_of_change,
    derivative,
    finite_difference,
    tangent_line,
)
from edumath.calculus.exercises import (
    critical_point_exercise,
    derivative_rule_exercise,
    limit_estimate_exercise,
    riemann_sum_exercise,
    tangent_line_exercise,
    tool_choice_exercise,
)
from edumath.calculus.integrals import (
    antiderivative,
    definite_integral,
    left_riemann_sum,
    midpoint_riemann_sum,
    right_riemann_sum,
    trapezoid_rule,
)
from edumath.calculus.plots import (
    accumulation_scene,
    derivative_sign_scene,
    optimization_scene,
    riemann_sum_scene,
    secant_tangent_scene,
)
from edumath.calculus.quizzes import (
    antiderivative_question,
    calculus_diagnostic_quiz,
    calculus_tool_question,
    definite_integral_question,
    derivative_question,
    optimization_question,
)
from edumath.calculus.validators import (
    validate_antiderivative_equivalence,
    validate_critical_point,
    validate_derivative_equivalence,
    validate_limit_value,
    validate_numeric_approximation,
)

__all__ = [
    "CALCULUS_APPLICATIONS",
    "CALCULUS_PATH",
    "DERIVATIVES",
    "DERIVATIVE_RULES",
    "INTEGRALS",
    "INTEGRATION_TECHNIQUES",
    "LIMITS",
    "OPTIMIZATION",
    "accumulation_scene",
    "antiderivative",
    "antiderivative_question",
    "average_rate_of_change",
    "calculus_diagnostic_quiz",
    "calculus_tool_question",
    "critical_point_exercise",
    "definite_integral",
    "definite_integral_question",
    "derivative",
    "derivative_question",
    "derivative_rule_exercise",
    "derivative_sign_scene",
    "finite_difference",
    "left_riemann_sum",
    "limit_estimate_exercise",
    "midpoint_riemann_sum",
    "optimization_question",
    "optimization_scene",
    "riemann_sum_exercise",
    "riemann_sum_scene",
    "right_riemann_sum",
    "secant_tangent_scene",
    "tangent_line",
    "tangent_line_exercise",
    "tool_choice_exercise",
    "trapezoid_rule",
    "validate_antiderivative_equivalence",
    "validate_critical_point",
    "validate_derivative_equivalence",
    "validate_limit_value",
    "validate_numeric_approximation",
]
