import matplotlib.pyplot as plt

from edumath.discrete_math import (
    DISCRETE_MATH_PATH,
    and_,
    cartesian_product,
    compose_relations,
    degree,
    degree_sequence,
    discrete_math_diagnostic_quiz,
    domain,
    finite_graph_scene,
    graph_degree_exercise,
    graph_degree_sequence_exercise,
    iff,
    implies,
    induction_step_exercise,
    is_connected,
    is_equivalent,
    is_function,
    is_path,
    is_reflexive,
    is_symmetric,
    is_tautology,
    is_transitive,
    neighbors,
    or_,
    power_set,
    relation_arrow_scene,
    relation_classification_exercise,
    sequence_next_term_exercise,
    sequence_points_scene,
    set_operation_exercise,
    set_operation_table,
    truth_table,
    truth_table_exercise,
    truth_table_rows,
    validate_set_answer,
    validate_truth_value,
    venn_region_counts,
    venn_two_set_scene,
    xor,
)


def test_discrete_math_path_has_expected_lessons() -> None:
    assert DISCRETE_MATH_PATH.slugs() == [
        "logic",
        "sets",
        "functions-relations",
        "sequences",
        "induction",
        "graphs",
    ]


def test_logic_helpers() -> None:
    rows = truth_table(("p", "q"), implies)
    assert len(rows) == 4
    assert rows[2]["result"] is False
    assert and_(True, True)
    assert or_(False, True)
    assert xor(True, False)
    assert iff(True, True)
    assert is_equivalent(lambda p: p, lambda p: not (not p), ("p",))
    assert is_tautology(truth_table_rows(("p",), "p | ~p"))


def test_set_helpers_and_validators() -> None:
    table = set_operation_table({1, 2, 3}, {3, 4})
    assert table["union"] == {1, 2, 3, 4}
    assert table["intersection"] == {3}
    assert power_set({1, 2}) == (
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    )
    assert cartesian_product({1, 2}, {"a"}) in (
        ((1, "a"), (2, "a")),
        ((2, "a"), (1, "a")),
    )
    assert venn_region_counts({1, 2}, {2, 3}, universe={1, 2, 3, 4}) == {
        "only_a": 1,
        "only_b": 1,
        "both": 1,
        "neither": 1,
    }
    assert validate_set_answer("{1,2,3}", {1, 2, 3}).correct
    assert validate_truth_value("true", True).correct


def test_relation_helpers() -> None:
    pairs = {(1, 2), (2, 3)}
    assert domain(pairs) == {1, 2}
    assert is_function(pairs)
    assert not is_function({(1, 2), (1, 3)})
    equality = {(1, 1), (2, 2)}
    assert is_reflexive(equality, {1, 2})
    assert is_symmetric(equality)
    assert is_transitive(equality)
    assert compose_relations({(1, 2)}, {(2, 3)}) == {(1, 3)}


def test_graph_helpers() -> None:
    vertices = ("A", "B", "C", "D")
    edges = (("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"))
    assert degree(vertices, edges, "C") == 3
    assert degree_sequence(vertices, edges) == (3, 2, 2, 1)
    assert neighbors(vertices, edges, "A") == {"B", "C"}
    assert is_path(vertices, edges, ("A", "B", "C", "D"))
    assert is_connected(vertices, edges)


def test_exercise_builders_accept_expected_answers() -> None:
    exercises = (
        truth_table_exercise(seed=1),
        set_operation_exercise(seed=1),
        relation_classification_exercise(seed=1),
        sequence_next_term_exercise(seed=1),
        induction_step_exercise(seed=1),
        graph_degree_exercise(seed=1),
        graph_degree_sequence_exercise(),
    )
    for exercise in exercises:
        assert exercise.check(exercise.expected).correct


def test_quiz_builders() -> None:
    quiz = discrete_math_diagnostic_quiz()
    assert quiz.total == 6
    assert quiz.questions[0].check(False).correct


def test_plot_scenes_render() -> None:
    scenes = (
        venn_two_set_scene([1, 2], [2, 3], universe=[1, 2, 3, 4]),
        relation_arrow_scene([1, 2], ["a", "b"], [(1, "a"), (2, "b")]),
        sequence_points_scene([2, 4, 6, 8]),
        finite_graph_scene(["A", "B", "C"], [("A", "B"), ("B", "C")]),
    )
    for scene in scenes:
        figure, axis = scene.render()
        assert axis.get_title()
        plt.close(figure)
