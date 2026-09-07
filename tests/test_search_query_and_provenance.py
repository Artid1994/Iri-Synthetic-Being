import unittest
from unittest.mock import Mock

from runtime.goal import Goal
from runtime.memory import Memory
from runtime.memory_brain_persistence import MemoryBrainPersistence
from runtime.research_learning import ResearchLearning
from runtime.research_safety import ResearchSafetyGate
from runtime.runtime import TranscendingRuntime
from runtime.web_research import ResearchResult, WebResearch


class TestSearchNormalizationAndProvenance(unittest.TestCase):
    def test_query_normalization_strips_operational_prefixes(self):
        cases = [
            ("Research missing knowledge for: Quantum Decoherence", "Quantum Decoherence"),
            ("Research missing knowledge about: Black Hole Entropy", "Black Hole Entropy"),
            ("Research missing knowledge: Topological Insulators", "Topological Insulators"),
            ("Investigate failure of: Motor Controller", "Motor Controller"),
            ("Investigate previous failure: Sensor Drift", "Sensor Drift"),
            ("Research: General Relativity", "General Relativity"),
            ('Research "Superconductivity"', "Superconductivity"),
            ("Ordinary topic without prefix", "Ordinary topic without prefix"),
        ]
        for raw, expected in cases:
            self.assertEqual(WebResearch.normalize_query(raw), expected)

    def test_web_research_encodes_clean_query_and_includes_timestamp(self):
        research = WebResearch(search_url="https://example.com/search?q=")
        captured = {}

        class FakeResponse:
            def read(self):
                return b"Clean content payload"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def fake_urlopen(request, timeout):
            captured["url"] = request.full_url
            return FakeResponse()

        import runtime.web_research as module
        orig = module.urlopen
        module.urlopen = fake_urlopen
        try:
            res = research.search("Research missing knowledge for: Bell Inequality")
            self.assertEqual(res.topic, "Bell Inequality")
            self.assertIn("Bell%20Inequality", captured["url"])
            self.assertNotIn("missing%20knowledge", captured["url"])
            self.assertIsNotNone(res.timestamp)
            self.assertGreater(res.timestamp, 0)
        finally:
            module.urlopen = orig

    def test_verified_research_stores_structured_provenance_in_memory_and_graph(self):
        runtime = TranscendingRuntime(cognitive=Mock())
        mock_web = Mock(spec=WebResearch)
        mock_web.search.return_value = ResearchResult(
            topic="Quantum Decoherence",
            source="https://arxiv.org/abs/quant-ph/0306072",
            content="Decoherence explains quantum to classical transition dynamically.",
            timestamp=1757161200.5,
        )
        runtime.autonomous_learning.research = mock_web

        parent = Goal("Quantum Decoherence")
        parent.pause()
        setattr(parent, "id", "parent_qid")

        child = Goal("Research missing knowledge for: Quantum Decoherence")
        setattr(child, "parent_goal_id", "parent_qid")
        runtime.goals.extend([parent, child])

        # Execute child research goal
        result = runtime.dispatch_next_goal(auto_chain=False)
        self.assertEqual(result.learning_result.status, "COMPLETED")
        self.assertTrue(result.learning_result.memory_updated)

        # Check semantic memory node in MemoryGraph
        node_id = "SEMANTIC:Decoherence explains quantum to classical transition dynamically."
        self.assertIn(node_id, runtime.memory.memory_graph.nodes)
        node = runtime.memory.memory_graph.nodes[node_id]
        self.assertEqual(node.source_url, "https://arxiv.org/abs/quant-ph/0306072")
        self.assertEqual(node.retrieval_timestamp, 1757161200.5)
        self.assertEqual(node.confidence, 0.5)

        # Check Experience object list
        web_exps = [e for e in runtime.memory.state.experiences if e.modality == "web_research"]
        self.assertEqual(len(web_exps), 1)
        self.assertEqual(web_exps[0].source, "https://arxiv.org/abs/quant-ph/0306072")
        self.assertEqual(web_exps[0].salience, 0.5)

    def test_provenance_survives_persistence_and_restart(self):
        memory1 = Memory()
        memory1.add_semantic(
            "Topological invariant",
            source_url="https://nature.com/articles/physics123",
            retrieval_timestamp=1700000000.0,
            confidence=0.9,
        )
        data = MemoryBrainPersistence.serialize_memory(memory1)

        # Restore into clean memory
        memory2 = MemoryBrainPersistence.deserialize_memory(data)
        node = memory2.memory_graph.nodes["SEMANTIC:Topological invariant"]
        self.assertEqual(node.source_url, "https://nature.com/articles/physics123")
        self.assertEqual(node.retrieval_timestamp, 1700000000.0)
        self.assertEqual(node.confidence, 0.9)


if __name__ == "__main__":
    unittest.main()
