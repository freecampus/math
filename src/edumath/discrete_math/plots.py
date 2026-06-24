"""Plotting helpers for discrete mathematics lessons."""

from __future__ import annotations

import math
from collections.abc import Hashable, Sequence
from dataclasses import dataclass, field
from typing import cast

from matplotlib.axes import Axes
from matplotlib.patches import Circle, FancyArrowPatch

from edumath.core import (
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    Segment2D,
    Viewport2D,
)
from edumath.core.plots import Drawable2D
from edumath.discrete_math.sets import venn_region_counts

Vertex = Hashable
Edge = tuple[Vertex, Vertex]


@dataclass(frozen=True)
class VennTwoSetDiagram:
    """Drawable two-set Venn diagram with region counts."""

    counts: dict[str, int]
    labels: tuple[str, str] = ("A", "B")
    style: PlotStyle = field(default_factory=lambda: PlotStyle(color="#1a73e8"))

    def draw(self, axis: Axes) -> None:
        """Draw a simple two-set Venn diagram."""

        left = Circle((-0.45, 0), 0.75, color="#1a73e8", alpha=0.22)
        right = Circle((0.45, 0), 0.75, color="#d93025", alpha=0.22)
        axis.add_patch(left)
        axis.add_patch(right)
        axis.text(-0.95, 0.75, self.labels[0], fontsize=12, weight="bold")
        axis.text(0.85, 0.75, self.labels[1], fontsize=12, weight="bold")
        axis.text(-0.75, 0, str(self.counts.get("only_a", 0)), ha="center")
        axis.text(0, 0, str(self.counts.get("both", 0)), ha="center")
        axis.text(0.75, 0, str(self.counts.get("only_b", 0)), ha="center")
        axis.text(0, -0.9, f"neither: {self.counts.get('neither', 0)}", ha="center")


@dataclass(frozen=True)
class RelationArrowDiagram:
    """Drawable relation from a domain to a codomain."""

    domain: tuple[Hashable, ...]
    codomain: tuple[Hashable, ...]
    pairs: tuple[tuple[Hashable, Hashable], ...]

    def draw(self, axis: Axes) -> None:
        """Draw domain/codomain points and arrows for ordered pairs."""

        left_positions = _vertical_positions(self.domain, x_value=-1.0)
        right_positions = _vertical_positions(self.codomain, x_value=1.0)
        for value, (x_coord, y_coord) in left_positions.items():
            axis.plot([x_coord], [y_coord], marker="o", color="#1a73e8")
            axis.text(x_coord - 0.08, y_coord, str(value), ha="right", va="center")
        for value, (x_coord, y_coord) in right_positions.items():
            axis.plot([x_coord], [y_coord], marker="o", color="#d93025")
            axis.text(x_coord + 0.08, y_coord, str(value), ha="left", va="center")
        for left, right in self.pairs:
            if left not in left_positions or right not in right_positions:
                continue
            start = left_positions[left]
            end = right_positions[right]
            arrow = FancyArrowPatch(
                start, end, arrowstyle="->", mutation_scale=10, alpha=0.7
            )
            axis.add_patch(arrow)


@dataclass(frozen=True)
class FiniteGraph2D:
    """Drawable finite graph from vertices and edges."""

    vertices: tuple[Vertex, ...]
    edges: tuple[Edge, ...]
    directed: bool = False
    style: PlotStyle = field(default_factory=lambda: PlotStyle(color="#1a73e8"))

    def draw(self, axis: Axes) -> None:
        """Draw a small graph with circular vertex layout."""

        positions = _circle_positions(self.vertices)
        for left, right in self.edges:
            if left not in positions or right not in positions:
                continue
            start = positions[left]
            end = positions[right]
            if self.directed:
                axis.add_patch(
                    FancyArrowPatch(
                        start, end, arrowstyle="->", mutation_scale=12, alpha=0.75
                    )
                )
            else:
                axis.plot(
                    [start[0], end[0]],
                    [start[1], end[1]],
                    color="#5f6368",
                    linewidth=1.6,
                )
        for vertex, (x_coord, y_coord) in positions.items():
            axis.plot([x_coord], [y_coord], marker="o", color=self.style.color)
            axis.text(x_coord, y_coord + 0.12, str(vertex), ha="center")


