import pytest

from application.creditline import (
    Graph,
    CreditLine,
    MAX_CREDIT,
)


@pytest.fixture
def setup_graph():
    def _setup(nodes_info, edges_info, source):
        lines = [
            CreditLine.of(src, dest, "product", "tenor", "B")
            for src, dest, max_credit in edges_info
        ]
        graph = Graph.of(source, nodes_info, lines, [])
        return graph

    return _setup


# Test cases
def test_calculate_shortest_paths_directed_simple(setup_graph):
    nodes_info = ["A", "B", "C"]
    edges_info = [("A", "B", 10), ("B", "C", 5)]  # Only A -> B and B -> C
    source = "A"
    graph = setup_graph(nodes_info, edges_info, source)
    graph.calculate_shortest_paths_from_source()

    assert graph.nodes["A"].credit == 0
    assert graph.nodes["B"].credit == 10
    assert graph.nodes["C"].credit == 15  # A -> B -> C
    assert [node.house for node in graph.nodes["B"].shortest_path] == ["A"]
    assert [node.house for node in graph.nodes["C"].shortest_path] == ["A", "B"]


def test_calculate_shortest_paths_directed_no_path(setup_graph):
    nodes_info = ["A", "B", "C"]
    edges_info = [("A", "B", 10)]  # Only A -> B, no path to C
    source = "A"
    graph = setup_graph(nodes_info, edges_info, source)
    graph.calculate_shortest_paths_from_source()

    assert graph.nodes["A"].credit == 0
    assert graph.nodes["B"].credit == 10
    assert graph.nodes["C"].credit == MAX_CREDIT  # No path from A to C
    assert [node.house for node in graph.nodes["B"].shortest_path] == ["A"]
    assert (
        graph.nodes["C"].shortest_path == []
    )  # No path, so the shortest path list should be empty


def test_calculate_shortest_paths_directed_complex(setup_graph):
    nodes_info = ["A", "B", "C", "D", "E"]
    edges_info = [
        ("A", "B", 3),
        ("A", "C", 1),
        ("C", "D", 2),
        ("D", "E", 7),
    ]  # Directed edges without bidirectionality
    source = "A"
    graph = setup_graph(nodes_info, edges_info, source)
    graph.calculate_shortest_paths_from_source()

    assert graph.nodes["E"].credit == 10  # A -> C -> D -> E
    assert [node.house for node in graph.nodes["E"].shortest_path] == ["A", "C", "D"]
    assert graph.nodes["B"].credit == 3  # Only A -> B
    assert [node.house for node in graph.nodes["B"].shortest_path] == ["A"]
