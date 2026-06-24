"""Discrete mathematics concept metadata."""

from __future__ import annotations

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

LOGIC = Lesson(
    title="Logic",
    slug="logic",
    objectives=(
        LearningObjective("Identify propositions and truth values."),
        LearningObjective("Build truth tables for compound statements."),
        LearningObjective("Explain implication, converse, and contrapositive."),
    ),
    sections=(
        LessonSection(
            title="Truth and structure",
            body="Logic makes mathematical statements precise enough to prove.",
        ),
    ),
    prerequisites=("careful reading", "basic Python booleans"),
    summary="Logic studies precise true/false statements and their connections.",
    tags=("discrete-math", "logic"),
)

SETS = Lesson(
    title="Sets",
    slug="sets",
    objectives=(
        LearningObjective("Use membership and subset notation."),
        LearningObjective("Compute unions, intersections, and differences."),
        LearningObjective("Connect sets to events, filters, and finite structures."),
    ),
    sections=(
        LessonSection(
            title="Collections",
            body="A set is a collection where order and repetition do not matter.",
        ),
    ),
    prerequisites=("basic notation", "Python sets"),
    summary=(
        "Sets organize objects and support operations such as union and intersection."
    ),
    tags=("discrete-math", "sets"),
)

FUNCTIONS_RELATIONS = Lesson(
    title="Functions and relations",
    slug="functions-relations",
    objectives=(
        LearningObjective("Represent relations as sets of ordered pairs."),
        LearningObjective("Decide whether a relation is a function."),
        LearningObjective("Classify simple relation properties."),
    ),
    sections=(
        LessonSection(
            title="Pairs and rules",
            body="A function is a relation where each input has one output.",
        ),
    ),
    prerequisites=("sets", "ordered pairs", "function notation"),
    summary="Relations describe pair connections; functions are special relations.",
    tags=("discrete-math", "relations", "functions"),
)

SEQUENCES = Lesson(
    title="Sequences",
    slug="sequences",
    objectives=(
        LearningObjective("Compute terms from explicit and recursive rules."),
        LearningObjective("Recognize arithmetic and geometric patterns."),
        LearningObjective("Interpret summation notation."),
    ),
    sections=(
        LessonSection(
            title="Ordered patterns",
            body="A sequence is an ordered list whose position matters.",
        ),
    ),
    prerequisites=("algebra", "exponents", "function notation"),
    summary="Sequences are functions whose inputs are integers.",
    tags=("discrete-math", "sequences"),
)

INDUCTION = Lesson(
    title="Induction",
    slug="induction",
    objectives=(
        LearningObjective("Identify base case and induction hypothesis."),
        LearningObjective("Prove an induction step."),
        LearningObjective("Use induction for sums and divisibility."),
    ),
    sections=(
        LessonSection(
            title="Proof chains",
            body="Induction proves infinitely many indexed statements using a chain.",
        ),
    ),
    prerequisites=("logic", "algebra", "integer notation"),
    summary="Induction proves statements for all integers in a starting range.",
    tags=("discrete-math", "proofs", "induction"),
)

GRAPHS = Lesson(
    title="Graphs",
    slug="graphs",
    objectives=(
        LearningObjective("Define vertices and edges."),
        LearningObjective("Compute degrees and neighbors."),
        LearningObjective("Recognize paths, cycles, and connected graphs."),
    ),
    sections=(
        LessonSection(
            title="Networks",
            body="Graph theory studies networks made of vertices and edges.",
        ),
    ),
    prerequisites=("sets", "relations", "basic counting"),
    summary=(
        "Graphs model networks such as roads, friendships, links, and dependencies."
    ),
    tags=("discrete-math", "graphs"),
)

DISCRETE_MATH_PATH = StudyPath(
    title="Discrete Mathematics",
    lessons=(LOGIC, SETS, FUNCTIONS_RELATIONS, SEQUENCES, INDUCTION, GRAPHS),
)

__all__ = [
    "DISCRETE_MATH_PATH",
    "FUNCTIONS_RELATIONS",
    "GRAPHS",
    "INDUCTION",
    "LOGIC",
    "SEQUENCES",
    "SETS",
]
