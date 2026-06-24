"""Quiz helpers for discrete mathematics lessons."""

from __future__ import annotations

from edumath.core import AnswerOption, Question, QuizSession
from edumath.discrete_math.graphs import degree
from edumath.discrete_math.logic import implies
from edumath.discrete_math.sets import set_operation_table
from edumath.discrete_math.validators import validate_set_answer, validate_truth_value


def truth_table_question() -> Question:
    """Create an implication truth-value question."""

    expected = implies(True, False)
    return Question(
        prompt="What is the truth value of `p -> q` when p is true and q is false?",
        expected=expected,
        options=(
            AnswerOption("True", True),
            AnswerOption("False", False),
        ),
        validator=lambda received: validate_truth_value(received, expected),
        explanation=(
            "An implication fails exactly when the premise is true and the "
            "conclusion is false."
        ),
        tags=("discrete-math", "logic"),
    )


def set_operation_question() -> Question:
    """Create a set-union question."""

    left = {1, 2, 3}
    right = {3, 4}
    expected = set_operation_table(left, right)["union"]
    return Question(
        prompt="Let A={1,2,3} and B={3,4}. What is A union B?",
        expected=expected,
        answer_type="exact",
        validator=lambda received: validate_set_answer(received, expected),
        explanation="The union contains anything in A, in B, or in both.",
        tags=("discrete-math", "sets"),
    )


def relation_function_question() -> Question:
    """Create a function classification question."""

    pairs = {(1, 2), (1, 3), (2, 4)}
    expected = "not function"
    return Question(
        prompt=f"Is {pairs} a function?",
        expected=expected,
        options=(
            AnswerOption("Function", "function"),
            AnswerOption("Not a function", "not function"),
        ),
        explanation=(
            "Input 1 has two different outputs, so the relation is not a function."
        ),
        tags=("discrete-math", "relations", "functions"),
    )


def sequence_pattern_question() -> Question:
    """Create a sequence next-term question."""

    return Question(
        prompt="Find the next term: 3, 6, 12, 24, ...",
        expected=48,
        explanation="The sequence is geometric with common ratio 2.",
        tags=("discrete-math", "sequences"),
    )


def induction_structure_question() -> Question:
    """Create an induction proof-structure question."""

    return Question(
        prompt="What do you assume in the induction hypothesis?",
        expected="P(k)",
        options=(
            AnswerOption("P(k)", "P(k)"),
            AnswerOption("P(k+1)", "P(k+1)"),
            AnswerOption("Only P(1)", "P(1)"),
        ),
        explanation=(
            "The induction hypothesis assumes the statement for k so you can "
            "prove it for k+1."
        ),
        tags=("discrete-math", "induction"),
    )


def graph_degree_question() -> Question:
    """Create a graph degree question."""

    vertices = ("A", "B", "C")
    edges = (("A", "B"), ("A", "C"))
    expected = degree(vertices, edges, "A")
    return Question(
        prompt=f"In the graph with edges {edges}, what is degree(A)?",
        expected=expected,
        explanation="Vertex A is incident to two edges.",
        tags=("discrete-math", "graphs"),
    )


def discrete_math_diagnostic_quiz() -> QuizSession:
    """Return a short diagnostic quiz for discrete mathematics."""

    return QuizSession(
        questions=(
            truth_table_question(),
            set_operation_question(),
            relation_function_question(),
            sequence_pattern_question(),
            induction_structure_question(),
            graph_degree_question(),
        )
    )


__all__ = [
    "discrete_math_diagnostic_quiz",
    "graph_degree_question",
    "induction_structure_question",
    "relation_function_question",
    "sequence_pattern_question",
    "set_operation_question",
    "truth_table_question",
]
