"""Probability concepts and finite-set helpers."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import TypeVar

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

T = TypeVar("T", bound=Hashable)

SAMPLE_SPACES_EVENTS = Lesson(
    title="Sample Spaces and Events",
    slug="sample-spaces-events",
    prerequisites=("sets", "fractions", "basic counting"),
    objectives=(
        LearningObjective("List outcomes in a sample space."),
        LearningObjective("Represent events as subsets of a sample space."),
        LearningObjective("Compute simple probabilities by counting outcomes."),
    ),
    sections=(
        LessonSection(
            title="Outcomes and events",
            body=(
                "A probability model begins by naming every possible outcome and "
                "then describing events as subsets of those outcomes."
            ),
        ),
    ),
    summary="Probability starts by clearly naming what can happen.",
    tags=("probability", "sample-spaces", "events"),
)

COUNTING = Lesson(
    title="Counting",
    slug="counting",
    prerequisites=("multiplication", "fractions", "sets"),
    objectives=(
        LearningObjective("Use product and sum rules for counting."),
        LearningObjective("Distinguish permutations from combinations."),
        LearningObjective("Use counting results to compute probabilities."),
    ),
    sections=(
        LessonSection(
            title="Counting before probability",
            body=(
                "Many probabilities are favorable outcomes divided by total "
                "outcomes, so careful counting comes first."
            ),
        ),
    ),
    summary="Counting methods turn large sample spaces into manageable numbers.",
    tags=("probability", "counting", "combinations", "permutations"),
)

CONDITIONAL_PROBABILITY = Lesson(
    title="Conditional Probability",
    slug="conditional-probability",
    prerequisites=("fractions", "events", "two-way tables"),
    objectives=(
        LearningObjective("Interpret conditional probability as updated information."),
        LearningObjective("Compute conditional probability from counts or formulas."),
        LearningObjective("Recognize independence and Bayes' rule situations."),
    ),
    sections=(
        LessonSection(
            title="Probability after information",
            body=(
                "Conditional probability restricts attention to the outcomes that "
                "remain possible after new information is known."
            ),
        ),
    ),
    summary="Conditional probability is the language of updating information.",
    tags=("probability", "conditional-probability", "bayes"),
)

RANDOM_VARIABLES = Lesson(
    title="Random Variables",
    slug="random-variables",
    prerequisites=("functions", "sample spaces", "tables"),
    objectives=(
        LearningObjective("Define a random variable as a numeric rule on outcomes."),
        LearningObjective("Classify random variables as discrete or continuous."),
        LearningObjective("Read and validate simple probability mass functions."),
    ),
    sections=(
        LessonSection(
            title="Numbers from random outcomes",
            body=(
                "A random variable assigns a number to each outcome so that "
                "probability questions can be studied with arithmetic."
            ),
        ),
    ),
    summary="Random variables convert random outcomes into numeric data.",
    tags=("probability", "random-variables", "pmf"),
)

COMMON_DISTRIBUTIONS = Lesson(
    title="Common Distributions",
    slug="common-distributions",
    prerequisites=("random variables", "counting", "functions"),
    objectives=(
        LearningObjective("Match common distributions to real situations."),
        LearningObjective("Compute binomial probabilities."),
        LearningObjective("Interpret parameters such as n, p, mean, and spread."),
    ),
    sections=(
        LessonSection(
            title="Reusable probability patterns",
            body=(
                "A distribution describes how probability is assigned across possible "
                "values of a random variable."
            ),
        ),
    ),
    summary="Common distributions are named patterns for common random situations.",
    tags=("probability", "distributions", "binomial", "normal"),
)

EXPECTATION_VARIANCE = Lesson(
    title="Expectation and Variance",
    slug="expectation-variance",
    prerequisites=("random variables", "weighted averages", "squares"),
    objectives=(
        LearningObjective("Compute expected value as a weighted average."),
        LearningObjective("Compute variance and standard deviation for small tables."),
        LearningObjective("Interpret center and spread in decision-making."),
    ),
    sections=(
        LessonSection(
            title="Center and spread",
            body=(
                "Expectation describes the long-run center of a random variable, "
                "while variance describes how far outcomes tend to be from that center."
            ),
        ),
    ),
    summary="Expectation and variance summarize a probability distribution.",
    tags=("probability", "expectation", "variance", "risk"),
)

PROBABILITY_PATH = StudyPath(
    title="Probability",
    lessons=(
        SAMPLE_SPACES_EVENTS,
        COUNTING,
        CONDITIONAL_PROBABILITY,
        RANDOM_VARIABLES,
        COMMON_DISTRIBUTIONS,
        EXPECTATION_VARIANCE,
    ),
)


def probability(event: Iterable[T], sample_space: Iterable[T]) -> float:
    """Return ``P(event)`` for a finite equally likely sample space."""

    sample = set(sample_space)
    event_set = set(event)
    _validate_nonempty_sample_space(sample)
    _validate_subset(event_set, sample, name="event")
    return len(event_set) / len(sample)


def complement(event: Iterable[T], sample_space: Iterable[T]) -> set[T]:
    """Return the complement of an event inside a finite sample space."""

    sample = set(sample_space)
    event_set = set(event)
    _validate_nonempty_sample_space(sample)
    _validate_subset(event_set, sample, name="event")
    return sample - event_set


def union(*events: Iterable[T]) -> set[T]:
    """Return the union of finite events."""

    result: set[T] = set()
    for event in events:
        result |= set(event)
    return result


def intersection(*events: Iterable[T]) -> set[T]:
    """Return the intersection of finite events."""

    if not events:
        return set()
    iterator = iter(events)
    result = set(next(iterator))
    for event in iterator:
        result &= set(event)
    return result


def conditional_probability(
    event: Iterable[T],
    given: Iterable[T],
    sample_space: Iterable[T],
) -> float:
    """Return ``P(event | given)`` for a finite equally likely sample space."""

    sample = set(sample_space)
    event_set = set(event)
    given_set = set(given)
    _validate_nonempty_sample_space(sample)
    _validate_subset(event_set, sample, name="event")
    _validate_subset(given_set, sample, name="given event")
    if not given_set:
        msg = "given event must not be empty"
        raise ValueError(msg)
    return len(event_set & given_set) / len(given_set)


def _validate_nonempty_sample_space(sample_space: set[T]) -> None:
    if not sample_space:
        msg = "sample space must not be empty"
        raise ValueError(msg)


def _validate_subset(event: set[T], sample_space: set[T], *, name: str) -> None:
    if not event <= sample_space:
        missing = event - sample_space
        msg = f"{name} contains outcomes not in the sample space: {list(missing)!r}"
        raise ValueError(msg)


__all__ = [
    "COMMON_DISTRIBUTIONS",
    "CONDITIONAL_PROBABILITY",
    "COUNTING",
    "EXPECTATION_VARIANCE",
    "PROBABILITY_PATH",
    "RANDOM_VARIABLES",
    "SAMPLE_SPACES_EVENTS",
    "complement",
    "conditional_probability",
    "intersection",
    "probability",
    "union",
]
