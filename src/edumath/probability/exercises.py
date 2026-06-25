"""Deterministic exercise builders for probability lessons."""

from __future__ import annotations

from random import Random

from edumath.core import AnswerCheck, Exercise
from edumath.probability.concepts import conditional_probability, probability
from edumath.probability.distributions import combinations, expected_value
from edumath.probability.validators import validate_probability_answer


def sample_space_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a finite event-probability exercise."""

    rng = Random(seed)
    cases = (
        ((1, 2, 3, 4, 5, 6), {2, 4, 6}, "rolling an even number on a fair die"),
        (("H", "T"), {"H"}, "getting heads on one fair coin flip"),
        ((1, 2, 3, 4), {3, 4}, "getting a number greater than 2 from {1,2,3,4}"),
    )
    sample_space, event, story = rng.choice(cases)
    expected = probability(event, sample_space)
    return Exercise(
        prompt=f"Find the probability of {story}.",
        expected=expected,
        validator=lambda received: validate_probability_answer(received, expected),
        hint="Count favorable outcomes and divide by total equally likely outcomes.",
        explanation="Probability is favorable outcomes divided by total outcomes.",
        tags=("probability", "sample-spaces", "events"),
        exercise_id="probability-sample-space",
        answer_type="numeric",
    )


def counting_decision_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a combination-counting exercise."""

    rng = Random(seed)
    n = rng.choice((5, 6, 7, 8))
    k = rng.choice((2, 3))
    expected = combinations(n, k)
    return Exercise(
        prompt=f"How many ways are there to choose {k} items from {n} items?",
        expected=expected,
        validator=lambda received: _validate_int(received, expected),
        hint="Order does not matter, so use a combination.",
        explanation="Use C(n,k) = n! / (k!(n-k)!).",
        tags=("probability", "counting", "combinations"),
        exercise_id="probability-counting-combination",
        answer_type="numeric",
    )


def conditional_probability_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a finite conditional-probability exercise."""

    rng = Random(seed)
    sample_space = tuple(range(1, 7))
    event = {2, 4, 6}
    given_options = ({4, 5, 6}, {1, 2, 3, 4}, {2, 3, 5})
    given = rng.choice(given_options)
    expected = conditional_probability(event, given, sample_space)
    return Exercise(
        prompt=(
            "Roll a fair die. Let A be the event 'even' and B be "
            f"{sorted(given)}. Find P(A | B)."
        ),
        expected=expected,
        validator=lambda received: validate_probability_answer(received, expected),
        hint="Restrict the sample space to B, then count outcomes that are also in A.",
        explanation="P(A | B) = |A intersection B| / |B| for equally likely outcomes.",
        tags=("probability", "conditional-probability"),
        exercise_id="probability-conditional",
        answer_type="numeric",
    )


def distribution_matching_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a distribution-matching exercise."""

    rng = Random(seed)
    cases = (
        ("one yes/no trial", "bernoulli"),
        ("number of successes in fixed independent trials", "binomial"),
        ("measurement noise clustered around a mean", "normal"),
        ("each value in an interval or finite set is equally likely", "uniform"),
    )
    prompt, expected = rng.choice(cases)
    return Exercise(
        prompt=f"Which distribution pattern matches this story: {prompt}?",
        expected=expected,
        validator=lambda received: _validate_keyword(received, expected),
        hint="Ask what values are possible and how the probabilities are assigned.",
        explanation=f"The story is a typical use of the {expected} distribution.",
        tags=("probability", "distributions"),
        exercise_id="probability-distribution-match",
        answer_type="multiple_choice",
    )


def expectation_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a small expected-value exercise."""

    rng = Random(seed)
    cases = (
        ([0, 10], [0.7, 0.3]),
        ([1, 2, 3], [0.2, 0.5, 0.3]),
        ([-2, 4], [0.25, 0.75]),
    )
    values, probabilities = rng.choice(cases)
    expected = expected_value(values, probabilities)
    return Exercise(
        prompt=(
            f"Find the expected value for values {values} "
            f"with probabilities {probabilities}."
        ),
        expected=expected,
        validator=lambda received: validate_probability_answer(received, expected),
        hint="Multiply each value by its probability, then add.",
        explanation="Expected value is a weighted average.",
        tags=("probability", "expectation"),
        exercise_id="probability-expectation",
        answer_type="numeric",
    )


def _validate_int(received: object, expected: int) -> AnswerCheck:
    try:
        value = int(str(received).strip())
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            False, received, expected, f"Could not read integer: {error}"
        )
    correct = value == expected
    return AnswerCheck(
        correct, received, expected, "Correct." if correct else f"Expected {expected}."
    )


def _validate_keyword(received: object, expected: str) -> AnswerCheck:
    normalized = str(received).strip().lower()
    correct = normalized == expected
    return AnswerCheck(
        correct, received, expected, "Correct." if correct else f"Expected {expected}."
    )


__all__ = [
    "conditional_probability_exercise",
    "counting_decision_exercise",
    "distribution_matching_exercise",
    "expectation_exercise",
    "sample_space_exercise",
]
