from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryNode:
    content: str
    memory_type: str
    activation_count: int = 1


@dataclass
class MemoryEdge:
    source: str
    target: str
    weight: float = 1.0
    usage_count: int = 1


class MemoryGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, MemoryNode] = {}
        self.edges: dict[tuple[str, str], MemoryEdge] = {}

    def add_node(self, content: str, memory_type: str) -> str:
        content = content.strip()
        memory_type = memory_type.strip()

        if not content:
            raise ValueError("Memory node content cannot be empty")

        if not memory_type:
            raise ValueError("Memory node type cannot be empty")

        node_id = self._node_id(content, memory_type)

        if node_id in self.nodes:
            self.nodes[node_id].activation_count += 1
            return node_id

        self.nodes[node_id] = MemoryNode(
            content=content,
            memory_type=memory_type,
        )

        return node_id

    def activate(self, node_id: str) -> None:
        node = self.nodes.get(node_id)

        if node is None:
            raise ValueError("Memory node does not exist")

        node.activation_count += 1

    def co_activate(self, source: str, target: str) -> tuple[str, str]:
        if source not in self.nodes:
            raise ValueError("Source memory node does not exist")

        if target not in self.nodes:
            raise ValueError("Target memory node does not exist")

        if source == target:
            raise ValueError("Memory node cannot co-activate with itself")

        self.activate(source)
        self.activate(target)

        return self.connect(source, target)

    def connect(self, source: str, target: str) -> tuple[str, str]:
        if source not in self.nodes:
            raise ValueError("Source memory node does not exist")

        if target not in self.nodes:
            raise ValueError("Target memory node does not exist")

        if source == target:
            raise ValueError("Memory node cannot connect to itself")

        edge_id = (source, target)

        edge = self.edges.get(edge_id)

        if edge is None:
            self.edges[edge_id] = MemoryEdge(
                source=source,
                target=target,
            )
        else:
            edge.weight += 0.5
            edge.usage_count += 1

        return edge_id

    def decay(self, amount: float = 0.1) -> None:
        if amount < 0:
            raise ValueError("Decay amount cannot be negative")

        for edge in self.edges.values():
            edge.weight = max(0.0, edge.weight - amount)

    def prune(self, threshold: float = 0.1) -> None:
        if threshold < 0:
            raise ValueError("Pruning threshold cannot be negative")

        self.edges = {
            edge_id: edge
            for edge_id, edge in self.edges.items()
            if edge.weight > threshold
        }

    def recall(self, node_id: str) -> list[str]:
        if node_id not in self.nodes:
            raise ValueError("Memory node does not exist")

        related = [
            edge
            for edge in self.edges.values()
            if edge.source == node_id
        ]

        related.sort(
            key=lambda edge: edge.weight,
            reverse=True,
        )

        return [edge.target for edge in related]

    @staticmethod
    def _node_id(content: str, memory_type: str) -> str:
        return f"{memory_type}:{content}"
