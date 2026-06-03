import math

import matplotlib.pyplot as plt

from edumath.trigonometry.plots import (
    plot_unit_circle,
    unit_circle_point,
    unit_circle_widget,
)


def test_unit_circle_point_returns_sine_and_cosine() -> None:
    point = unit_circle_point(30)

    assert math.isclose(point.cosine, math.sqrt(3) / 2)
    assert math.isclose(point.sine, 0.5)


def test_plot_unit_circle_returns_matplotlib_objects() -> None:
    figure, axis = plot_unit_circle(45)

    assert figure is axis.figure
    assert axis.get_aspect() == 1.0
    assert axis.get_title() == "Angle: 45 deg"

    plt.close(figure)


def test_unit_circle_widget_can_be_constructed_without_displaying() -> None:
    widget = unit_circle_widget(initial_angle=60)

    assert widget.controls is not None
    assert widget.output is not None
