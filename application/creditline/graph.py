from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Iterable, Set, Deque

from more_itertools import consume

from .line import MAX_CREDIT, CreditLine


def calculate_shortest_paths(nodes: Dict[str, Node], source: str) -> None:
    """Calculate the shortest paths from the source to all other nodes using Dijkstra's algorithm."""
    if source not in nodes:
        raise ValueError(f"Source node '{source}' not found in nodes.")

    source_node = nodes[source]
    source_node.initialize_as_source()

    unsettled_nodes: Deque[Node] = deque([source_node])

    while unsettled_nodes:
        current_node = unsettled_nodes.popleft()

        for house, credit in current_node.adjacent_node_distances.items():
            adjacent_node = current_node.adjacent_nodes[house]
            updated = update_credit_and_path(adjacent_node, credit, current_node)
            if updated and not adjacent_node.visited:
                unsettled_nodes.append(adjacent_node)
                adjacent_node.mark_visited()


def update_credit_and_path(adjacent_node: Node, credit: int, source_node: Node) -> bool:
    """Update the distance and path of an adjacent node if a shorter path is found."""
    new_distance = source_node.credit + credit
    if adjacent_node.credit < new_distance:
        adjacent_node.credit = new_distance
        adjacent_node.shortest_path = source_node.shortest_path + [source_node]
        return True
    return False


@dataclass
class Node:
    house: str
    shortest_path: List[Node] = field(default_factory=list)
    all_paths: List[List[Node]] = field(default_factory=list)
    credit: int = field(default=-MAX_CREDIT)
    visited: bool = False
    adjacent_node_distances: Dict[str, int] = field(default_factory=dict)
    adjacent_nodes: Dict[str, Node] = field(default_factory=dict)

    def initialize_as_source(self) -> None:
        """Set the node as the source by resetting its distance and marking it as visited."""
        self.credit = 0
        self.visited = True
        self.shortest_path = []

    def add_destination(self, destination: Node, distance: int):
        self.adjacent_node_distances[destination.house] = distance
        self.add_adjacent_node(destination)

    def add_adjacent_node(self, node: Node):
        self.adjacent_nodes[node.house] = node

    def set_shortest_path(self, shortest_path: List[Node]):
        self.shortest_path = shortest_path
        if shortest_path not in self.all_paths:
            self.all_paths.insert(0, shortest_path)
            self.all_paths = self.all_paths[:5]
            self.all_paths.sort(key=lambda x: x[-1].credit, reverse=True)

    def mark_visited(self):
        self.visited = True


@dataclass
class Graph:
    source: str
    nodes: Dict[str, Node] = field(default_factory=dict)
    credit_line_map: Dict[Tuple[str, str], CreditLine] = field(
        default_factory=dict, init=False
    )

    @classmethod
    def of(
        cls,
        source: str,
        houses: Set[str],
        credit_lines: List[CreditLine],
        switchers: Set[str],
    ) -> Graph:
        graph = cls(source)
        graph.create_nodes(houses)
        graph.add_lines(credit_lines)
        graph.link_nodes_with_switchers(houses, switchers)
        graph.calculate_shortest_paths_from_source()
        return graph

    def link_nodes_with_switchers(self, houses: Set[str], switchers: Set[str]) -> None:
        consume(self.link_node(node, houses, switchers) for node in self.nodes.values())

    def link_node(self, node: Node, houses: Set[str], switchers: Set[str]) -> None:
        consume(
            self.set_node_credit(node, house)
            for house in houses
            if house != node.house and self.is_switchable(node.house, house, switchers)
        )

    def is_switchable(
        self, from_house: str, to_house: str, switchers: Set[str]
    ) -> bool:
        return (
            (from_house in switchers or to_house in switchers)
            and (from_house, to_house) in self.credit_line_map
            and (to_house, from_house) in self.credit_line_map
        )

    def set_node_credit(self, node: Node, house: str):
        credit_distance = (
            MAX_CREDIT
            + 1
            - min(
                self.credit_line_map[(node.house, house)].max,
                self.credit_line_map[(house, node.house)].max,
            )
        )
        node.add_destination(self.nodes[house], credit_distance)

    def create_node(self, house: str) -> None:
        self.nodes[house] = Node(house)

    def create_nodes(self, houses: Iterable[str]):
        consume(self.create_node(h) for h in houses)

    def add_line(self, line: CreditLine) -> None:
        self.credit_line_map[(line.source, line.destination)] = line
        source_node = self.nodes.get(line.source)
        destination_node = self.nodes.get(line.destination)
        source_node.add_destination(destination_node, line.remaining)

    def add_lines(self, lines: List[CreditLine]):
        consume(self.add_line(line) for line in lines)

    def calculate_shortest_paths_from_source(self):
        calculate_shortest_paths(self.nodes, self.source)
