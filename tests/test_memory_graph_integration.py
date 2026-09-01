import unittest

from runtime.memory import Memory


class TestMemoryGraphIntegration(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_add_experience_creates_graph_node(self):
        self.memory.add_experience("quantum state")

        node_id = "EPISODIC:quantum state"

        self.assertIn(node_id, self.memory.memory_graph.nodes)
        self.assertEqual(
            self.memory.memory_graph.nodes[node_id].content,
            "quantum state",
        )

    def test_add_semantic_creates_graph_node(self):
        self.memory.add_semantic("decoherence")

        node_id = "SEMANTIC:decoherence"

        self.assertIn(node_id, self.memory.memory_graph.nodes)
        self.assertEqual(
            self.memory.memory_graph.nodes[node_id].content,
            "decoherence",
        )

    def test_existing_memory_api_remains_compatible(self):
        self.memory.add_experience("quantum state")

        self.assertEqual(
            self.memory.recall("quantum state"),
            "quantum state",
        )

    def test_associate_creates_graph_edge(self):
        self.memory.add_experience("quantum state")
        self.memory.add_semantic("wavefunction")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )

        source = "EPISODIC:quantum state"
        target = "SEMANTIC:wavefunction"

        edge_id = (source, target)

        self.assertIn(
            edge_id,
            self.memory.memory_graph.edges,
        )

    def test_associations_api_remains_compatible(self):
        self.memory.associate(
            "quantum state",
            "wavefunction",
        )

        self.assertEqual(
            self.memory.associations("quantum state"),
            ["wavefunction"],
        )


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphSynchronization(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_import_structured_creates_graph_nodes(self):
        from runtime.memory_processing import StructuredMemory

        structured = StructuredMemory(
            episodic=("quantum state",),
            semantic=("decoherence",),
        )

        self.memory.import_structured(structured)

        self.assertIn(
            "EPISODIC:quantum state",
            self.memory.memory_graph.nodes,
        )

        self.assertIn(
            "SEMANTIC:decoherence",
            self.memory.memory_graph.nodes,
        )

    def test_import_structured_does_not_duplicate_graph_nodes(self):
        from runtime.memory_processing import StructuredMemory

        structured = StructuredMemory(
            episodic=("quantum state",),
            semantic=("decoherence",),
        )

        self.memory.import_structured(structured)
        self.memory.import_structured(structured)

        self.assertEqual(
            len(self.memory.memory_graph.nodes),
            2,
        )


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphPrunePolicy(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_memory_prune_does_not_delete_graph_nodes(self):
        self.memory.add_experience("old experience")
        self.memory.add_experience("new experience")

        self.memory.prune(max_episodic=1)

        self.assertIn(
            "EPISODIC:old experience",
            self.memory.memory_graph.nodes,
        )

        self.assertIn(
            "EPISODIC:new experience",
            self.memory.memory_graph.nodes,
        )

    def test_memory_prune_does_not_delete_graph_edges(self):
        self.memory.add_experience("quantum state")
        self.memory.add_semantic("wavefunction")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )

        edge_id = (
            "EPISODIC:quantum state",
            "SEMANTIC:wavefunction",
        )

        self.memory.prune(max_episodic=0)

        self.assertIn(
            edge_id,
            self.memory.memory_graph.edges,
        )


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphRealUsage(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_multiple_memories_create_independent_graph_nodes(self):
        self.memory.add_experience("quantum state")
        self.memory.add_experience("classical state")
        self.memory.add_semantic("decoherence")

        self.assertEqual(
            len(self.memory.memory_graph.nodes),
            3,
        )

    def test_multiple_associations_are_kept(self):
        self.memory.add_experience("quantum state")
        self.memory.add_semantic("wavefunction")
        self.memory.add_semantic("decoherence")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )
        self.memory.associate(
            "quantum state",
            "decoherence",
        )

        graph = self.memory.memory_graph

        source = "EPISODIC:quantum state"

        self.assertEqual(
            len(graph.recall(source)),
            2,
        )

        self.assertIn(
            "SEMANTIC:wavefunction",
            graph.recall(source),
        )

        self.assertIn(
            "SEMANTIC:decoherence",
            graph.recall(source),
        )

    def test_recall_isolated_between_source_nodes(self):
        self.memory.add_experience("quantum state")
        self.memory.add_experience("classical state")

        self.memory.add_semantic("wavefunction")
        self.memory.add_semantic("measurement")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )
        self.memory.associate(
            "classical state",
            "measurement",
        )

        graph = self.memory.memory_graph

        quantum = graph.recall(
            "EPISODIC:quantum state"
        )

        classical = graph.recall(
            "EPISODIC:classical state"
        )

        self.assertEqual(
            quantum,
            ["SEMANTIC:wavefunction"],
        )

        self.assertEqual(
            classical,
            ["SEMANTIC:measurement"],
        )

    def test_repeated_association_strengthens_real_memory_edge(self):
        self.memory.add_experience("quantum state")
        self.memory.add_semantic("wavefunction")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )
        self.memory.associate(
            "quantum state",
            "wavefunction",
        )

        edge_id = (
            "EPISODIC:quantum state",
            "SEMANTIC:wavefunction",
        )

        edge = self.memory.memory_graph.edges[edge_id]

        self.assertEqual(edge.usage_count, 2)
        self.assertEqual(edge.weight, 1.5)


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphLifecycle(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

        self.memory.add_experience("quantum state")
        self.memory.add_semantic("wavefunction")

        self.memory.associate(
            "quantum state",
            "wavefunction",
        )

        self.source = "EPISODIC:quantum state"
        self.target = "SEMANTIC:wavefunction"
        self.edge_id = (self.source, self.target)

    def test_strengthening_decay_pruning_lifecycle(self):
        graph = self.memory.memory_graph

        graph.connect(self.source, self.target)

        self.assertEqual(
            graph.edges[self.edge_id].weight,
            1.5,
        )

        graph.decay(amount=0.5)

        self.assertEqual(
            graph.edges[self.edge_id].weight,
            1.0,
        )

        graph.decay(amount=1.0)
        graph.prune(threshold=0.0)

        self.assertNotIn(
            self.edge_id,
            graph.edges,
        )

    def test_pruned_edge_is_not_recalled(self):
        graph = self.memory.memory_graph

        graph.decay(amount=1.0)
        graph.prune(threshold=0.0)

        self.assertEqual(
            graph.recall(self.source),
            [],
        )

    def test_pruning_edge_preserves_memory_nodes(self):
        graph = self.memory.memory_graph

        graph.decay(amount=1.0)
        graph.prune(threshold=0.0)

        self.assertIn(
            self.source,
            graph.nodes,
        )

        self.assertIn(
            self.target,
            graph.nodes,
        )


if __name__ == "__main__":
    unittest.main()


class TestMemoryGraphStructuredImportEdgeCases(unittest.TestCase):

    def setUp(self):
        self.memory = Memory()

    def test_import_multiple_episodic_items_creates_all_graph_nodes(self):
        from runtime.memory_processing import StructuredMemory

        structured = StructuredMemory(
            episodic=(
                "experience one",
                "experience two",
                "experience three",
            ),
            semantic=(),
        )

        self.memory.import_structured(structured)

        for experience in structured.episodic:
            self.assertIn(
                f"EPISODIC:{experience}",
                self.memory.memory_graph.nodes,
            )

    def test_import_empty_episodic_does_not_fail(self):
        from runtime.memory_processing import StructuredMemory

        structured = StructuredMemory(
            episodic=(),
            semantic=(),
        )

        self.memory.import_structured(structured)

        self.assertEqual(
            len(self.memory.memory_graph.nodes),
            0,
        )


if __name__ == "__main__":
    unittest.main()


class TestMemoryCoActivation(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_co_activate_creates_graph_edge(self):
        edge_id = self.memory.co_activate(
            "quantum state",
            "wavefunction",
        )

        self.assertIn(edge_id, self.memory.memory_graph.edges)

    def test_co_activate_strengthens_existing_relation(self):
        edge_id = self.memory.co_activate(
            "quantum state",
            "wavefunction",
        )
        self.memory.co_activate(
            "quantum state",
            "wavefunction",
        )

        edge = self.memory.memory_graph.edges[edge_id]

        self.assertEqual(edge.usage_count, 2)
        self.assertEqual(edge.weight, 1.5)

    def test_unrelated_memory_is_not_connected(self):
        self.memory.co_activate(
            "quantum state",
            "wavefunction",
        )

        graph = self.memory.memory_graph
        third = graph.add_node("classical state", "SEMANTIC")

        first = graph.add_node("quantum state", "SEMANTIC")

        self.assertNotIn((first, third), graph.edges)
        self.assertNotIn((third, first), graph.edges)

    def test_existing_memory_api_remains_unchanged(self):
        self.memory.add_experience("quantum measurement")

        self.assertEqual(
            self.memory.recall("quantum measurement"),
            "quantum measurement",
        )
