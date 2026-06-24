import matplotlib.pyplot as plt
import numpy as np
import pytest

from edumath.linear_algebra import (
    LINEAR_ALGEBRA_PATH,
    can_multiply,
    determinant_2x2,
    dot_product,
    dot_product_exercise,
    eigenvalues_2x2,
    eigenvector_check_exercise,
    eigenvector_scene,
    identity_matrix,
    inverse_2x2,
    linear_algebra_diagnostic_quiz,
    linear_system_exercise,
    matrix_product,
    matrix_shape,
    matrix_shape_exercise,
    matrix_transformation_scene,
    matrix_vector_product,
    matrix_vector_product_exercise,
    scalar_multiply,
    solve_linear_system,
    system_lines_scene,
    transformation_classification_exercise,
    validate_eigenpair,
    validate_matrix_answer,
    validate_shape_answer,
    validate_solution_vector,
    validate_vector_answer,
    vector_add,
    vector_addition_scene,
    vector_norm,
    vector_norm_exercise,
    vector_scene,
)


def test_linear_algebra_path_has_expected_lessons() -> None:
    assert LINEAR_ALGEBRA_PATH.slugs() == [
        "vectors",
        "matrices",
        "matrix-operations",
        "systems-and-elimination",
        "linear-transformations",
        "eigenvalues-eigenvectors",
    ]


def test_vector_and_matrix_operations() -> None:
    assert np.allclose(vector_add([1, 2], [3, 4]), [4, 6])
    assert np.allclose(scalar_multiply(3, [1, -2]), [3, -6])
    assert dot_product([1, 2], [3, 4]) == 11
    assert vector_norm([3, 4]) == 5
    assert matrix_shape([[1, 2, 3], [4, 5, 6]]) == (2, 3)
    assert can_multiply((2, 3), (3, 4))
    assert not can_multiply((2, 3), (2, 4))
    assert np.allclose(matrix_vector_product([[2, 0], [0, 3]], [5, 4]), [10, 12])
    assert np.allclose(matrix_product([[1, 2]], [[3], [4]]), [[11]])
    assert np.allclose(identity_matrix(2), [[1, 0], [0, 1]])


def test_small_matrix_inverse_determinant_eigenvalues_and_systems() -> None:
    matrix = [[4, 7], [2, 6]]
    assert determinant_2x2(matrix) == 10
    assert np.allclose(inverse_2x2(matrix), [[0.6, -0.7], [-0.2, 0.4]])
    with pytest.raises(ValueError):
        inverse_2x2([[1, 2], [2, 4]])
    values = eigenvalues_2x2([[2, 0], [0, 3]])
    assert set(values) == {2 + 0j, 3 + 0j}
    assert np.allclose(solve_linear_system([[1, 1], [1, -1]], [5, 1]), [3, 2])


def test_validators_accept_common_student_formats() -> None:
    assert validate_vector_answer("3, 2", [3, 2]).correct
    assert validate_matrix_answer("1 0; 0 1", [[1, 0], [0, 1]]).correct
    assert validate_shape_answer("2 x 3", (2, 3)).correct
    assert validate_solution_vector("3, 2", [[1, 1], [1, -1]], [5, 1]).correct
    assert validate_eigenpair([[3, 0], [0, 1]], [1, 0], 3).correct
    assert not validate_vector_answer("3, 3", [3, 2]).correct


def test_exercise_builders_accept_expected_answers() -> None:
    exercises = (
        vector_norm_exercise(seed=1),
        dot_product_exercise(seed=1),
        matrix_shape_exercise(seed=1),
        matrix_vector_product_exercise(seed=1),
        linear_system_exercise(seed=1),
        transformation_classification_exercise(seed=1),
        eigenvector_check_exercise(seed=1),
    )
    for exercise in exercises:
        assert exercise.check(exercise.expected).correct


def test_quiz_builders() -> None:
    quiz = linear_algebra_diagnostic_quiz()
    assert quiz.total == 8
    assert quiz.questions[0].check(5).correct
    assert quiz.questions[-1].check(5).correct


def test_plot_scenes_render() -> None:
    scenes = (
        vector_scene(([3, 4], [-2, 1])),
        vector_addition_scene([1, 2], [3, 1]),
        matrix_transformation_scene([[1, 1], [0, 1]]),
        system_lines_scene([[1, 1], [1, -1]], [5, 1]),
        eigenvector_scene([[3, 0], [0, 1]], [1, 0]),
    )
    for scene in scenes:
        figure, axis = scene.render()
        assert axis.get_title()
        plt.close(figure)
