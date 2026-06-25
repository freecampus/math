"""Tests for statistics lesson helpers."""

from __future__ import annotations

import math

import pytest

from edumath.statistics import (
    STATISTICS_PATH,
    confidence_interval_proportion,
    correlation,
    describe,
    five_number_summary,
    interquartile_range,
    margin_of_error,
    mean_exercise,
    normal_p_value,
    one_sample_z_test,
    outlier_fences,
    predict,
    residuals,
    sampling_bias_exercise,
    simple_linear_regression,
    standard_error,
    validate_interval_answer,
    validate_keyword_answer,
    validate_numeric_answer,
    z_score,
)


def test_statistics_path_lists_expected_lessons() -> None:
    assert STATISTICS_PATH.slugs() == [
        "descriptive-statistics",
        "sampling",
        "probability-for-statistics",
        "sampling-distributions",
        "estimation",
        "hypothesis-tests",
        "comparing-groups",
        "chi-square-tests",
        "regression-basics",
        "statistics-cumulative-review",
    ]


def test_descriptive_and_quartile_helpers() -> None:
    stats = describe([1, 2, 3, 4], sample=False)
    summary = five_number_summary([1, 2, 3, 4])

    assert stats.mean == 2.5
    assert stats.variance == 1.25
    assert summary.minimum == 1
    assert summary.maximum == 4
    assert math.isclose(interquartile_range([1, 2, 3, 4]), 1.5)


def test_outlier_fences_identify_extreme_values() -> None:
    fences = outlier_fences([1, 2, 2, 3, 100])

    assert fences.lower < 1
    assert fences.upper < 100
    assert fences.outliers == (100.0,)


def test_standard_error_confidence_interval_and_z_helpers() -> None:
    assert standard_error(12, 36) == 2
    assert z_score(14, 10, 2) == 2
    assert math.isclose(margin_of_error(2), 3.919927969080108, rel_tol=1e-12)

    interval = confidence_interval_proportion(60, 100)
    assert math.isclose(interval.estimate, 0.6)
    assert interval.lower < 0.6 < interval.upper

    test = one_sample_z_test(105, 100, 2.5, alternative="greater")
    assert math.isclose(test.statistic, 2)
    assert math.isclose(test.p_value, normal_p_value(2, alternative="greater"))


def test_regression_helpers() -> None:
    line = simple_linear_regression([1, 2, 3], [3, 5, 7])

    assert math.isclose(line.slope, 2)
    assert math.isclose(line.intercept, 1)
    assert math.isclose(line.correlation, 1)
    assert math.isclose(correlation([1, 2, 3], [3, 5, 7]), 1)
    assert math.isclose(predict(line, 4), 9)
    assert residuals(line, [1, 2, 3], [3, 5, 7]) == (0.0, 0.0, 0.0)


def test_statistics_validators_and_exercises() -> None:
    numeric_check = validate_numeric_answer("1/2", 0.5)
    interval_check = validate_interval_answer("[0.1, 0.2]", (0.1, 0.2))
    keyword_check = validate_keyword_answer("Fail_To_Reject", "fail-to-reject")

    assert numeric_check.correct
    assert interval_check.correct
    assert keyword_check.correct

    mean = mean_exercise(seed=1)
    assert mean.validator is not None
    assert mean.validator(mean.expected).correct

    bias = sampling_bias_exercise(seed=1)
    assert bias.validator is not None
    assert bias.validator(bias.expected).correct


def test_statistics_helpers_validate_inputs() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        describe([])

    with pytest.raises(ValueError, match="positive"):
        z_score(3, 2, 0)

    with pytest.raises(ValueError, match="same length"):
        simple_linear_regression([1, 2], [1])
