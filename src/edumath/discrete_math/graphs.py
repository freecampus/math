"""Tiny finite graph helpers for lessons."""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable, Sequence
from itertools import pairwise

Vertex = Hashable
Edge = tuple[Vertex, Vertex]


def neighbors(
    vertices: Iterable[Vertex],
    edges: Iterable[Edge],
    vertex: Vertex,
    *,
    directed: bool = False,
) -> set[Vertex]:
    """Return neighbors reachable from ``vertex``."""

    vertex_set = set(vertices)
    if vertex not in vertex_set:
        msg = "vertex must be in vertices"
        raise ValueError(msg)
    result: set[Vertex] = set()
    for left, right in edges:
        if left == vertex:
            result.add(right)
        if not directed and right == vertex:
            result.add(left)
    return result


def degree(
    vertices: Iterable[Vertex],
    edges: Iterable[Edge],
    vertex: Vertex,
    *,
    directed: bool = False,
) -> int:
    """Return degree for an undirected graph or out-degree for a directed graph."""

    vertex_set = set(vertices)
    if vertex not in vertex_set:
        msg = "vertex must be in vertices"
        raise ValueError(msg)
    total = 0
    for left, right in edges:
        if directed:
            if left == vertex:
                total += 1
        else:
            if left == vertex and right == vertex:
                total += 2
            elif left == vertex or right == vertex:
                total += 1
    return total


def in_degree(vertices: Iterable[Vertex], edges: Iterable[Edge], vertex: Vertex) -> int:
    """Return directed in-degree."""

    vertex_set = set(vertices)
    if vertex not in vertex_set:
        msg = "vertex must be in vertices"
        raise ValueError(msg)
    return sum(1 for _, right in edges if right == vertex)


def out_degree(
    vertices: Iterable[Vertex], edges: Iterable[Edge], vertex: Vertex
) -> int:
    """Return directed out-degree."""

    return degree(vertices, edges, vertex, directed=True)


def degree_sequence(
    vertices: Iterable[Vertex],
    edges: Iterable[Edge],
    *,
    directed: bool = False,
) -> tuple[int, ...]:
    """Return degrees sorted from largest to smallest."""

    vertex_tuple = tuple(vertices)
    return tuple(
        sorted(
            (
                degree(vertex_tuple, edges, vertex, directed=directed)
                for vertex in vertex_tuple
            ),
            reverse=True,
        )
    )


def is_path(
    vertices: Iterable[Vertex],
    edges: Iterable[Edge],
    walk: Sequence[Vertex],
    *,
    directed: bool = False,
) -> bool:
    """Return whether a sequence of vertices is a path with no repeats."""

    vertex_set = set(vertices)
    if any(vertex not in vertex_set for vertex in walk):
        return False
    if len(set(walk)) != len(walk):
        return False
    edge_set = set(edges)
    for left, right in pairwise(walk):
        if (left, right) in edge_set:
            continue
        if not directed and (right, left) in edge_set:
            continue
        return False
    return True


def is_connected(vertices: Iterable[Vertex], edges: Iterable[Edge]) -> bool:
    """Return whether every vertex is reachable in an undirected graph."""

    vertex_tuple = tuple(vertices)
    if not vertex_tuple:
        return True
    seen: set[Vertex] = {vertex_tuple[0]}
    queue: deque[Vertex] = deque([vertex_tuple[0]])
    while queue:
        current = queue.popleft()
        for neighbor in neighbors(vertex_tuple, edges, current):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(set(vertex_tuple))


__all__ = [
    "Edge",
    "Vertex",
    "degree",
    "degree_sequence",
    "in_degree",
    "is_connected",
    "is_path",
    "neighbors",
    "out_degree",
]
