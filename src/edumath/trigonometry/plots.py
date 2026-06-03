"""Trigonometry plots and notebook widgets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, cast

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display as ipython_display
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle


class UnitCirclePoint(NamedTuple):
    """Point and component values for an angle on the unit circle."""

    theta_degrees: float
    theta_radians: float
    cosine: float
    sine: float


@dataclass(frozen=True)
class UnitCircleWidget:
    """Container returned by :func:`unit_circle_widget`."""

    controls: widgets.Widget
    output: widgets.Output

    def display(self) -> None:
        """Display the widget in a notebook frontend."""

        _display(self.controls)
        _display(self.output)


def unit_circle_point(theta_degrees: float) -> UnitCirclePoint:
    """Return sine and cosine coordinates for an angle in degrees."""

    theta_radians = float(np.deg2rad(theta_degrees))
    return UnitCirclePoint(
        theta_degrees=theta_degrees,
        theta_radians=theta_radians,
        cosine=float(np.cos(theta_radians)),
        sine=float(np.sin(theta_radians)),
    )


def plot_unit_circle(
    theta_degrees: float,
    *,
    axis: Axes | None = None,
    show: bool = False,
) -> tuple[Figure, Axes]:
    """Plot a unit-circle angle and its sine/cosine components.

    Parameters
    ----------
    theta_degrees:
        Angle in degrees.
    axis:
        Optional Matplotlib axis to draw into.
    show:
        If true, call ``plt.show()`` after drawing. Keep false for tests,
        library code, and Quarto/Jupyter cells that handle figure display.
    """

    point = unit_circle_point(theta_degrees)

    if axis is None:
        figure, axis = plt.subplots(figsize=(7, 7), constrained_layout=True)
    else:
        figure = cast(Figure, axis.figure)

    circle = Circle(
        (0, 0),
        1,
        color="#9aa0a6",
        fill=False,
        linewidth=2,
        linestyle="--",
    )
    axis.add_patch(circle)

    axis.axhline(0, color="#202124", linewidth=1)
    axis.axvline(0, color="#202124", linewidth=1)
    axis.plot(
        [0, point.cosine],
        [0, point.sine],
        color="#202124",
        marker="o",
        linewidth=2,
        label="radius",
    )
    axis.plot(
        [point.cosine, point.cosine],
        [0, point.sine],
        color="#1a73e8",
        linewidth=3,
        label=f"sin(theta) = {point.sine:.2f}",
    )
    axis.plot(
        [0, point.cosine],
        [0, 0],
        color="#d93025",
        linewidth=3,
        label=f"cos(theta) = {point.cosine:.2f}",
    )

    axis.set_xlim(-1.2, 1.2)
    axis.set_ylim(-1.2, 1.2)
    axis.set_aspect("equal")
    axis.grid(True, alpha=0.3)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_title(f"Angle: {point.theta_degrees:g} deg")
    axis.legend(loc="upper right")

    if show:
        plt.show()

    return figure, axis


def unit_circle_widget(
    *,
    initial_angle: int = 45,
    min_angle: int = 0,
    max_angle: int = 360,
    step: int = 1,
) -> UnitCircleWidget:
    """Return linked angle controls and a live unit-circle plot output."""

    angle_slider = widgets.IntSlider(
        min=min_angle,
        max=max_angle,
        step=step,
        value=initial_angle,
        description="Angle",
        continuous_update=True,
    )
    angle_text = widgets.IntText(
        value=initial_angle,
        description="Degrees:",
        continuous_update=False,
        layout=widgets.Layout(width="160px"),
    )

    widgets.jslink((angle_slider, "value"), (angle_text, "value"))

    controls = widgets.HBox([angle_slider, angle_text])
    output = widgets.interactive_output(
        lambda theta_degrees: plot_unit_circle(
            theta_degrees,
            show=True,
        ),
        {"theta_degrees": angle_slider},
    )

    return UnitCircleWidget(controls=controls, output=output)


def display_unit_circle_widget(**kwargs: int) -> UnitCircleWidget:
    """Create and display the unit-circle widget in a notebook frontend."""

    widget = unit_circle_widget(**kwargs)
    widget.display()
    return widget


def _display(value: object) -> None:
    ipython_display(value)  # type: ignore[no-untyped-call]


__all__ = [
    "UnitCirclePoint",
    "UnitCircleWidget",
    "display_unit_circle_widget",
    "plot_unit_circle",
    "unit_circle_point",
    "unit_circle_widget",
]
