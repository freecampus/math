import matplotlib.pyplot as plt
import numpy as np

from edumath.core import (
    ExplicitFunction2D,
    ParametricCurve2D,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    PolarCurve2D,
    Segment2D,
    Viewport2D,
)


def test_explicit_function_samples_y_values() -> None:
    graph = ExplicitFunction2D("x**2", domain=PlotRange(-1, 1, 3))

    curve = graph.sample()

    assert curve.x.tolist() == [-1.0, 0.0, 1.0]
    assert curve.y.tolist() == [1.0, 0.0, 1.0]


def test_parametric_curve_samples_xy_values() -> None:
    curve = ParametricCurve2D(
        "cos(t)",
        "sin(t)",
        domain=PlotRange(0, float(np.pi / 2), 3),
    ).sample()

    assert round(float(curve.x[0]), 6) == 1.0
    assert round(float(curve.y[-1]), 6) == 1.0


def test_polar_curve_converts_to_cartesian_values() -> None:
    curve = PolarCurve2D("1", domain=PlotRange(0, float(np.pi / 2), 3)).sample()

    assert round(float(curve.x[0]), 6) == 1.0
    assert round(float(curve.y[-1]), 6) == 1.0


def test_plot_scene_renders_elements() -> None:
    scene = PlotScene2D(
        elements=(
            ExplicitFunction2D(
                "x",
                domain=PlotRange(-1, 1, 3),
                style=PlotStyle(label="line"),
            ),
            Segment2D(Point2D(0, 0), Point2D(1, 1)),
        ),
        viewport=Viewport2D(x=PlotRange(-2, 2), y=PlotRange(-2, 2)),
        title="Example",
    )

    figure, axis = scene.render()

    assert figure is axis.figure
    assert axis.get_title() == "Example"

    plt.close(figure)
