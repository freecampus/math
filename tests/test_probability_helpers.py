import math

import pytest

from edumath.probability import (
    PROBABILITY_PATH,
    bernoulli_pmf,
    binomial_mean,
    binomial_pmf,
    binomial_variance,
    combinations,
    complement,
    conditional_probability,
    conditional_probability_exercise,
    counting_decision_exercise,
    distribution_matching_exercise,
    expectation_exercise,
    expected_value,
    factorial,
    intersection,
    is_independent,
    permutations,
    probability,
    sample_space_exercise,
    standard_deviation,
    union,
    validate_event_subset,
    validate_pmf,
    validate_probabilities,
    validate_probability_answer,
    variance,
)


def test_probability_path_has_expected_lessons() -> None:
    assert PROBABILITY_PATH.slugs() == [
        "sample-spaces-events",
        "counting",
        "conditional-probability",
        "random-variables",
        "common-distributions",
        "expectation-variance",
    ]


def test_finite_event_helpers() -> None:
    sample_space = {1, 2, 3, 4, 5, 6}
    even = {2, 4, 6}
    large = {4, 5, 6}
    assert probability(even, sample_space) == 0.5
    assert complement(even, sample_space) == {1, 3, 5}
    assert union(even, large) == {2, 4, 5, 6}
    assert intersection(even, large) == {4, 6}
    assert conditional_probability(even, large, sample_space) == pytest.approx(2 / 3)
    with pytest.raises(ValueError):
        probability({7}, sample_space)


def test_distribution_helpers() -> None:
    assert factorial(5) == 120
    assert combinations(6, 2) == 15
    assert permutations(6, 2) == 30
    assert bernoulli_pmf(1, 0.25) == 0.25
    assert bernoulli_pmf(0, 0.25) == 0.75
    assert math.isclose(binomial_pmf(10, 3, 0.5), 0.1171875)
    assert binomial_mean(10, 0.4) == 4
    assert binomial_variance(10, 0.4) == pytest.approx(2.4)
    assert expected_value([0, 1], [0.25, 0.75]) == 0.75
    assert variance([0, 2], [0.5, 0.5]) == 1
    assert standard_deviation([0, 2], [0.5, 0.5]) == 1


@pytest.mark.parametrize(
    ("func", "args"),
    [
        (factorial, (-1,)),
        (combinations, (2, 3)),
        (permutations, (2, 3)),
        (binomial_pmf, (3, 1, 1.5)),
        (expected_value, ([1, 2], [0.2, 0.2])),
    ],
)
def test_invalid_distribution_inputs_raise(func, args) -> None:
    with pytest.raises(ValueError):
        func(*args)


def test_probability_validators() -> None:
    assert validate_probability_answer("1/2", 0.5).correct
    assert validate_probability_answer("25%", 0.25).correct
    assert validate_probabilities([0.2, 0.3, 0.5]).correct
    assert not validate_probabilities([0.2, 0.3]).correct
    assert validate_pmf([0, 1], [0.4, 0.6]).correct
    assert not validate_pmf([0, 1], [0.4]).correct
    assert validate_event_subset({1, 2}, {1, 2, 3}).correct
    assert not validate_event_subset({1, 4}, {1, 2, 3}).correct
    assert is_independent(0.5, 0.4, 0.2)
    assert not is_independent(0.5, 0.4, 0.3)


def test_exercise_builders_accept_expected_answers() -> None:
    exercises = (
        sample_space_exercise(seed=1),
        counting_decision_exercise(seed=1),
        conditional_probability_exercise(seed=1),
        distribution_matching_exercise(seed=1),
        expectation_exercise(seed=1),
    )
    for exercise in exercises:
        assert exercise.check(exercise.expected).correct
