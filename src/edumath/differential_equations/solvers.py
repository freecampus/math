"""Differential equation helpers."""

from __future__ import annotations

from collections.abc import Callable

DerivativeFunction = Callable[[float, float], float]


def euler_method(
    derivative: DerivativeFunction,
    *,
    initial_x: float,
    initial_y: float,
    step: float,
    steps: int,
) -> list[tuple[float, float]]:
    """Approximate an ODE solution with Euler's method."""

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


__all__ = ["DerivativeFunction", "euler_method"]
