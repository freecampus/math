import matplotlib.pyplot as plt

from edumath.python_fundamentals import (
    array_summary,
    classify_number,
    cumulative_sum,
    describe_value,
    plot_values,
    scatter_values,
)


def test_describe_value_returns_type_name_and_repr() -> None:
    info = describe_value(42)

    assert info.type_name == "int"
    assert info.representation == "42"


def test_control_flow_helpers() -> None:
    assert classify_number(-1) == "negative"
    assert classify_number(0) == "zero"
    assert classify_number(1) == "positive"
    assert cumulative_sum([1, 2, 3]) == [1, 3, 6]


def test_array_summary_returns_basic_statistics() -> None:
    summary = array_summary([1, 2, 3])

    assert summary.shape == (3,)
    assert summary.mean == 2
    assert summary.minimum == 1
    assert summary.maximum == 3
    assert summary.total == 6


def test_plot_helpers_return_matplotlib_objects() -> None:
    figure, axis = plot_values([1, 4, 9])
    assert figure is axis.figure
    plt.close(figure)

    figure, axis = scatter_values([1, 2, 3], [1, 4, 9])
    assert figure is axis.figure
    plt.close(figure)
