"""Discrete mathematics exercise builders."""

from __future__ import annotations

from collections.abc import Sequence
from random import Random
from typing import cast

from edumath.core import AnswerCheck, Exercise
from edumath.discrete_math.graphs import degree
from edumath.discrete_math.logic import implies
from edumath.discrete_math.sets import set_operation_table
from edumath.discrete_math.validators import (
    validate_graph_degree_sequence,
    validate_set_answer,
    validate_truth_value,
)


def truth_table_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a truth-value exercise for implication."""

    rng = Random(seed)
    p_value = rng.choice([False, True])
    q_value = rng.choice([False, True])
    expected = implies(p_value, q_value)
    return Exercise(
        prompt=f"Evaluate p -> q when p is {p_value} and q is {q_value}.",
        expected=expected,
        validator=lambda received: validate_truth_value(received, expected),
        explanation="An implication is false only when p is true and q is false.",
        tags=("discrete-math", "logic"),
        answer_type="exact",
    )


def set_operation_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a finite set operation exercise."""

    rng = Random(seed)
    left = set(rng.sample(range(1, 8), 3))
    right = set(rng.sample(range(1, 8), 3))
    operation = rng.choice(["union", "intersection", "a_minus_b"])
    expected = set_operation_table(left, right)[operation]
    symbol = {
        "union": "A union B",
        "intersection": "A intersection B",
        "a_minus_b": "A - B",
    }[operation]
    return Exercise(
        prompt=f"Let A={left} and B={right}. Find {symbol}.",
        expected=expected,
        validator=lambda received: validate_set_answer(received, expected),
        explanation="Apply the set operation directly from the definitions.",
        tags=("discrete-math", "sets"),
        answer_type="exact",
    )


def relation_classification_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a relation/function classification exercise."""

    rng = Random(seed)
    examples = (
        ({(1, 2), (2, 3), (3, 4)}, "function"),
        ({(1, 2), (1, 3), (2, 4)}, "not function"),
    )
    pairs, expected = rng.choice(examples)
    return Exercise(
        prompt=f"Is the relation {pairs} a function?",
        expected=expected,
        validator=lambda received: _check_string(received, expected),
        explanation="A function cannot assign one input to two different outputs.",
        tags=("discrete-math", "relations", "functions"),
        answer_type="multiple_choice",
    )


def sequence_next_term_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a next-term sequence exercise."""

    rng = Random(seed)
    start = rng.randint(1, 5)
    difference = rng.randint(2, 6)
    terms = [start + index * difference for index in range(4)]
    expected = terms[-1] + difference
    return Exercise(
        prompt=(
            f"Find the next term: {terms[0]}, {terms[1]}, {terms[2]}, {terms[3]}, ..."
        ),
        expected=expected,
        explanation="This arithmetic sequence adds the same difference each time.",
        tags=("discrete-math", "sequences"),
        answer_type="numeric",
    )


def induction_step_exercise(*, seed: int | None = None) -> Exercise:
    """Generate an induction-structure exercise."""

    _ = Random(seed)
    expected = "assume p(k), prove p(k+1)"
    return Exercise(
        prompt="What is the main structure of the induction step?",
        expected=expected,
        validator=lambda received: _check_string(received, expected),
        explanation="The induction step proves that truth passes from k to k+1.",
        tags=("discrete-math", "induction"),
        answer_type="exact",
    )


def graph_degree_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a graph degree exercise."""

    rng = Random(seed)
    vertices = ("A", "B", "C", "D")
    edges = (("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"))
    vertex = rng.choice(vertices)
    expected = degree(vertices, edges, vertex)
    return Exercise(
        prompt=f"In the graph with edges {edges}, find degree({vertex}).",
        expected=expected,
        explanation="Degree counts edges incident to the chosen vertex.",
        tags=("discrete-math", "graphs"),
        answer_type="numeric",
    )


def graph_degree_sequence_exercise() -> Exercise:
    """Generate a graph degree-sequence exercise."""

    vertices = ("A", "B", "C")
    edges = (("A", "B"), ("A", "C"))
    expected = (2, 1, 1)
    return Exercise(
        prompt=f"Find the degree sequence for vertices {vertices} and edges {edges}.",
        expected=expected,
        validator=lambda received: validate_graph_degree_sequence(
            cast(Sequence[object], received),
            expected,
        ),
        explanation="Compute each degree, then sort from largest to smallest.",
        tags=("discrete-math", "graphs"),
        answer_type="exact",
    )


def _check_string(received: object, expected: str) -> AnswerCheck:
    normalized = str(received).strip().lower()
    correct = normalized == expected
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "graph_degree_exercise",
    "graph_degree_sequence_exercise",
    "induction_step_exercise",
    "relation_classification_exercise",
    "sequence_next_term_exercise",
    "set_operation_exercise",
    "truth_table_exercise",
]
