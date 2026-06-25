"""Deterministic exercise builders for trigonometry lessons."""

from __future__ import annotations

from random import Random

from edumath.core import Exercise
from edumath.trigonometry.concepts import (
    coterminal_angle,
    degrees_to_radians,
    quadrant,
    reference_angle_degrees,
    special_angle_values,
)
from edumath.trigonometry.validators import validate_angle_answer, validate_keyword


def angle_conversion_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a degrees-to-radians exercise."""

    rng = Random(seed)
    angle = rng.choice((30, 45, 60, 90, 180, 270, 360))
    expected = degrees_to_radians(angle)
    return Exercise(
        prompt=f"Convert {angle} degrees to radians. Give a decimal approximation.",
        expected=expected,
        validator=lambda received: validate_angle_answer(received, expected),
        hint="Multiply degrees by pi/180.",
        explanation="Degrees to radians uses radians = degrees*pi/180.",
        tags=("trigonometry", "radians", "degrees"),
        exercise_id="trigonometry-angle-conversion",
        answer_type="numeric",
    )


def reference_angle_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a reference-angle exercise."""

    rng = Random(seed)
    angle = rng.choice((120, 135, 210, 225, 300, 330))
    expected = reference_angle_degrees(angle)
    return Exercise(
        prompt=f"Find the reference angle for {angle} degrees.",
        expected=expected,
        validator=lambda received: validate_angle_answer(received, expected),
        hint="Move to the nearest x-axis after locating the quadrant.",
        explanation="A reference angle is the acute angle to the x-axis.",
        tags=("trigonometry", "reference-angle"),
        exercise_id="trigonometry-reference-angle",
        answer_type="numeric",
    )


def quadrant_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a quadrant-identification exercise."""

    rng = Random(seed)
    angle = rng.choice((30, 120, 210, 300))
    expected = quadrant(angle)
    return Exercise(
        prompt=f"Which quadrant contains {angle} degrees?",
        expected=expected,
        validator=lambda received: validate_keyword(received, expected),
        hint="Reduce to 0-360 degrees and locate the angle on the unit circle.",
        explanation="Quadrants are numbered counterclockwise from the positive x-axis.",
        tags=("trigonometry", "quadrants"),
        exercise_id="trigonometry-quadrant",
        answer_type="multiple_choice",
    )


def special_angle_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a special-angle sine exercise."""

    rng = Random(seed)
    angle = rng.choice((0, 30, 45, 60, 90, 180, 270))
    expected = special_angle_values(angle).sine
    return Exercise(
        prompt=f"Find the exact value of sin({angle} degrees).",
        expected=expected,
        validator=lambda received: validate_keyword(received, expected),
        hint="Use the special-angle table or unit circle.",
        explanation="Special angles have exact values that are worth memorizing.",
        tags=("trigonometry", "special-angles", "sine"),
        exercise_id="trigonometry-special-angle",
        answer_type="exact",
    )


def coterminal_angle_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a coterminal-angle exercise."""

    rng = Random(seed)
    angle = rng.choice((-450, -30, 390, 765))
    expected = coterminal_angle(angle)
    return Exercise(
        prompt=(
            f"Find the coterminal angle between 0 and 360 degrees for {angle} degrees."
        ),
        expected=expected,
        validator=lambda received: validate_angle_answer(received, expected),
        hint="Add or subtract 360 degrees until the angle is in [0,360).",
        explanation="Coterminal angles differ by full turns.",
        tags=("trigonometry", "coterminal-angles"),
        exercise_id="trigonometry-coterminal-angle",
        answer_type="numeric",
    )


__all__ = [
    "angle_conversion_exercise",
    "coterminal_angle_exercise",
    "quadrant_exercise",
    "reference_angle_exercise",
    "special_angle_exercise",
]
