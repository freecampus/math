"""Trigonometry helpers."""

from __future__ import annotations

import math


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""

    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""

    return math.degrees(radians)


def coterminal_angle(degrees: float) -> float:
    """Return a coterminal angle in the interval [0, 360)."""

    return degrees % 360


__all__ = ["coterminal_angle", "degrees_to_radians", "radians_to_degrees"]
