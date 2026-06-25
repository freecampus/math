"""Statistics concepts and reusable computational helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Literal

import numpy as np
import numpy.typing as npt

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

Alternative = Literal["two-sided", "greater", "less"]


@dataclass(frozen=True)
class DescriptiveStats:
    """Basic descriptive statistics."""

    mean: float
    median: float
    variance: float
    standard_deviation: float
    minimum: float
    maximum: float


@dataclass(frozen=True)
class FiveNumberSummary:
    """Minimum, quartiles, median, and maximum for numeric data."""

    minimum: float
    q1: float
    median: float
    q3: float
    maximum: float


@dataclass(frozen=True)
class OutlierFences:
    """Tukey outlier fences and values beyond them."""

    lower: float
    upper: float
    outliers: tuple[float, ...]


@dataclass(frozen=True)
class ConfidenceInterval:
    """A confidence interval with estimate and margin of error."""

    estimate: float
    lower: float
    upper: float
    margin_of_error: float
    confidence_level: float


@dataclass(frozen=True)
class HypothesisTestResult:
    """Normal-approximation hypothesis-test summary."""

    statistic: float
    p_value: float
    alternative: Alternative


@dataclass(frozen=True)
class RegressionLine:
    """Simple linear regression model ``y = intercept + slope * x``."""

    slope: float
    intercept: float
    correlation: float


DESCRIPTIVE_STATISTICS = Lesson(
    title="Descriptive Statistics",
    slug="descriptive-statistics",
    prerequisites=("arithmetic", "fractions", "graphs"),
    objectives=(
        LearningObjective("Summarize data with measures of center and spread."),
        LearningObjective("Use plots and summaries to describe distribution shape."),
        LearningObjective("Identify outliers and understand their effect."),
    ),
    sections=(
        LessonSection(
            title="Data summaries",
            body=(
                "Descriptive statistics turn a list of values into a concise "
                "description of center, spread, shape, and unusual observations."
            ),
        ),
    ),
    summary="Descriptive statistics help you see what a dataset is saying.",
    tags=("statistics", "descriptive-statistics", "data"),
)

SAMPLING = Lesson(
    title="Sampling and Study Design",
    slug="sampling",
    prerequisites=("sets", "percentages", "basic probability"),
    objectives=(
        LearningObjective("Distinguish populations, samples, and parameters."),
        LearningObjective("Recognize sampling bias and nonresponse bias."),
        LearningObjective("Explain why random sampling supports inference."),
    ),
    sections=(
        LessonSection(
            title="Learning from part of a population",
            body=(
                "Sampling is the art of choosing data so that it can answer a "
                "question about a larger population or process."
            ),
        ),
    ),
    summary="Good inference starts with good data collection.",
    tags=("statistics", "sampling", "study-design"),
)

PROBABILITY_FOR_STATISTICS = Lesson(
    title="Probability for Statistics",
    slug="probability-for-statistics",
    prerequisites=("fractions", "probability", "random variables"),
    objectives=(
        LearningObjective("Use probability rules in statistical reasoning."),
        LearningObjective("Connect expected value and variance to data summaries."),
        LearningObjective("Recognize normal, binomial, and sampling models."),
    ),
    sections=(
        LessonSection(
            title="Uncertainty language",
            body=(
                "Probability supplies the grammar for statements about random "
                "samples, estimates, and evidence."
            ),
        ),
    ),
    summary="Statistics uses probability to describe what random data can do.",
    tags=("statistics", "probability", "distributions"),
)

SAMPLING_DISTRIBUTIONS = Lesson(
    title="Sampling Distributions",
    slug="sampling-distributions",
    prerequisites=("sampling", "probability", "descriptive statistics"),
    objectives=(
        LearningObjective("Describe how sample statistics vary from sample to sample."),
        LearningObjective("Compute and interpret standard error."),
        LearningObjective("Use the central limit theorem at an introductory level."),
    ),
    sections=(
        LessonSection(
            title="Statistics have distributions too",
            body=(
                "A statistic such as a sample mean changes from sample to sample; "
                "its long-run pattern is a sampling distribution."
            ),
        ),
    ),
    summary="Sampling distributions explain why estimates have uncertainty.",
    tags=("statistics", "sampling-distributions", "standard-error"),
)

ESTIMATION = Lesson(
    title="Estimation",
    slug="estimation",
    prerequisites=("sampling distributions", "standard error", "normal models"),
    objectives=(
        LearningObjective("Distinguish point estimates from interval estimates."),
        LearningObjective("Compute margin of error from a standard error."),
        LearningObjective("Interpret confidence intervals accurately."),
    ),
    sections=(
        LessonSection(
            title="Estimate plus uncertainty",
            body=(
                "A confidence interval reports a plausible range of parameter "
                "values based on an estimate and its sampling variability."
            ),
        ),
    ),
    summary="Estimation quantifies what the data suggest and how uncertain it is.",
    tags=("statistics", "confidence-intervals", "estimation"),
)

HYPOTHESIS_TESTS = Lesson(
    title="Hypothesis Tests",
    slug="hypothesis-tests",
    prerequisites=("estimation", "sampling distributions", "probability"),
    objectives=(
        LearningObjective("State null and alternative hypotheses."),
        LearningObjective("Compute a test statistic in simple normal settings."),
        LearningObjective("Interpret p-values without overclaiming."),
    ),
    sections=(
        LessonSection(
            title="Evidence against a baseline",
            body=(
                "A hypothesis test asks whether observed data would be unusual "
                "if a baseline claim were true."
            ),
        ),
    ),
    summary="Hypothesis tests organize evidence, uncertainty, and decisions.",
    tags=("statistics", "hypothesis-tests", "p-values"),
)

COMPARING_GROUPS = Lesson(
    title="Comparing Groups",
    slug="comparing-groups",
    prerequisites=("estimation", "hypothesis tests", "study design"),
    objectives=(
        LearningObjective("Compare two means or two proportions."),
        LearningObjective("Distinguish paired and independent samples."),
        LearningObjective("Interpret differences with uncertainty."),
    ),
    sections=(
        LessonSection(
            title="Differences are estimates too",
            body=(
                "When groups are compared, the main estimate is often a "
                "difference, and that difference has its own standard error."
            ),
        ),
    ),
    summary="Comparing groups requires design awareness and uncertainty estimates.",
    tags=("statistics", "comparing-groups", "inference"),
)

CHI_SQUARE_TESTS = Lesson(
    title="Chi-Square Tests",
    slug="chi-square-tests",
    prerequisites=("categorical data", "hypothesis tests", "tables"),
    objectives=(
        LearningObjective("Organize categorical counts in one-way or two-way tables."),
        LearningObjective("Compare observed and expected counts."),
        LearningObjective("Interpret chi-square evidence for fit or association."),
    ),
    sections=(
        LessonSection(
            title="Testing patterns in counts",
            body=(
                "Chi-square methods compare observed categorical counts with "
                "counts expected under a null model."
            ),
        ),
    ),
    summary="Chi-square tests study categorical patterns through observed counts.",
    tags=("statistics", "chi-square", "categorical-data"),
)

REGRESSION_BASICS = Lesson(
    title="Regression Basics",
    slug="regression-basics",
    prerequisites=("scatterplots", "linear functions", "descriptive statistics"),
    objectives=(
        LearningObjective("Fit and interpret a simple linear regression line."),
        LearningObjective("Use residuals to assess model fit."),
        LearningObjective("Avoid causal claims from association alone."),
    ),
    sections=(
        LessonSection(
            title="Modeling relationships",
            body=(
                "Regression describes how a response variable tends to change "
                "as an explanatory variable changes."
            ),
        ),
    ),
    summary="Regression models relationships and prediction error.",
    tags=("statistics", "regression", "correlation"),
)

STATISTICS_CUMULATIVE_REVIEW = Lesson(
    title="Statistics Cumulative Review",
    slug="statistics-cumulative-review",
    prerequisites=("statistics lessons",),
    objectives=(
        LearningObjective("Choose appropriate statistical tools for common tasks."),
        LearningObjective("Explain results in context with uncertainty."),
        LearningObjective("Recognize assumptions and limitations."),
    ),
    sections=(
        LessonSection(
            title="Putting the workflow together",
            body=(
                "Statistical thinking moves from question to data, summary, "
                "model, inference, and cautious interpretation."
            ),
        ),
    ),
    summary="A cumulative review connects the full introductory statistics workflow.",
    tags=("statistics", "review", "study-path"),
)

STATISTICS_PATH = StudyPath(
    title="Statistics",
    lessons=(
        DESCRIPTIVE_STATISTICS,
        SAMPLING,
        PROBABILITY_FOR_STATISTICS,
        SAMPLING_DISTRIBUTIONS,
        ESTIMATION,
        HYPOTHESIS_TESTS,
        COMPARING_GROUPS,
        CHI_SQUARE_TESTS,
        REGRESSION_BASICS,
        STATISTICS_CUMULATIVE_REVIEW,
    ),
)


def describe(values: npt.ArrayLike, *, sample: bool = True) -> DescriptiveStats:
    """Return descriptive statistics for numeric data.

    Set ``sample=False`` to use population variance and standard deviation.
    """

    array = _as_nonempty_array(values)
    ddof = 1 if sample and array.size > 1 else 0
    return DescriptiveStats(
        mean=float(np.mean(array)),
        median=float(np.median(array)),
        variance=float(np.var(array, ddof=ddof)),
        standard_deviation=float(np.std(array, ddof=ddof)),
        minimum=float(np.min(array)),
        maximum=float(np.max(array)),
    )


def five_number_summary(values: npt.ArrayLike) -> FiveNumberSummary:
    """Return minimum, Q1, median, Q3, and maximum."""

    array = _as_nonempty_array(values)
    q1, median, q3 = np.percentile(array, [25, 50, 75])
    return FiveNumberSummary(
        minimum=float(np.min(array)),
        q1=float(q1),
        median=float(median),
        q3=float(q3),
        maximum=float(np.max(array)),
    )


def interquartile_range(values: npt.ArrayLike) -> float:
    """Return the interquartile range ``Q3 - Q1``."""

    summary = five_number_summary(values)
    return summary.q3 - summary.q1


def outlier_fences(values: npt.ArrayLike, *, multiplier: float = 1.5) -> OutlierFences:
    """Return Tukey lower/upper fences and values outside the fences."""

    if multiplier <= 0:
        msg = "multiplier must be positive"
        raise ValueError(msg)
    array = _as_nonempty_array(values)
    summary = five_number_summary(array)
    iqr = summary.q3 - summary.q1
    lower = summary.q1 - multiplier * iqr
    upper = summary.q3 + multiplier * iqr
    outliers = tuple(float(value) for value in array if value < lower or value > upper)
    return OutlierFences(lower=float(lower), upper=float(upper), outliers=outliers)


def z_score(value: float, mean: float, standard_deviation: float) -> float:
    """Return a z-score."""

    if standard_deviation <= 0:
        msg = "standard_deviation must be positive"
        raise ValueError(msg)
    return (value - mean) / standard_deviation


def standard_error(standard_deviation: float, sample_size: int) -> float:
    """Return ``standard_deviation / sqrt(sample_size)``."""

    if sample_size <= 0:
        msg = "sample_size must be positive"
        raise ValueError(msg)
    if standard_deviation < 0:
        msg = "standard_deviation must be non-negative"
        raise ValueError(msg)
    return float(standard_deviation) / math.sqrt(sample_size)


def proportion_standard_error(proportion: float, sample_size: int) -> float:
    """Return standard error for a sample proportion."""

    _validate_probability(proportion, name="proportion")
    if sample_size <= 0:
        msg = "sample_size must be positive"
        raise ValueError(msg)
    return math.sqrt(proportion * (1 - proportion) / sample_size)


def z_critical(confidence_level: float = 0.95) -> float:
    """Return the two-sided standard-normal critical value."""

    _validate_confidence_level(confidence_level)
    return NormalDist().inv_cdf(0.5 + confidence_level / 2)


def margin_of_error(
    standard_error_value: float,
    *,
    confidence_level: float = 0.95,
) -> float:
    """Return a normal-approximation margin of error."""

    if standard_error_value < 0:
        msg = "standard_error_value must be non-negative"
        raise ValueError(msg)
    return z_critical(confidence_level) * standard_error_value


def confidence_interval_mean(
    values: npt.ArrayLike,
    *,
    confidence_level: float = 0.95,
    population_standard_deviation: float | None = None,
) -> ConfidenceInterval:
    """Return a normal-approximation confidence interval for a mean."""

    array = _as_nonempty_array(values)
    estimate = float(np.mean(array))
    if population_standard_deviation is None:
        spread = float(np.std(array, ddof=1 if array.size > 1 else 0))
    else:
        if population_standard_deviation < 0:
            msg = "population_standard_deviation must be non-negative"
            raise ValueError(msg)
        spread = population_standard_deviation
    se = standard_error(spread, int(array.size))
    moe = margin_of_error(se, confidence_level=confidence_level)
    return ConfidenceInterval(
        estimate=estimate,
        lower=estimate - moe,
        upper=estimate + moe,
        margin_of_error=moe,
        confidence_level=confidence_level,
    )


def confidence_interval_proportion(
    successes: int,
    sample_size: int,
    *,
    confidence_level: float = 0.95,
) -> ConfidenceInterval:
    """Return a normal-approximation confidence interval for a proportion."""

    if sample_size <= 0:
        msg = "sample_size must be positive"
        raise ValueError(msg)
    if successes < 0 or successes > sample_size:
        msg = "successes must be between 0 and sample_size"
        raise ValueError(msg)
    estimate = successes / sample_size
    se = proportion_standard_error(estimate, sample_size)
    moe = margin_of_error(se, confidence_level=confidence_level)
    return ConfidenceInterval(
        estimate=estimate,
        lower=max(0.0, estimate - moe),
        upper=min(1.0, estimate + moe),
        margin_of_error=moe,
        confidence_level=confidence_level,
    )


def z_test_statistic(
    estimate: float,
    null_value: float,
    standard_error_value: float,
) -> float:
    """Return ``(estimate - null_value) / standard_error``."""

    if standard_error_value <= 0:
        msg = "standard_error_value must be positive"
        raise ValueError(msg)
    return (estimate - null_value) / standard_error_value


def normal_p_value(
    statistic: float,
    *,
    alternative: Alternative = "two-sided",
) -> float:
    """Return a standard-normal p-value for a z statistic."""

    distribution = NormalDist()
    z = float(statistic)
    if alternative == "two-sided":
        return 2 * min(distribution.cdf(z), 1 - distribution.cdf(z))
    if alternative == "greater":
        return 1 - distribution.cdf(z)
    if alternative == "less":
        return distribution.cdf(z)
    msg = "alternative must be 'two-sided', 'greater', or 'less'"
    raise ValueError(msg)


def one_sample_z_test(
    estimate: float,
    null_value: float,
    standard_error_value: float,
    *,
    alternative: Alternative = "two-sided",
) -> HypothesisTestResult:
    """Return a normal-approximation z test result."""

    statistic = z_test_statistic(estimate, null_value, standard_error_value)
    p_value = normal_p_value(statistic, alternative=alternative)
    return HypothesisTestResult(
        statistic=statistic,
        p_value=p_value,
        alternative=alternative,
    )


def difference_standard_error(
    first_standard_deviation: float,
    first_sample_size: int,
    second_standard_deviation: float,
    second_sample_size: int,
) -> float:
    """Return standard error for a difference of independent means."""

    first = standard_error(first_standard_deviation, first_sample_size) ** 2
    second = standard_error(second_standard_deviation, second_sample_size) ** 2
    return math.sqrt(first + second)


def correlation(x_values: npt.ArrayLike, y_values: npt.ArrayLike) -> float:
    """Return Pearson correlation for paired numeric data."""

    x, y = _paired_arrays(x_values, y_values)
    if x.size < 2:
        msg = "at least two paired observations are required"
        raise ValueError(msg)
    x_sd = float(np.std(x, ddof=1))
    y_sd = float(np.std(y, ddof=1))
    if x_sd == 0 or y_sd == 0:
        msg = "correlation is undefined when either variable has zero variation"
        raise ValueError(msg)
    return float(np.corrcoef(x, y)[0, 1])


def simple_linear_regression(
    x_values: npt.ArrayLike,
    y_values: npt.ArrayLike,
) -> RegressionLine:
    """Return the least-squares regression line for paired data."""

    x, y = _paired_arrays(x_values, y_values)
    if x.size < 2:
        msg = "at least two paired observations are required"
        raise ValueError(msg)
    x_variance = float(np.var(x, ddof=1))
    if x_variance == 0:
        msg = "x_values must have nonzero variation"
        raise ValueError(msg)
    covariance = float(np.cov(x, y, ddof=1)[0, 1])
    slope = covariance / x_variance
    intercept = float(np.mean(y) - slope * np.mean(x))
    return RegressionLine(
        slope=slope,
        intercept=intercept,
        correlation=correlation(x, y),
    )


def predict(line: RegressionLine, x_value: float) -> float:
    """Predict ``y`` from a regression line and an ``x`` value."""

    return line.intercept + line.slope * x_value


def residuals(
    line: RegressionLine,
    x_values: npt.ArrayLike,
    y_values: npt.ArrayLike,
) -> tuple[float, ...]:
    """Return observed minus predicted values for paired data."""

    x, y = _paired_arrays(x_values, y_values)
    return tuple(
        float(observed - predict(line, float(x_value)))
        for x_value, observed in zip(x, y, strict=True)
    )


def _as_nonempty_array(values: npt.ArrayLike) -> npt.NDArray[np.float64]:
    array = np.asarray(values, dtype=float)
    if array.size == 0:
        msg = "values must not be empty"
        raise ValueError(msg)
    if not np.all(np.isfinite(array)):
        msg = "values must be finite numbers"
        raise ValueError(msg)
    return np.ravel(array).astype(float)


def _paired_arrays(
    x_values: npt.ArrayLike,
    y_values: npt.ArrayLike,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    x = _as_nonempty_array(x_values)
    y = _as_nonempty_array(y_values)
    if x.size != y.size:
        msg = "x_values and y_values must have the same length"
        raise ValueError(msg)
    return x, y


def _validate_confidence_level(confidence_level: float) -> None:
    if not 0 < confidence_level < 1:
        msg = "confidence_level must be between 0 and 1"
        raise ValueError(msg)


def _validate_probability(value: float, *, name: str) -> None:
    if not 0 <= value <= 1:
        msg = f"{name} must be between 0 and 1"
        raise ValueError(msg)


__all__ = [
    "CHI_SQUARE_TESTS",
    "COMPARING_GROUPS",
    "DESCRIPTIVE_STATISTICS",
    "ESTIMATION",
    "HYPOTHESIS_TESTS",
    "PROBABILITY_FOR_STATISTICS",
    "REGRESSION_BASICS",
    "SAMPLING",
    "SAMPLING_DISTRIBUTIONS",
    "STATISTICS_CUMULATIVE_REVIEW",
    "STATISTICS_PATH",
    "ConfidenceInterval",
    "DescriptiveStats",
    "FiveNumberSummary",
    "HypothesisTestResult",
    "OutlierFences",
    "RegressionLine",
    "confidence_interval_mean",
    "confidence_interval_proportion",
    "correlation",
    "describe",
    "difference_standard_error",
    "five_number_summary",
    "interquartile_range",
    "margin_of_error",
    "normal_p_value",
    "one_sample_z_test",
    "outlier_fences",
    "predict",
    "proportion_standard_error",
    "residuals",
    "simple_linear_regression",
    "standard_error",
    "z_critical",
    "z_score",
    "z_test_statistic",
]
