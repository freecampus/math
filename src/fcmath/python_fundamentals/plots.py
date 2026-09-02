"""Matplotlib helpers for introductory Python plotting."""

from __future__ import annotations

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def plot_values(
    values: npt.ArrayLike,
    *,
    axis: Axes | None = None,
    title: str = "Values",
) -> tuple[Figure, Axes]:
    """Plot a sequence of numeric values as a line chart."""

    array = np.asarray(values, dtype=float)
    x_values = np.arange(len(array), dtype=float)

    if axis is None:
        figure, axis = plt.subplots(figsize=(7, 4), constrained_layout=True)
    else:
        figure = cast(Figure, axis.figure)

    axis.plot(x_values, array, marker="o", color="#1a73e8")
    axis.set_title(title)
    axis.set_xlabel("index")
    axis.set_ylabel("value")
    axis.grid(True, alpha=0.28)
    return figure, axis


def scatter_values(
    x_values: npt.ArrayLike,
    y_values: npt.ArrayLike,
    *,
    axis: Axes | None = None,
    title: str = "Scatter plot",
) -> tuple[Figure, Axes]:
    """Plot paired numeric values as a scatter plot."""

    x_array = np.asarray(x_values, dtype=float)
    y_array = np.asarray(y_values, dtype=float)

    if axis is None:
        figure, axis = plt.subplots(figsize=(7, 4), constrained_layout=True)
    else:
        figure = cast(Figure, axis.figure)

    axis.scatter(x_array, y_array, color="#d93025")
    axis.set_title(title)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(True, alpha=0.28)
    return figure, axis
