"""Deterministic exercise builders for statistics lessons."""

from __future__ import annotations

from random import Random

from edumath.core import AnswerCheck, Exercise
from edumath.statistics.concepts import (
    confidence_interval_proportion,
    describe,
    predict,
    simple_linear_regression,
    standard_error,
)
from edumath.statistics.validators import (
    validate_interval_answer,
    validate_keyword_answer,
    validate_numeric_answer,
)


def mean_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a mean calculation exercise."""

    rng = Random(seed)
    values = rng.choice(([2, 4, 6, 8], [3, 5, 7], [1, 2, 3, 10]))
    expected = describe(values, sample=False).mean
    return Exercise(
        prompt=f"Find the mean of {list(values)}.",
        expected=expected,
        validator=lambda received: validate_numeric_answer(received, expected),
        hint="Add the values, then divide by how many values there are.",
        explanation="The mean is the arithmetic balance point of the data.",
        tags=("statistics", "descriptive-statistics", "mean"),
        exercise_id="statistics-mean",
        answer_type="numeric",
    )


def standard_error_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a standard-error exercise."""

    rng = Random(seed)
    standard_deviation_value, sample_size = rng.choice(((12, 36), (10, 25), (8, 64)))
    expected = standard_error(standard_deviation_value, sample_size)
    return Exercise(
        prompt=(
            "A sample mean has sample standard deviation "
            f"{standard_deviation_value} and n={sample_size}. Find the standard error."
        ),
        expected=expected,
        validator=lambda received: validate_numeric_answer(received, expected),
        hint="Use standard error = standard deviation / sqrt(n).",
        explanation=(
            "Standard error measures sample-to-sample variation of an estimate."
        ),
        tags=("statistics", "sampling-distributions", "standard-error"),
        exercise_id="statistics-standard-error",
        answer_type="numeric",
    )


def confidence_interval_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a proportion confidence-interval exercise."""

    rng = Random(seed)
    successes, sample_size = rng.choice(((60, 100), (45, 90), (180, 300)))
    interval = confidence_interval_proportion(successes, sample_size)
    expected = (interval.lower, interval.upper)
    return Exercise(
        prompt=(
            f"In a sample of {sample_size}, {successes} are successes. "
            "Give the approximate 95% confidence interval for the proportion."
        ),
        expected=expected,
        validator=lambda received: validate_interval_answer(received, expected),
        hint="Compute p-hat, standard error sqrt(p-hat(1-p-hat)/n), then use 1.96 SE.",
        explanation="A confidence interval is estimate ± margin of error.",
        tags=("statistics", "estimation", "confidence-intervals"),
        exercise_id="statistics-confidence-interval-proportion",
        answer_type="numeric",
    )


def hypothesis_test_interpretation_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a p-value interpretation exercise."""

    rng = Random(seed)
    cases = (
        ("p-value = 0.01 with alpha = 0.05", "reject"),
        ("p-value = 0.18 with alpha = 0.05", "fail-to-reject"),
        ("p-value = 0.04 with alpha = 0.10", "reject"),
    )
    prompt, expected = rng.choice(cases)
    return Exercise(
        prompt=f"Decision for {prompt}: reject or fail-to-reject?",
        expected=expected,
        validator=lambda received: validate_keyword_answer(received, expected),
        hint="Reject the null hypothesis when p-value <= alpha.",
        explanation=(
            "A smaller p-value than alpha is treated as statistically significant."
        ),
        tags=("statistics", "hypothesis-tests", "p-values"),
        exercise_id="statistics-hypothesis-decision",
        answer_type="multiple_choice",
    )


def regression_prediction_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a simple regression prediction exercise."""

    rng = Random(seed)
    x_values, y_values, x_predict = rng.choice(
        (
            ([1, 2, 3], [3, 5, 7], 4),
            ([0, 1, 2], [10, 13, 16], 3),
            ([2, 4, 6], [5, 9, 13], 8),
        )
    )
    line = simple_linear_regression(x_values, y_values)
    expected = predict(line, x_predict)
    return Exercise(
        prompt=(
            f"Fit the line for x={x_values}, y={y_values}. "
            f"Predict y when x={x_predict}."
        ),
        expected=expected,
        validator=lambda received: validate_numeric_answer(received, expected),
        hint="Find the linear pattern or fit y = intercept + slope*x.",
        explanation="The prediction comes from the least-squares regression line.",
        tags=("statistics", "regression", "prediction"),
        exercise_id="statistics-regression-prediction",
        answer_type="numeric",
    )


def sampling_bias_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a sampling-bias classification exercise."""

    rng = Random(seed)
    cases = (
        ("Survey only people who visit a gym about exercise habits.", "selection-bias"),
        ("Many selected people do not answer the survey.", "nonresponse-bias"),
        ("Ask 'Do you agree with this obviously helpful policy?'", "response-bias"),
    )
    prompt, expected = rng.choice(cases)
    return Exercise(
        prompt=f"Name the main bias: {prompt}",
        expected=expected,
        validator=lambda received: validate_keyword_answer(received, expected),
        hint="Ask whether the issue is who was selected, who answered, or wording.",
        explanation="Bias is a systematic error in how data are collected or measured.",
        tags=("statistics", "sampling", "bias"),
        exercise_id="statistics-sampling-bias",
        answer_type="multiple_choice",
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
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "confidence_interval_exercise",
    "hypothesis_test_interpretation_exercise",
    "mean_exercise",
    "regression_prediction_exercise",
    "sampling_bias_exercise",
    "standard_error_exercise",
]
