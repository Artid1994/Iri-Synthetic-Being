import unittest

from runtime.memory_graph import MemoryGraph


class TestMemoryGraph(unittest.TestCase):

    def setUp(self):
        self.graph = MemoryGraph()

    def test_add_node_creates_memory_node(self):
        node_id = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        self.assertIn(node_id, self.graph.nodes)

        node = self.graph.nodes[node_id]

        self.assertEqual(node.content, "quantum state")
        self.assertEqual(node.memory_type, "SEMANTIC")
        self.assertEqual(node.activation_count, 1)

    def test_same_content_reuses_existing_node(self):
        first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        second = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        self.assertEqual(first, second)
        self.assertEqual(len(self.graph.nodes), 1)

    def test_connect_creates_edge(self):
        first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        second = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

        edge = self.graph.connect(first, second)

        self.assertIn(edge, self.graph.edges)
        self.assertEqual(
            self.graph.edges[edge].source,
            first,
        )
        self.assertEqual(
            self.graph.edges[edge].target,
            second,
        )
        self.assertEqual(
            self.graph.edges[edge].weight,
            1.0,
        )
        self.assertEqual(
            self.graph.edges[edge].usage_count,
            1,
        )

    def test_reconnecting_strengthens_edge(self):
        first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        second = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

        edge = self.graph.connect(first, second)
        self.graph.connect(first, second)

        self.assertEqual(
            self.graph.edges[edge].weight,
            1.5,
        )
        self.assertEqual(
            self.graph.edges[edge].usage_count,
            2,
        )

    def test_activation_increases_node_count(self):
        node_id = self.graph.add_node(
            content="decoherence",
            memory_type="SEMANTIC",
        )

        self.graph.activate(node_id)

        self.assertEqual(
            self.graph.nodes[node_id].activation_count,
            2,
        )

    def test_invalid_node_connection_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.connect("missing_a", "missing_b")


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphDecayAndPruning(unittest.TestCase):

    def setUp(self):
        self.graph = MemoryGraph()

        self.first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        self.second = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

    def test_decay_reduces_edge_weight(self):
        edge = self.graph.connect(self.first, self.second)

        self.graph.decay(amount=0.25)

        self.assertEqual(
            self.graph.edges[edge].weight,
            0.75,
        )

    def test_decay_never_makes_weight_negative(self):
        edge = self.graph.connect(self.first, self.second)

        self.graph.decay(amount=2.0)

        self.assertEqual(
            self.graph.edges[edge].weight,
            0.0,
        )

    def test_prune_removes_weak_edges(self):
        edge = self.graph.connect(self.first, self.second)

        self.graph.decay(amount=0.5)
        self.graph.prune(threshold=0.5)

        self.assertNotIn(edge, self.graph.edges)

    def test_prune_keeps_strong_edges(self):
        edge = self.graph.connect(self.first, self.second)

        self.graph.prune(threshold=0.5)

        self.assertIn(edge, self.graph.edges)


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphRecall(unittest.TestCase):

    def setUp(self):
        self.graph = MemoryGraph()

        self.quantum = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        self.wavefunction = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

        self.decoherence = self.graph.add_node(
            content="decoherence",
            memory_type="SEMANTIC",
        )

    def test_recall_returns_connected_nodes(self):
        self.graph.connect(self.quantum, self.wavefunction)

        results = self.graph.recall(self.quantum)

        self.assertEqual(
            results,
            [self.wavefunction],
        )

    def test_recall_orders_by_edge_weight(self):
        self.graph.connect(self.quantum, self.wavefunction)
        self.graph.connect(self.quantum, self.decoherence)

        self.graph.connect(self.quantum, self.decoherence)

        results = self.graph.recall(self.quantum)

        self.assertEqual(
            results,
            [self.decoherence, self.wavefunction],
        )

    def test_recall_does_not_return_unconnected_nodes(self):
        self.graph.connect(self.quantum, self.wavefunction)

        results = self.graph.recall(self.quantum)

        self.assertNotIn(
            self.decoherence,
            results,
        )

    def test_recall_missing_node_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.recall("missing_node")


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphValidation(unittest.TestCase):

    def setUp(self):
        self.graph = MemoryGraph()

    def test_empty_content_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.add_node("", "SEMANTIC")

    def test_empty_memory_type_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.add_node("quantum state", "")

    def test_missing_node_activation_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.activate("missing_node")

    def test_self_connection_is_rejected(self):
        node = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        with self.assertRaises(ValueError):
            self.graph.connect(node, node)

    def test_negative_decay_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.decay(amount=-0.1)

    def test_negative_pruning_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            self.graph.prune(threshold=-0.1)

    def test_pruning_does_not_delete_nodes(self):
        first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        second = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

        self.graph.connect(first, second)
        self.graph.decay(amount=1.0)
        self.graph.prune(threshold=0.0)

        self.assertIn(first, self.graph.nodes)
        self.assertIn(second, self.graph.nodes)

    def test_recall_does_not_modify_edge(self):
        first = self.graph.add_node(
            content="quantum state",
            memory_type="SEMANTIC",
        )

        second = self.graph.add_node(
            content="wavefunction",
            memory_type="SEMANTIC",
        )

        edge = self.graph.connect(first, second)

        weight_before = self.graph.edges[edge].weight
        usage_before = self.graph.edges[edge].usage_count

        self.graph.recall(first)

        self.assertEqual(
            self.graph.edges[edge].weight,
            weight_before,
        )
        self.assertEqual(
            self.graph.edges[edge].usage_count,
            usage_before,
        )


if __name__ == "__main__":
    unittest.main()
