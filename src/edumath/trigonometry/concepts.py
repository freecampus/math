"""Trigonometry concepts and small computational helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath


@dataclass(frozen=True)
class ExactTrigValues:
    """Exact sine, cosine, and tangent values as display strings."""

    sine: str
    cosine: str
    tangent: str


RADIANS_AND_DEGREES = Lesson(
    title="Radians and Degrees",
    slug="radians-and-degrees",
    prerequisites=("fractions", "circles", "proportions"),
    objectives=(
        LearningObjective("Convert angles between degrees and radians."),
        LearningObjective("Explain why one full turn is 360 degrees or 2π radians."),
        LearningObjective("Find coterminal and reference angles."),
    ),
    sections=(
        LessonSection(
            title="Two angle languages",
            body=(
                "Degrees divide a turn into 360 parts; radians measure angle "
                "by arc length over radius."
            ),
        ),
    ),
    summary="Radians and degrees are two ways to measure the same rotation.",
    tags=("trigonometry", "angles", "radians", "degrees"),
)

UNIT_CIRCLE = Lesson(
    title="The Unit Circle",
    slug="unit-circle",
    prerequisites=("coordinate plane", "circles", "signed numbers"),
    objectives=(
        LearningObjective("Read sine and cosine as coordinates on the unit circle."),
        LearningObjective("Use quadrants to decide signs of trigonometric values."),
        LearningObjective("Use reference angles to find related unit-circle points."),
    ),
    sections=(
        LessonSection(
            title="Coordinates from rotation",
            body="An angle on the unit circle lands at the point (cos θ, sin θ).",
        ),
    ),
    summary="The unit circle turns trigonometry into coordinate geometry.",
    tags=("trigonometry", "unit-circle", "sine", "cosine"),
)

SINE_COSINE = Lesson(
    title="Sine and Cosine",
    slug="sine-cosine",
    prerequisites=("unit circle", "coordinates", "right triangles"),
    objectives=(
        LearningObjective(
            "Interpret sine as vertical coordinate and cosine as horizontal coordinate."
        ),
        LearningObjective("Compute common sine and cosine values."),
        LearningObjective("Connect unit-circle values to right-triangle ratios."),
    ),
    sections=(
        LessonSection(
            title="Coordinates and ratios",
            body=(
                "Sine and cosine describe both unit-circle coordinates and "
                "right-triangle side ratios."
            ),
        ),
    ),
    summary="Sine and cosine are the two core trigonometric functions.",
    tags=("trigonometry", "sine", "cosine"),
)

TRIG_FUNCTIONS_AND_GRAPHS = Lesson(
    title="Trigonometric Functions and Graphs",
    slug="trig-functions-and-graphs",
    prerequisites=("functions", "unit circle", "graphing"),
    objectives=(
        LearningObjective("Describe amplitude, period, midline, and phase shift."),
        LearningObjective("Sketch basic sine and cosine graphs."),
        LearningObjective("Interpret transformations of trigonometric graphs."),
    ),
    sections=(
        LessonSection(
            title="Circular motion becomes a wave",
            body=(
                "As an angle rotates around the unit circle, sine and cosine "
                "coordinates trace repeating graphs."
            ),
        ),
    ),
    summary="Trig graphs show repeating behavior from circular motion.",
    tags=("trigonometry", "graphs", "periodic-functions"),
)

IDENTITIES = Lesson(
    title="Trigonometric Identities",
    slug="identities",
    prerequisites=("algebra", "sine", "cosine", "unit circle"),
    objectives=(
        LearningObjective("Use the Pythagorean identity."),
        LearningObjective("Rewrite tangent, secant, cosecant, and cotangent."),
        LearningObjective("Verify simple identities step by step."),
    ),
    sections=(
        LessonSection(
            title="Always-true trig equations",
            body=(
                "An identity is an equation that is true for all allowed angle values."
            ),
        ),
    ),
    summary="Trig identities let us rewrite expressions without changing their value.",
    tags=("trigonometry", "identities", "algebra"),
)

TRIG_EQUATIONS = Lesson(
    title="Trigonometric Equations",
    slug="trig-equations",
    prerequisites=("unit circle", "inverse functions", "algebra"),
    objectives=(
        LearningObjective("Solve basic sine, cosine, and tangent equations."),
        LearningObjective("Find all solutions in a requested interval."),
        LearningObjective("Use periodicity to describe infinitely many solutions."),
    ),
    sections=(
        LessonSection(
            title="Equations with repeating answers",
            body=(
                "Trig equations often have more than one solution because "
                "trig functions repeat."
            ),
        ),
    ),
    summary=(
        "Solving trig equations means combining algebra, unit-circle values, "
        "and periodicity."
    ),
    tags=("trigonometry", "equations", "unit-circle"),
)

APPLICATIONS = Lesson(
    title="Applications of Trigonometry",
    slug="applications",
    prerequisites=("right triangles", "sine", "cosine", "tangent"),
    objectives=(
        LearningObjective("Use trig ratios to solve right-triangle problems."),
        LearningObjective("Model height, distance, and angle-of-elevation problems."),
        LearningObjective("Connect sinusoidal functions to periodic phenomena."),
    ),
    sections=(
        LessonSection(
            title="Angles in real problems",
            body=(
                "Trigonometry connects angles to distances, heights, waves, "
                "and circular motion."
            ),
        ),
    ),
    summary="Trigonometry turns angle information into useful measurements.",
    tags=("trigonometry", "applications", "right-triangles"),
)

TRIGONOMETRY_PATH = StudyPath(
    title="Trigonometry",
    lessons=(
        RADIANS_AND_DEGREES,
        UNIT_CIRCLE,
        SINE_COSINE,
        TRIG_FUNCTIONS_AND_GRAPHS,
        IDENTITIES,
        TRIG_EQUATIONS,
        APPLICATIONS,
    ),
)

SPECIAL_ANGLE_VALUES: dict[int, ExactTrigValues] = {
    0: ExactTrigValues(sine="0", cosine="1", tangent="0"),
    30: ExactTrigValues(sine="1/2", cosine="sqrt(3)/2", tangent="sqrt(3)/3"),
    45: ExactTrigValues(sine="sqrt(2)/2", cosine="sqrt(2)/2", tangent="1"),
    60: ExactTrigValues(sine="sqrt(3)/2", cosine="1/2", tangent="sqrt(3)"),
    90: ExactTrigValues(sine="1", cosine="0", tangent="undefined"),
    180: ExactTrigValues(sine="0", cosine="-1", tangent="0"),
    270: ExactTrigValues(sine="-1", cosine="0", tangent="undefined"),
    360: ExactTrigValues(sine="0", cosine="1", tangent="0"),
}


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""

    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""

    return math.degrees(radians)


def coterminal_angle(degrees: float) -> float:
    """Return a coterminal angle in the interval [0, 360)."""

    return degrees % 360


def reference_angle_degrees(degrees: float) -> float:
    """Return the acute reference angle for a degree measure."""

    angle = coterminal_angle(degrees)
    if angle <= 90:
        return angle
    if angle <= 180:
        return 180 - angle
    if angle <= 270:
        return angle - 180
    return 360 - angle


def quadrant(degrees: float) -> str:
    """Return the quadrant or axis location for an angle in degrees."""

    angle = coterminal_angle(degrees)
    if angle == 0:
        return "positive x-axis"
    if angle == 90:
        return "positive y-axis"
    if angle == 180:
        return "negative x-axis"
    if angle == 270:
        return "negative y-axis"
    if 0 < angle < 90:
        return "I"
    if 90 < angle < 180:
        return "II"
    if 180 < angle < 270:
        return "III"
    return "IV"


def trig_signs(degrees: float) -> dict[str, str]:
    """Return signs of sine, cosine, and tangent for an angle."""

    location = quadrant(degrees)
    if location == "I":
        return {"sine": "+", "cosine": "+", "tangent": "+"}
    if location == "II":
        return {"sine": "+", "cosine": "-", "tangent": "-"}
    if location == "III":
        return {"sine": "-", "cosine": "-", "tangent": "+"}
    if location == "IV":
        return {"sine": "-", "cosine": "+", "tangent": "-"}
    if "x-axis" in location:
        return {
            "sine": "0",
            "cosine": "+" if "positive" in location else "-",
            "tangent": "0",
        }
    return {
        "sine": "+" if "positive" in location else "-",
        "cosine": "0",
        "tangent": "undefined",
    }


def special_angle_values(degrees: int) -> ExactTrigValues:
    """Return exact values for common unit-circle angles."""

    angle = int(coterminal_angle(degrees))
    if angle not in SPECIAL_ANGLE_VALUES:
        msg = f"{degrees} degrees is not in the built-in special-angle table"
        raise ValueError(msg)
    return SPECIAL_ANGLE_VALUES[angle]


def sine_cosine_tangent(degrees: float) -> tuple[float, float, float | None]:
    """Return numeric sine, cosine, and tangent for an angle in degrees."""

    radians = degrees_to_radians(degrees)
    sine = math.sin(radians)
    cosine = math.cos(radians)
    if math.isclose(cosine, 0.0, abs_tol=1e-12):
        tangent = None
    else:
        tangent = math.tan(radians)
    return sine, cosine, tangent


__all__ = [
    "APPLICATIONS",
    "IDENTITIES",
    "RADIANS_AND_DEGREES",
    "SINE_COSINE",
    "SPECIAL_ANGLE_VALUES",
    "TRIGONOMETRY_PATH",
    "TRIG_EQUATIONS",
    "TRIG_FUNCTIONS_AND_GRAPHS",
    "UNIT_CIRCLE",
    "ExactTrigValues",
    "coterminal_angle",
    "degrees_to_radians",
    "quadrant",
    "radians_to_degrees",
    "reference_angle_degrees",
    "sine_cosine_tangent",
    "special_angle_values",
    "trig_signs",
]
