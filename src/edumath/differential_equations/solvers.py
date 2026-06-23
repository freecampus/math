"""Differential equation solvers and qualitative helpers."""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Sequence
from typing import cast

import sympy as sp

from edumath.core import parse_expression

DerivativeFunction = Callable[[float, float], float]
SystemDerivativeFunction = Callable[[float, tuple[float, ...]], Sequence[float]]
SlopeSample = tuple[float, float, float, float]
SystemState = tuple[float, tuple[float, ...]]


def euler_method(
    derivative: DerivativeFunction,
    *,
    initial_x: float,
    initial_y: float,
    step: float,
    steps: int,
) -> list[tuple[float, float]]:
    """Approximate a first-order ODE solution with Euler's method."""

    if steps < 0:
        msg = "steps must be non-negative"
        raise ValueError(msg)

    points = [(initial_x, initial_y)]
    x_value = initial_x
    y_value = initial_y
    for _ in range(steps):
        y_value = y_value + step * derivative(x_value, y_value)
        x_value = x_value + step
        points.append((x_value, y_value))
    return points


def improved_euler_method(
    derivative: DerivativeFunction,
    *,
    initial_x: float,
    initial_y: float,
    step: float,
    steps: int,
) -> list[tuple[float, float]]:
    """Approximate an ODE solution with Heun's improved Euler method."""

    if steps < 0:
        msg = "steps must be non-negative"
        raise ValueError(msg)

    points = [(initial_x, initial_y)]
    x_value = initial_x
    y_value = initial_y
    for _ in range(steps):
        first_slope = derivative(x_value, y_value)
        predicted_y = y_value + step * first_slope
        second_slope = derivative(x_value + step, predicted_y)
        y_value = y_value + step * (first_slope + second_slope) / 2
        x_value = x_value + step
        points.append((x_value, y_value))
    return points


def system_euler_method(
    derivative: SystemDerivativeFunction,
    *,
    initial_t: float,
    initial_state: Sequence[float],
    step: float,
    steps: int,
) -> list[SystemState]:
    """Approximate a first-order system with Euler's method."""

    if steps < 0:
        msg = "steps must be non-negative"
        raise ValueError(msg)

    time = initial_t
    state = tuple(float(value) for value in initial_state)
    points: list[SystemState] = [(time, state)]
    for _ in range(steps):
        rates = tuple(float(value) for value in derivative(time, state))
        if len(rates) != len(state):
            msg = "derivative must return one rate for each state component"
            raise ValueError(msg)
        state = tuple(
            value + step * rate for value, rate in zip(state, rates, strict=True)
        )
        time += step
        points.append((time, state))
    return points


def direction_field_values(
    derivative: DerivativeFunction,
    x_values: Iterable[float],
    y_values: Iterable[float],
    *,
    segment_length: float = 0.35,
) -> list[SlopeSample]:
    """Return normalized slope-field segments ``(x, y, dx, dy)``."""

    if segment_length <= 0:
        msg = "segment_length must be positive"
        raise ValueError(msg)

    samples: list[SlopeSample] = []
    for x_value in x_values:
        for y_value in y_values:
            slope = derivative(float(x_value), float(y_value))
            scale = segment_length / math.sqrt(1 + slope * slope)
            samples.append((float(x_value), float(y_value), scale, slope * scale))
    return samples


def equilibrium_points_1d(
    expression: str | sp.Expr,
    *,
    variable: str = "y",
) -> tuple[sp.Expr, ...]:
    """Solve ``f(y)=0`` for equilibria of an autonomous equation ``y'=f(y)``."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    solutions = sp.solve(sp.Eq(expr, 0), symbol)
    return tuple(cast(sp.Expr, sp.simplify(solution)) for solution in solutions)


def classify_equilibrium_1d(
    expression: str | sp.Expr,
    point: float,
    *,
    variable: str = "y",
    sample_step: float = 0.1,
) -> str:
    """Classify a one-dimensional equilibrium as stable, unstable, or semistable."""

    if sample_step <= 0:
        msg = "sample_step must be positive"
        raise ValueError(msg)

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    left = _sign(float(function(point - sample_step)))
    right = _sign(float(function(point + sample_step)))

    if left > 0 and right < 0:
        return "stable"
    if left < 0 and right > 0:
        return "unstable"
    if left == 0 and right == 0:
        return "neutral"
    return "semistable"


def _sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


__all__ = [
    "DerivativeFunction",
    "SlopeSample",
    "SystemDerivativeFunction",
    "SystemState",
    "classify_equilibrium_1d",
    "direction_field_values",
    "equilibrium_points_1d",
    "euler_method",
    "improved_euler_method",
    "system_euler_method",
]