def venn_two_set_scene(
    a: Sequence[Hashable],
    b: Sequence[Hashable],
    *,
    universe: Sequence[Hashable] | None = None,
) -> PlotScene2D:
    """Create a two-set Venn diagram scene."""

    counts = venn_region_counts(a, b, universe=universe)
    return PlotScene2D(
        elements=(VennTwoSetDiagram(counts),),
        viewport=Viewport2D(x=PlotRange(-1.6, 1.6), y=PlotRange(-1.2, 1.2)),
        title="Two-set Venn diagram",
        show_axes=False,
        show_grid=False,
    )


def relation_arrow_scene(
    domain: Sequence[Hashable],
    codomain: Sequence[Hashable],
    pairs: Sequence[tuple[Hashable, Hashable]],
) -> PlotScene2D:
    """Create an arrow diagram scene for a finite relation."""

    return PlotScene2D(
        elements=(RelationArrowDiagram(tuple(domain), tuple(codomain), tuple(pairs)),),
        viewport=Viewport2D(x=PlotRange(-1.4, 1.4), y=PlotRange(-1.4, 1.4)),
        title="Relation arrow diagram",
        show_axes=False,
        show_grid=False,
    )


def sequence_points_scene(terms: Sequence[float]) -> PlotScene2D:
    """Create a point plot for a finite sequence."""

    points = tuple(
        Point2D(index + 1, value, style=PlotStyle(color="#1a73e8", marker="o"))
        for index, value in enumerate(terms)
    )
    segments = tuple(
        Segment2D(points[index], points[index + 1], style=PlotStyle(color="#5f6368"))
        for index in range(len(points) - 1)
    )
    y_min = min(terms) - 1 if terms else -1
    y_max = max(terms) + 1 if terms else 1
    return PlotScene2D(
        elements=cast(tuple[Drawable2D, ...], (*segments, *points)),
        viewport=Viewport2D(
            x=PlotRange(0, max(2, len(terms) + 1)), y=PlotRange(y_min, y_max)
        ),
        title="Sequence terms",
    )


def finite_graph_scene(
    vertices: Sequence[Vertex],
    edges: Sequence[Edge],
    *,
    directed: bool = False,
) -> PlotScene2D:
    """Create a finite graph scene."""

    return PlotScene2D(
        elements=(FiniteGraph2D(tuple(vertices), tuple(edges), directed=directed),),
        viewport=Viewport2D(x=PlotRange(-1.5, 1.5), y=PlotRange(-1.5, 1.5)),
        title="Finite graph",
        show_axes=False,
        show_grid=False,
        equal_aspect=True,
    )


def _circle_positions(vertices: Sequence[Vertex]) -> dict[Vertex, tuple[float, float]]:
    if not vertices:
        return {}
    return {
        vertex: (
            math.cos(2 * math.pi * index / len(vertices)),
            math.sin(2 * math.pi * index / len(vertices)),
        )
        for index, vertex in enumerate(vertices)
    }


def _vertical_positions(
    values: Sequence[Hashable],
    *,
    x_value: float,
) -> dict[Hashable, tuple[float, float]]:
    if not values:
        return {}
    if len(values) == 1:
        return {values[0]: (x_value, 0.0)}
    return {
        value: (x_value, 1 - 2 * index / (len(values) - 1))
        for index, value in enumerate(values)
    }


__all__ = [
    "Edge",
    "FiniteGraph2D",
    "RelationArrowDiagram",
    "VennTwoSetDiagram",
    "Vertex",
    "finite_graph_scene",
    "relation_arrow_scene",
    "sequence_points_scene",
    "venn_two_set_scene",
]
