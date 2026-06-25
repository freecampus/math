import math

from edumath.trigonometry import (
    TRIGONOMETRY_PATH,
    angle_conversion_exercise,
    coterminal_angle,
    coterminal_angle_exercise,
    degrees_to_radians,
    quadrant,
    quadrant_exercise,
    radians_to_degrees,
    reference_angle_degrees,
    reference_angle_exercise,
    sine_cosine_tangent,
    special_angle_exercise,
    special_angle_values,
    trig_signs,
    validate_angle_answer,
    validate_keyword,
)


def test_trigonometry_path_has_expected_lessons() -> None:
    assert TRIGONOMETRY_PATH.slugs() == [
        "radians-and-degrees",
        "unit-circle",
        "sine-cosine",
        "trig-functions-and-graphs",
        "identities",
        "trig-equations",
        "applications",
    ]


def test_angle_helpers() -> None:
    assert math.isclose(degrees_to_radians(180), math.pi)
    assert math.isclose(radians_to_degrees(math.pi / 2), 90)
    assert coterminal_angle(-30) == 330
    assert reference_angle_degrees(225) == 45
    assert quadrant(120) == "II"
    assert quadrant(270) == "negative y-axis"
    assert trig_signs(210) == {"sine": "-", "cosine": "-", "tangent": "+"}


def test_special_values_and_numeric_trig_values() -> None:
    values = special_angle_values(30)
    assert values.sine == "1/2"
    assert values.cosine == "sqrt(3)/2"
    sine, cosine, tangent = sine_cosine_tangent(45)
    assert math.isclose(sine, math.sqrt(2) / 2)
    assert math.isclose(cosine, math.sqrt(2) / 2)
    assert tangent is not None and math.isclose(tangent, 1)
    assert sine_cosine_tangent(90)[2] is None


def test_validators() -> None:
    assert validate_angle_answer(45, 45).correct
    assert validate_keyword("ii", "II").correct
    assert not validate_angle_answer(30, 45).correct


def test_exercise_builders_accept_expected_answers() -> None:
    exercises = (
        angle_conversion_exercise(seed=1),
        reference_angle_exercise(seed=1),
        quadrant_exercise(seed=1),
        special_angle_exercise(seed=1),
        coterminal_angle_exercise(seed=1),
    )
    for exercise in exercises:
        assert exercise.check(exercise.expected).correct
