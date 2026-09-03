from dataclasses import asdict, is_dataclass


def snapshot_value(value):
    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, dict):
        return {
            key: snapshot_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            snapshot_value(item)
            for item in value
        ]

    return value


class RuntimeSnapshot:
    def __init__(self, runtime):
        self.runtime = runtime

    def capture(self):
        snapshot = snapshot_value(
            self.runtime.snapshot()
        )

        graph = self.runtime.memory.memory_graph

        snapshot["memory_graph"] = {
            "nodes": {
                node_id: snapshot_value(node)
                for node_id, node in graph.nodes.items()
            },
            "edges": {
                f"{source}->{target}": snapshot_value(edge)
                for (source, target), edge in graph.edges.items()
            },
        }

        return snapshot
